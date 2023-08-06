# Native python libraries
import os
import json

# Other Python libraries
import pandas as pd
import numpy as np
from datetime import timedelta


# Libraries developed for this module
from .consumption import generate_load as gen_loads
from .renewable import generate_solar_wind as gen_enr
from .thermal import generate_dispatch as gen_dispatch
from .dispatch import utils as du
from .dispatch import EconomicDispatch as ec
from . import generation_utils as gu
from ..config import DispatchConfigManager, LoadsConfigManager, ResConfigManager


def time_parameters(weeks, start_date):
    result = dict()
    start_date = pd.to_datetime(start_date, format='%Y-%m-%d')
    result['weeks'] = weeks
    result['start_date'] = start_date
    result['year'] = start_date.year
    return result


def updated_time_parameters_with_timestep(time_parameters, timestep):
    time_parameters['end_date'] = time_parameters['start_date'] + timedelta(
        days=7 * int(time_parameters['weeks'])) - timedelta(minutes=timestep)
    time_parameters['T'] = int(
        pd.Timedelta(
            time_parameters['end_date'] - time_parameters['start_date']
        ).total_seconds() // 60
    )
    return time_parameters


# Call generation scripts n_scenario times with dedicated random seeds
def main(case, n_scenarios, input_folder, output_folder, time_params, mode='LRTK'):
    """
    Main function for chronics generation. It works with three steps: load generation, renewable generation (solar and wind) and then dispatch computation to get the whole energy mix

    Parameters
    ----------
    case (str): name of case to study (must be a folder within input_folder)
    year (int): year of generation
    n_scenarios (int): number of desired scenarios to generate for the same timescale
    params (dict): parameters of generation, as returned by function chronix2grid.generation.generate_chronics.read_configuration
    input_folder (str): path of folder containing inputs
    output_folder (str): path where outputs will be written (intermediate folder case/year/scenario will be used)
    prods_charac (pandas.DataFrame): as returned by function chronix2grid.generation.generate_chronics.read_configuration
    loads_charac (pandas.DataFrame): as returned by function chronix2grid.generation.generate_chronics.read_configuration
    lines (pandas.DataFrame): as returned by function chronix2grid.generation.generate_chronics.read_configuration
    solar_pattern (pandas.DataFrame): as returned by function chronix2grid.generation.generate_chronics.read_configuration
    load_weekly_pattern (pandas.DataFrame): as returned by function chronix2grid.generation.generate_chronics.read_configuration
    mode (str): options to launch certain parts of the generation process : L load R renewable T thermal

l
    Returns
    -------

    """

    print('=====================================================================================================================================')
    print('============================================== CHRONICS GENERATION ==================================================================')
    print('=====================================================================================================================================')

    ## Random seeds:  Make sure the seeds are the same, whether computation is parallel or sequential
    seeds = [np.random.randint(low=0, high=2 ** 31) for _ in range(n_scenarios)]

    ## Folder settings
    year = time_params['year']

    dispatch_input_folder, dispatch_input_folder_case, dispatch_output_folder = gu.make_generation_input_output_directories(input_folder, case, year, output_folder)
    load_config_manager = LoadsConfigManager(
        name="Loads Generation",
        root_directory=input_folder,
        input_directories=dict(case=case, patterns='patterns'),
        required_input_files=dict(case=['loads_charac.csv', 'params.json'],
                                  patterns=['load_weekly_pattern.csv']),
        output_directory=dispatch_input_folder
    )
    load_config_manager.validate_configuration()

    params, loads_charac, load_weekly_pattern = load_config_manager.read_configuration()

    res_config_manager = ResConfigManager(
        name="Renewables Generation",
        root_directory=input_folder,
        input_directories=dict(case=case, patterns='patterns'),
        required_input_files=dict(case=['prods_charac.csv', 'params.json'],
                                  patterns=['solar_pattern.npy']),
        output_directory=dispatch_input_folder
    )

    params, prods_charac, solar_pattern = res_config_manager.read_configuration()

    params.update(time_params)
    params = updated_time_parameters_with_timestep(params, params['dt'])

    dispath_config_manager = DispatchConfigManager(
        name="Dispatch",
        root_directory=os.path.join(input_folder, case),
        output_directory=dispatch_output_folder,
        input_directories=dict(params='.', year=os.path.join('dispatch', str(year))),
        required_input_files=dict(params=['params_opf.json'], year=[])
    )
    dispath_config_manager.validate_configuration()
    params_opf = dispath_config_manager.read_configuration()
    dispatcher = ec.init_dispatcher_from_config(params_opf["grid_path"], input_folder)

    ## Launch proper scenarios generation
    for i, seed in enumerate(seeds):
        scenario_name = f'Scenario_{i}'
        scenario_dispatch_input_folder = os.path.join(dispatch_input_folder, scenario_name)

        print("================ Generating "+scenario_name+" ================")
        if 'L' in mode:
            load, load_forecasted = gen_loads.main(scenario_dispatch_input_folder, seed, params, loads_charac, load_weekly_pattern, write_results = True)

        if 'R' in mode:
            prod_solar, prod_solar_forecasted, prod_wind, prod_wind_forecasted = gen_enr.main(scenario_dispatch_input_folder, seed, params, prods_charac, solar_pattern, write_results = True)
        if 'T' in mode:
            input_scenario_folder, output_scneario_folder = du.make_scenario_input_output_directories(
                dispatch_input_folder, dispatch_output_folder, scenario_name)
            prods = pd.concat([prod_solar, prod_wind], axis=1)
            res_names = dict(wind=prod_wind.columns, solar=prod_solar.columns)
            dispatcher.chronix_scenario = ec.ChroniXScenario(load, prods, res_names,
                                                             scenario_name)

            dispatch_results = gen_dispatch.main(dispatcher, input_scenario_folder,
                                                 output_scneario_folder,
                                                 seed, params_opf)
        print('\n')
    return params, loads_charac, prods_charac

