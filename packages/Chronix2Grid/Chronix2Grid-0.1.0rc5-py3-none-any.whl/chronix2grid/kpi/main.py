# Python built-in modules
import warnings
import os
import json

# Chronix2grid modules
from .preprocessing.pivot_KPI import pivot_format
from .deterministic.kpis import EconomicDispatchValidator


def main(kpi_input_folder, generation_input_folder, generation_output_folder, images_repo, year, case, n_scenarios, wind_solar_only, params,
         loads_charac, prods_charac):
    """
        This is the main function for KPI computation. It formats synthetic and reference chronics and then computes KPIs on it with 2 modes (wind solar and load only or full energy mix). It saves plots in png and html files. It writes a json output

        Parameters
        ----------
        kpi_input_folder (str): path to folder of kpi inputs, which contains paramsKPI.json and benchmark folders. paramsKPI.json tells which benchmark to read as reference
        generation_input_folder (str): path to the input folder of generation module (to read chronics before dispatch)
        generation_output_folder (str): path to the output folder of generation module (to read chronics after dispatch)
        images_repo (str): path to the images folder in which KPI plots will be saved
        year (int): year in which chronics have been generated
        case (str): identify the studied case for chronics generation, such as l2rpn_118
        n_scenario (int): number of scenarios to consider (KPIs are computed for each scenario succesively)
        wind_solar_only (boolean): True if the generated chronics contain only wind, solar and load chronics, False otherwise
        params (dict): configuration params computed from params.json, such as timestep or mesh characteristics
        loads_charac (pandas.DataFrame): characteristics of loads node such as Pmax, type of demand and region
        prods_charac (pandas.DataFrame): characteristics of generators such as Pmax, carrier and region

    """


    print('=====================================================================================================================================')
    print('================================================= KPI GENERATION  ===================================================================')
    print('=====================================================================================================================================')

    warnings.filterwarnings("ignore")


    # Create single zone if no zone is given
    if 'zone' not in prods_charac.columns:
        prods_charac['zone'] = 'R1'
        loads_charac['zone'] = 'R1'

    ## Format and compute KPI for each scenario
    for scenario_num in range(n_scenarios):
        print('Scenario '+str(scenario_num)+'...')

        # Return Warning if KPIs are not computed on full year. Yet, the computation will work
        if params['weeks'] != 52:
            print('Warning: KPI are incomplete. Computation has been made on '+str(params['weeks'])+' weeks, but are meant to be computed on 52 weeks')

        # Read reference and synthetic chronics, but also KPI configuration, in pivot format. 2 modes: with or without full dispatch
        if wind_solar_only:
            # Get reference and synthetic dispatch and loads
            ref_dispatch, ref_consumption, syn_dispatch, syn_consumption, monthly_pattern, hours = pivot_format(generation_input_folder,
                                                                                                            kpi_input_folder,
                                                                                                            year,
                                                                                                            scenario_num,
                                                                                                            prods_charac,
                                                                                                            loads_charac,
                                                                                                            wind_solar_only,
                                                                                                            params, case)
            ref_prices = None
            prices = None
        else:
            # Get reference and synthetic dispatch and loads
            ref_dispatch, ref_consumption, syn_dispatch, syn_consumption, monthly_pattern, hours, ref_prices, prices = pivot_format(
                                                                                                generation_output_folder,
                                                                                                kpi_input_folder,
                                                                                                year,
                                                                                                scenario_num,
                                                                                                prods_charac,
                                                                                                loads_charac,
                                                                                                wind_solar_only,
                                                                                                params, case)


        ## Start and Run Economic dispatch validator
        # -- + -- + -- + -- + -- + -- + --
        print ('(1) Computing KPI\'s...')
        dispatch_validator = EconomicDispatchValidator(ref_consumption,
                                                       syn_consumption,
                                                       ref_dispatch,
                                                       syn_dispatch,
                                                       year,
                                                       scenario_num,
                                                       images_repo,
                                                       prods_charac=prods_charac,
                                                       loads_charac=loads_charac,
                                                       ref_prices=ref_prices,
                                                       syn_prices=prices)


        # Compute dispatch temporal view
        if wind_solar_only:
            max_col = 1
        else:
            max_col = 2
        dispatch_validator.plot_carriers_pw(curve='reference', stacked=True, max_col_splot=max_col, save_html=True,
                                            wind_solar_only=wind_solar_only)
        dispatch_validator.plot_carriers_pw(curve='synthetic', stacked=True, max_col_splot=max_col, save_html=True,
                                            wind_solar_only=wind_solar_only)

        # Get Load KPI
        dispatch_validator.load_kpi()

        # Get Wind KPI
        dispatch_validator.wind_kpi()

        # Get Solar KPI
        dispatch_validator.solar_kpi(monthly_pattern=monthly_pattern, hours=hours)

        # Wind - Solar KPI
        dispatch_validator.wind_load_kpi()

        # These KPI only if dispatch has been made
        if not wind_solar_only:
            # Get Energy Mix
            dispatch_validator.energy_mix()

            # Get Hydro KPI
            dispatch_validator.hydro_kpi()

            # Get Nuclear KPI
            dispatch_validator.nuclear_kpi()

            # Get Thermal KPI
            dispatch_validator.thermal_kpi()
            dispatch_validator.thermal_load_kpi()


        # Write json output file
        # -- + -- + -- + -- + --
        print ('(2) Generating json output file...')

        kpi_output_folder = os.path.join(kpi_input_folder, os.pardir, 'output', str(year))
        if not os.path.exists(kpi_output_folder):
            os.makedirs(kpi_output_folder)
        kpi_output_folder = os.path.join(kpi_output_folder,'Scenario_' + str(scenario_num))
        if not os.path.exists(kpi_output_folder):
            os.makedirs(kpi_output_folder)

        with open(os.path.join(kpi_output_folder,'ec_validator_output.json'), 'w') as json_f:
            json.dump(dispatch_validator.output, json_f)

        print ('-Done-\n')