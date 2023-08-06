"""Class for the economic dispatch framework. Allows to parametrize and run
an economic dispatch based on RES and consumption time series"""

from collections import namedtuple
from copy import deepcopy
import datetime as dt
import os

import grid2op
from grid2op.Chronics import ChangeNothing
import numpy as np
import pandas as pd
import plotly.express as px
import pypsa

from chronix2grid.generation.dispatch.utils import RampMode
from chronix2grid.generation.thermal.EDispatch_L2RPN2020.run_economic_dispatch import (
    main_run_disptach)
from chronix2grid.generation.thermal.EDispatch_L2RPN2020.utils import add_noise_gen

DispatchResults = namedtuple('DispatchResults', ['chronix', 'terminal_conditions'])


def init_dispatcher_from_config(grid_path, input_folder):

    env118_withoutchron = grid2op.make("blank",
                                       grid_path=grid_path,
                                       chronics_class=ChangeNothing)

    dispatcher = Dispatcher.from_gri2op_env(env118_withoutchron)

    dispatcher.read_hydro_guide_curves(
        os.path.join(input_folder, 'patterns', 'hydro_french.csv'))

    return dispatcher


class Dispatcher(pypsa.Network):
    """Wrapper around a pypsa.Network to add higher level methods"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add('Bus', 'node')
        self.add('Load', name='agg_load', bus='node')
        self._env = None  # The grid2op environment when instanciated with from_gri2dop_env
        self._chronix_scenario = None
        self._simplified_chronix_scenario = None
        self._has_results = False
        self._has_simplified_results = False

    @property
    def wind_p(self):
        if self._chronix_scenario is None:
            raise Exception('Cannot access this property before instantiated the Load and '
                            'renewables scenario.')
        return self._chronix_scenario.wind_p

    @property
    def solar_p(self):
        if self._chronix_scenario is None:
            raise Exception('Cannot access this property before instantiated the Load and '
                            'renewables scenario.')
        return self._chronix_scenario.solar_p

    @property
    def chronix_scenario(self):
        if self._chronix_scenario is None:
            raise Exception('Cannot access this property before instantiated the Load and '
                            'renewables scenario.')
        return self._chronix_scenario

    @chronix_scenario.setter
    def chronix_scenario(self, chronix_scenario):
        if not isinstance(chronix_scenario, ChroniXScenario):
            raise Exception('The chronix_scenario argument should be an instance of '
                            'ChronixScenario.')
        self._chronix_scenario = chronix_scenario

    def net_load(self, losses_pct, name):
        if self._chronix_scenario is None:
            raise Exception('Cannot compute net load before instantiated the Load and'
                            'renewables scenario.')
        return self._chronix_scenario.net_load(losses_pct, name)

    def nlargest_ramps(self, n, losses_pct):
        ramps = self.net_load(losses_pct, "").diff()
        return ramps.nlargest(n, ramps.columns[0])

    @classmethod
    def from_gri2op_env(cls, grid2op_env):
        net = cls()
        net._env = grid2op_env

        carrier_types_to_exclude = ['wind', 'solar']

        for i, generator in enumerate(grid2op_env.name_gen):
            gen_type = grid2op_env.gen_type[i]
            if gen_type not in carrier_types_to_exclude:
                net.add(
                    class_name='Generator', name=generator, bus='node',
                    p_nom=grid2op_env.gen_pmax[i], carrier=grid2op_env.gen_type[i],
                    marginal_cost=grid2op_env.gen_cost_per_MW[i],
                    ramp_limit_up=grid2op_env.gen_max_ramp_up[i] / grid2op_env.gen_pmax[i],
                    ramp_limit_down=grid2op_env.gen_max_ramp_down[i] / grid2op_env.gen_pmax[i],
                )

        return net

    def reset_ramps_from_grid2op_env(self):
        if self._env is None:
            raise Exception('This method can only be applied when Dispatch has been'
                            'instantiated from a grid2op Environment.')
        for i, generator in enumerate(self._env.name_gen):
            if generator in self.generators.index:
                self.generators.loc[generator, 'ramp_limit_up'] = \
                    self._env.gen_max_ramp_up[i] / self._env.gen_pmax[i]
                self.generators.loc[generator, 'ramp_limit_down'] = \
                    self._env.gen_max_ramp_down[i] / self._env.gen_pmax[i]

    def read_hydro_guide_curves(self, hydro_file_path):
        dateparse = lambda x: dt.datetime.strptime(x, '%d/%m/%Y %H:%M')
        hydro_pattern = pd.read_csv(hydro_file_path, usecols=[0, 2, 3],
                                    parse_dates=[0], date_parser=dateparse)
        hydro_pattern.set_index(hydro_pattern.columns[0], inplace=True)
        hydro_names = self.generators[self.generators.carrier == 'hydro'].index

        for extremum in ['min', 'max']:
            hydro_pu = hydro_pattern[[f'p_{extremum}_u'] * len(hydro_names)]
            hydro_pu.columns = hydro_names
            hydro_pu.index = hydro_pu.index.map(
                lambda x: (x.month, x.day, x.hour, x.minute, x.second))
            setattr(self, f'_{extremum}_hydro_pu', hydro_pu)

        self._hydro_file_path = hydro_file_path

    def read_load_and_res_scenario(self, load_path_file, prod_path_file, scenario_name):
        if self._env is None:
            raise Exception('This method can only be applied when Dispatch has been'
                            'instantiated from a grid2op Environment.')
        res_names = dict(
            wind=[name for i, name in enumerate(self._env.name_gen)
                  if self._env.gen_type[i] == 'wind'],
            solar=[name for i, name in enumerate(self._env.name_gen)
                   if self._env.gen_type[i] == 'solar']
        )
        self._chronix_scenario = ChroniXScenario.from_disk(load_path_file, prod_path_file,
                                                           res_names, scenario_name=scenario_name)

    def make_hydro_constraints_from_res_load_scenario(self):
        if self._chronix_scenario is None or self._hydro_file_path is None:
            raise Exception('This method can only be applied when a Scenario for load'
                            'and renewables has been instantiated and hydro guide'
                            'curves have been read.')
        index_slice = self._chronix_scenario.loads.index.map(
           lambda x: (x.month, x.day, x.hour, x.minute, x.second)
        )

        self._min_hydro_pu = self._min_hydro_pu.reindex(index_slice).fillna(method='ffill')
        self._max_hydro_pu = self._max_hydro_pu.reindex(index_slice).fillna(method='ffill')

        return {'p_max_pu': self._max_hydro_pu.copy(), 'p_min_pu': self._min_hydro_pu.copy()}

    def modify_marginal_costs(self, new_costs):
        """
        Modify marginal costs used for the dispatch given a dictionary
        providing new costs for carriers.

        Parameters
        ----------
        new_costs: dict
            new costs by carrier

        """
        for carrier, new_cost in new_costs.items():
            try:
                targeted_generators = self.generators.carrier.isin([carrier])
                self.generators.loc[targeted_generators, 'marginal_cost'] = new_cost
            except KeyError:
                print(f'Carrier {carrier} is not a valid carrier')
                raise

    def plot_ramps(self):
        caract_gen = self.generators[['p_nom', 'carrier', 'ramp_limit_up']].reset_index()
        caract_gen = caract_gen.rename(columns={'index': 'name'})

        fig = px.scatter(
            caract_gen, x='p_nom', y='ramp_limit_up', color='carrier',
            hover_data=['name']
        )
        return fig

    def simplify_net(self):
        carriers = self.generators.carrier.unique()
        simplified_net = Dispatcher()
        for carrier in carriers:
            names = self.generators[self.generators.carrier == carrier].index.tolist()

            gens = self.generators.loc[
                names,
                ['p_nom', 'ramp_limit_up', 'ramp_limit_down', 'marginal_cost']
            ]
            gens['ramp_up_mw'] = gens['p_nom'] * gens['ramp_limit_up']
            gens['ramp_down_mw'] = gens['p_nom'] * gens['ramp_limit_down']
            params = gens.agg(['sum', 'mean'])
            simplified_net.add(
                class_name='Generator', name=carrier, bus='node',
                p_nom=params.loc['sum', 'p_nom'], carrier=carrier,
                marginal_cost=params.loc['mean', 'marginal_cost'],
                ramp_limit_up=params.loc['sum', 'ramp_up_mw'] / params.loc['sum', 'p_nom'],
                ramp_limit_down=params.loc['sum', 'ramp_down_mw'] / params.loc['sum', 'p_nom'],
            )
        simplified_net._hydro_file_path = self._hydro_file_path
        simplified_net._min_hydro_pu = self._min_hydro_pu.iloc[:, 0]
        simplified_net._max_hydro_pu = self._max_hydro_pu.iloc[:, 0]

        print('simplified dispatch by carrier')
        full_ramp = simplified_net.generators['p_nom'] * simplified_net.generators['ramp_limit_up']
        df_full_ramp = pd.DataFrame({'full_ramp': full_ramp})

        print(pd.concat(
            [
                simplified_net.generators[['p_nom', 'ramp_limit_up',
                                           'ramp_limit_down', 'marginal_cost']],
                df_full_ramp
            ], axis=1))
        return simplified_net

    def run(self, load, params, gen_constraints=None,
                     ramp_mode=RampMode.hard, by_carrier=False):
        prods_dispatch, terminal_conditions, marginal_prices = main_run_disptach(
            self if not by_carrier else self.simplify_net(),
            load, params, gen_constraints, ramp_mode)
        if by_carrier:
            self._simplified_chronix_scenario = self._chronix_scenario.simplify_chronix()
            self._simplified_chronix_scenario.prods_dispatch = prods_dispatch
            self._simplified_chronix_scenario.marginal_prices = marginal_prices
            results = self._simplified_chronix_scenario
            self._has_simplified_results = True
            self._has_results = False
        else:
            self._chronix_scenario.prods_dispatch = prods_dispatch
            self._chronix_scenario.marginal_prices = marginal_prices
            results = self._chronix_scenario
            self._has_results = True
            self._has_simplified_results = False
        self.reset_ramps_from_grid2op_env()
        return DispatchResults(chronix=results, terminal_conditions=terminal_conditions)

    def save_results(self, output_folder):
        if not self._has_results and not self._has_simplified_results:
            print('The optimization has first to run successfully in order to '
                  'save results.')
        if self._has_results:
            print('Saving results for the grids with individual generators...')
            res_load_scenario = self.chronix_scenario
        else:
            print('Saving results for the grids with aggregated generators by carriers...')
            res_load_scenario = self._simplified_chronix_scenario

        full_opf_dispatch = pd.concat(
            [res_load_scenario.prods_dispatch, res_load_scenario.wind_p,
             res_load_scenario.solar_p],
            axis=1
        )
        try:
            full_opf_dispatch = full_opf_dispatch[self._env.name_gen].round(2)
        except KeyError:
            # Either we're trying to save results from a simplified dispatch or
            # using the save function before instanciating an env.
            pass

        gen_cap = pd.Series({gen_name: gen_pmax for gen_name, gen_pmax in
                             zip(self._env.name_gen, self._env.gen_pmax)})
        prod_p_with_noise = add_noise_gen(full_opf_dispatch, gen_cap, noise_factor=0.0007)

        print(f'Saving chronics into {output_folder}')
        full_opf_dispatch.to_csv(
            os.path.join(output_folder, "prod_p_forecasted.csv.bz2"),
            sep=';', index=False
        )
        prod_p_with_noise.to_csv(
            os.path.join(output_folder, "prod_p.csv.bz2"),
            sep=';', index=False
        )
        res_load_scenario.marginal_prices.to_csv(
            os.path.join(output_folder, "prices.csv.bz2"),
            sep=';', index=False
        )
        res_load_scenario.loads.to_csv(
            os.path.join(output_folder, "load_p.csv.bz2"),
            sep=';', index=False
        )


class ChroniXScenario:
    def __init__(self, loads, prods, res_names, scenario_name):
        self.loads = loads
        self.wind_p = prods[res_names['wind']]
        self.solar_p = prods[res_names['solar']]
        self.total_res = pd.concat([self.wind_p, self.solar_p], axis=1).sum(axis=1)
        self.prods_dispatch = None  # Will receive the results of the dispatch
        self.marginal_prices = None # Will receive the marginal prices associated to a dispatch
        self.name = scenario_name

    @classmethod
    def from_disk(cls, load_path_file, prod_path_file, res_names, scenario_name):
        loads = pd.read_csv(load_path_file, sep=';', index_col=0, parse_dates=True)
        prods = pd.read_csv(prod_path_file, sep=';', index_col=0, parse_dates=True)
        return cls(loads, prods, res_names, scenario_name)

    def net_load(self, losses_pct, name):
        load_minus_losses = self.loads.sum(axis=1) * (1 + losses_pct/100)
        return (load_minus_losses - self.total_res).to_frame(name=name)

    def simplify_chronix(self):
        simplified_chronix = deepcopy(self)
        simplified_chronix.wind_p = simplified_chronix.wind_p.sum(axis=1).to_frame(name='wind')
        simplified_chronix.solar_p = simplified_chronix.solar_p.sum(axis=1).to_frame(name='solar')
        simplified_chronix.name = simplified_chronix.name + 'by_carrier'
        return simplified_chronix


if __name__ == "__main__":
    import os
    import grid2op
    from grid2op.Chronics import ChangeNothing
    import chronix2grid.generation.thermal.EDispatch_L2RPN2020.run_economic_dispatch as run_economic_dispatch

    INPUT_FOLDER = 'chronix2grid/generation/input'
    CASE = 'case118_l2rpn'
    path_grid = os.path.join(INPUT_FOLDER, CASE)

    losses_pct = 3.0

    env118_blank = grid2op.make(
        "blank",
        grid_path=os.path.join(path_grid, "L2RPN_2020_case118_redesigned.json"),
        chronics_class=ChangeNothing,
    )
    params = {'snapshots': [],
              'step_opf_min': 5,
              'mode_opf': 'week',
              'reactive_comp': 1.025,
              }
    chronics_path_gen = os.path.join(INPUT_FOLDER, "dispatch", str(2012))
    this_path = os.path.join(chronics_path_gen, 'Scenario_0')
    dispatch = Dispatcher.from_gri2op_env(env118_blank)
    dispatch.read_hydro_guide_curves(os.path.join(INPUT_FOLDER, 'patterns', 'hydro.csv'))
    dispatch.read_load_and_res_scenario(os.path.join(this_path, 'load_p.csv.bz2'),
                                        os.path.join(this_path, 'prod_p.csv.bz2'),
                                        'Scenario_0')
    dispatch.make_hydro_constraints_from_res_load_scenario()
    net_by_carrier = dispatch.simplify_net()
    agg_load_without_renew = dispatch.net_load(losses_pct, name=dispatch.loads.index[0])

    # Prepare gen constraints for EDispatch module
    hydro_constraints = {'p_max_pu': dispatch._max_hydro_pu.copy(),
                         'p_min_pu': dispatch._min_hydro_pu.copy()}

    opf_dispatch, term_conditions = dispatch.run(
        agg_load_without_renew,
        params=params,
        gen_constraints=hydro_constraints,
        ramp_mode=run_economic_dispatch.RampMode.easy,
        by_carrier=False  # True to run the dispatch only aggregated generators by carrier
    )

    dispatch.save_results('.')
    test_prods = pd.read_csv('./Scenario_0/prod_p.csv.bz2', sep=";")
    test_prices = pd.read_csv('./Scenario_0/prices.csv.bz2', sep=";")




