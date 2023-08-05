"""
costs according to supply systems
"""
from __future__ import division

import pandas as pd
from geopandas import GeoDataFrame as gpdf

import cea.config
import cea.inputlocator

__author__ = "Jimeno A. Fonseca"
__copyright__ = "Copyright 2015, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Jimeno A. Fonseca"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Daren Thomas"
__email__ = "cea@arch.ethz.ch"
__status__ = "Production"


def operation_costs(locator, config):
    # get local variables
    demand = pd.read_csv(locator.get_total_demand())
    supply_systems = gpdf.from_file(locator.get_building_supply()).drop('geometry', axis=1)
    data_all_in_one_systems = pd.read_excel(locator.get_database_supply_systems(), sheet_name='ALL_IN_ONE_SYSTEMS')
    factors_heating = data_all_in_one_systems[data_all_in_one_systems['system'].isin(['HEATING', 'NONE'])]
    factors_dhw = data_all_in_one_systems[data_all_in_one_systems['system'].isin(['HEATING', 'NONE'])]
    factors_cooling = data_all_in_one_systems[data_all_in_one_systems['system'].isin(['COOLING', 'NONE'])]
    factors_electricity = data_all_in_one_systems[data_all_in_one_systems['system'].isin(['ELECTRICITY', 'NONE'])]
    factors_resources = pd.read_excel(locator.get_database_supply_systems(), sheet_name='FEEDSTOCKS')

    # local variables
    # calculate the total operational non-renewable primary energy demand and CO2 emissions
    ## create data frame for each type of end use energy containing the type of supply system use, the final energy
    ## demand and the primary energy and emissions factors for each corresponding type of supply system
    heating_costs = factors_heating.merge(factors_resources, left_on='feedstock', right_on='code')[
        ['code_x', 'feedstock', 'Opex_var_buy_USD2015perkWh']]
    cooling_costs = factors_cooling.merge(factors_resources, left_on='feedstock', right_on='code')[
        ['code_x', 'feedstock', 'Opex_var_buy_USD2015perkWh']]
    dhw_costs = factors_dhw.merge(factors_resources, left_on='feedstock', right_on='code')[
        ['code_x', 'feedstock', 'Opex_var_buy_USD2015perkWh']]
    electricity_costs = factors_electricity.merge(factors_resources, left_on='feedstock', right_on='code')[
        ['code_x', 'feedstock', 'Opex_var_buy_USD2015perkWh']]

    heating = supply_systems.merge(demand, on='Name').merge(heating_costs, left_on='type_hs', right_on='code_x')
    dhw = supply_systems.merge(demand, on='Name').merge(dhw_costs, left_on='type_dhw', right_on='code_x')
    cooling = supply_systems.merge(demand, on='Name').merge(cooling_costs, left_on='type_cs', right_on='code_x')
    electricity = supply_systems.merge(demand, on='Name').merge(electricity_costs, left_on='type_el', right_on='code_x')

    fields_to_plot = []
    heating_services = ['DH_hs', 'OIL_hs', 'NG_hs', 'WOOD_hs', 'COAL_hs', 'SOLAR_hs']
    for service in heating_services:
        try:
            fields_to_plot.extend([service + '_cost_yr', service + '_cost_m2yr'])
            # calculate the total and relative costs
            heating[service + '_cost_yr'] = heating[service + '_MWhyr'] * heating['Opex_var_buy_USD2015perkWh'] * 1000
            heating[service + '_cost_m2yr'] = heating[service + '_cost_yr'] / heating['Aocc_m2']
        except KeyError:
            print(heating)
            print(list(heating.columns))
            raise

    # for cooling services
    dhw_services = ['DH_ww', 'OIL_ww', 'NG_ww', 'WOOD_ww', 'COAL_ww', 'SOLAR_ww']
    for service in dhw_services:
        fields_to_plot.extend([service + '_cost_yr', service + '_cost_m2yr'])
        # calculate the total and relative costs
        # calculate the total and relative costs
        dhw[service + '_cost_yr'] = dhw[service + '_MWhyr'] * dhw['Opex_var_buy_USD2015perkWh'] * 1000
        dhw[service + '_cost_m2yr'] = dhw[service + '_cost_yr'] / dhw['Aocc_m2']

    ## calculate the operational primary energy and emissions for cooling services
    cooling_services = ['DC_cs', 'DC_cdata', 'DC_cre']
    for service in cooling_services:
        fields_to_plot.extend([service + '_cost_yr', service + '_cost_m2yr'])
        # change price to that of local electricity mix
        # calculate the total and relative costs
        cooling[service + '_cost_yr'] = cooling[service + '_MWhyr'] * cooling['Opex_var_buy_USD2015perkWh'] * 1000
        cooling[service + '_cost_m2yr'] = cooling[service + '_cost_yr'] / cooling['Aocc_m2']

    ## calculate the operational primary energy and emissions for electrical services
    electrical_services = ['GRID', 'PV']
    for service in electrical_services:
        fields_to_plot.extend([service + '_cost_yr', service + '_cost_m2yr'])
        # calculate the total and relative costs
        electricity[service + '_cost_yr'] = electricity[service + '_MWhyr'] * electricity['Opex_var_buy_USD2015perkWh'] * 1000
        electricity[service + '_cost_m2yr'] = electricity[service + '_cost_yr'] / electricity['Aocc_m2']

    # plot also NFA area and costs
    analysis_fields_costs = ['Opex_a_sys_connected_USD',
                             'Opex_a_sys_disconnected_USD',
                             'Capex_a_sys_disconnected_USD',
                             'Capex_a_sys_connected_USD',
                             ]
    fields_to_plot.extend(['Aocc_m2'])
    fields_to_plot.extend(analysis_fields_costs)

    # create and save results
    result = heating.merge(dhw, on='Name', suffixes=('', '_dhw'))
    result = result.merge(cooling, on='Name', suffixes=('', '_cooling'))
    result = result.merge(electricity, on='Name', suffixes=('', '_ electricity'))

    # add totals:
    result['Opex_a_sys_connected_USD'] = result['GRID_cost_yr'] + \
                                         result['DH_hs_cost_yr'] + \
                                         result['DH_ww_cost_yr'] + \
                                         result['DC_cdata_cost_yr'] + \
                                         result['DC_cs_cost_yr'] + \
                                         result['DC_cre_cost_yr']

    result['Opex_a_sys_disconnected_USD'] = result['OIL_hs_cost_yr'] + \
                                            result['NG_hs_cost_yr'] + \
                                            result['WOOD_hs_cost_yr'] + \
                                            result['COAL_hs_cost_yr'] + \
                                            result['SOLAR_hs_cost_yr'] + \
                                            result['PV_cost_yr'] + \
                                            result['OIL_ww_cost_yr'] + \
                                            result['NG_ww_cost_yr'] + \
                                            result['WOOD_ww_cost_yr'] + \
                                            result['COAL_ww_cost_yr'] + \
                                            result['SOLAR_ww_cost_yr']

    #TODO: craete a model to calculate the capital costs
    result['Capex_a_sys_connected_USD'] = 0.0
    result['Capex_a_sys_disconnected_USD'] = 0.0

    result[['Name'] + fields_to_plot].to_csv(
        locator.get_costs_operation_file(), index=False, float_format='%.2f')


def main(config):
    locator = cea.inputlocator.InputLocator(scenario=config.scenario)

    print('Running operation-costs with scenario = %s' % config.scenario)

    operation_costs(locator=locator, config=config)


if __name__ == '__main__':
    main(cea.config.Configuration())
