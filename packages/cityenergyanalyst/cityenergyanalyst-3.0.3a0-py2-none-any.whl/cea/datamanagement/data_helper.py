"""
building properties algorithm
"""

# HISTORY:
# J. A. Fonseca  script development          22.03.15

from __future__ import absolute_import
from __future__ import division

import warnings

import numpy as np
import pandas as pd

import cea.config
import cea.inputlocator
from cea import InvalidOccupancyNameException
from cea.datamanagement.schedule_helper import calc_mixed_schedule
from cea.datamanagement.databases_verification import COLUMNS_ZONE_OCCUPANCY
from cea.utilities.dbf import dbf_to_dataframe, dataframe_to_dbf


__author__ = "Jimeno A. Fonseca"
__copyright__ = "Copyright 2015, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Jimeno A. Fonseca", "Daren Thomas", "Martin Mosteiro"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Daren Thomas"
__email__ = "cea@arch.ethz.ch"
__status__ = "Production"


def get_technology_related_databases(locator, region):
    technology_database_template = locator.get_technology_template_for_region(region)
    print("Copying technology databases from {source}".format(source=technology_database_template))
    output_directory = locator.get_databases_folder()

    from distutils.dir_util import copy_tree
    copy_tree(technology_database_template, output_directory)


def data_helper(locator, region, overwrite_technology_folder,
                update_architecture_dbf, update_HVAC_systems_dbf, update_indoor_comfort_dbf,
                update_internal_loads_dbf, update_supply_systems_dbf,
                update_schedule_operation_cea, buildings):
    """
    algorithm to query building properties from statistical database
    Archetypes_HVAC_properties.csv. for more info check the integrated demand
    model of Fonseca et al. 2015. Appl. energy.

    :param InputLocator locator: an InputLocator instance set to the scenario to work on
    :param boolean update_architecture_dbf: if True, update the construction and architecture properties.
    :param boolean update_indoor_comfort_dbf: if True, get properties about thermal comfort.
    :param boolean update_HVAC_systems_dbf: if True, get properties about types of HVAC systems, otherwise False.
    :param boolean update_internal_loads_dbf: if True, get properties about internal loads, otherwise False.

    The following files are created by this script, depending on which flags were set:

    - building_HVAC: .dbf
        describes the queried properties of HVAC systems.

    - architecture.dbf
        describes the queried properties of architectural features

    - building_thermal: .shp
        describes the queried thermal properties of buildings

    - indoor_comfort.shp
        describes the queried thermal properties of buildings
    """
    # get technology database
    if overwrite_technology_folder:
        # copy all the region-specific archetypes to the scenario's technology folder
        get_technology_related_databases(locator, region)

    # get occupancy and age files
    building_occupancy_df = dbf_to_dataframe(locator.get_building_occupancy())
    building_age_df = dbf_to_dataframe(locator.get_building_age())

    # validate list of uses in case study
    list_uses = get_list_of_uses_in_case_study(building_occupancy_df)

    # get occupant densities from archetypes schedules
    occupant_densities = {}
    occ_densities = pd.read_excel(locator.get_archetypes_properties(), 'INTERNAL_LOADS').set_index('Code')
    for use in list_uses:
        if occ_densities.loc[use, 'Occ_m2pax'] > 0.0:
            occupant_densities[use] = 1 / occ_densities.loc[use, 'Occ_m2pax']
        else:
            occupant_densities[use] = 0.0

    # prepare shapefile to store results (a shapefile with only names of buildings
    names_df = building_age_df[['Name']]

    # define main use:
    building_occupancy_df['mainuse'] = calc_mainuse(building_occupancy_df, list_uses)

    # dataframe with joined data for categories
    categories_df = building_occupancy_df.merge(building_age_df, on='Name')

    # get properties about the construction and architecture
    if update_architecture_dbf:
        architecture_DB = pd.read_excel(locator.get_archetypes_properties(), 'ARCHITECTURE')
        architecture_DB['Code'] = architecture_DB.apply(lambda x: calc_code(x['building_use'], x['year_start'],
                                                                            x['year_end'], x['standard']), axis=1)
        categories_df['cat_built'] = calc_category(architecture_DB, categories_df, 'built', 'C')
        retrofit_category = ['envelope', 'roof', 'windows']
        for category in retrofit_category:
            categories_df['cat_' + category] = calc_category(architecture_DB, categories_df, category, 'R')

        prop_architecture_df = get_prop_architecture(categories_df, architecture_DB, list_uses)

        # write to dbf file
        prop_architecture_df_merged = names_df.merge(prop_architecture_df, on="Name")

        fields = ['Name',
                  'Hs_ag',
                  'Hs_bg',
                  'Ns',
                  'Es',
                  'void_deck',
                  'wwr_north',
                  'wwr_west',
                  'wwr_east',
                  'wwr_south',
                  'type_cons',
                  'type_leak',
                  'type_roof',
                  'type_wall',
                  'type_win',
                  'type_shade']

        dataframe_to_dbf(prop_architecture_df_merged[fields], locator.get_building_architecture())

    # get properties about types of HVAC systems
    if update_HVAC_systems_dbf:
        construction_properties_hvac = pd.read_excel(locator.get_archetypes_properties(), 'HVAC')
        construction_properties_hvac['Code'] = construction_properties_hvac.apply(
            lambda x: calc_code(x['building_use'], x['year_start'],
                                x['year_end'], x['standard']), axis=1)

        categories_df['cat_HVAC'] = calc_category(construction_properties_hvac, categories_df, 'HVAC', 'R')

        # define HVAC systems types
        prop_HVAC_df = categories_df.merge(construction_properties_hvac, left_on='cat_HVAC', right_on='Code')

        # write to shapefile
        fields = ['Name',
                  'type_cs',
                  'type_hs',
                  'type_dhw',
                  'type_ctrl',
                  'type_vent',
                  'heat_starts',
                  'heat_ends',
                  'cool_starts',
                  'cool_ends']
        prop_HVAC_df_merged = names_df.merge(prop_HVAC_df, on="Name")
        dataframe_to_dbf(prop_HVAC_df_merged[fields], locator.get_building_air_conditioning())

    if update_indoor_comfort_dbf:
        comfort_DB = pd.read_excel(locator.get_archetypes_properties(), 'INDOOR_COMFORT')

        # define comfort
        prop_comfort_df = categories_df.merge(comfort_DB, left_on='mainuse', right_on='Code')

        # write to shapefile
        fields = ['Name',
                  'Tcs_set_C',
                  'Ths_set_C',
                  'Tcs_setb_C',
                  'Ths_setb_C',
                  'Ve_lpspax',
                  'RH_min_pc',
                  'RH_max_pc']
        prop_comfort_df_merged = names_df.merge(prop_comfort_df, on="Name")
        prop_comfort_df_merged = calculate_average_multiuse(fields,
                                                            prop_comfort_df_merged,
                                                            occupant_densities,
                                                            list_uses,
                                                            comfort_DB)

        dataframe_to_dbf(prop_comfort_df_merged[fields], locator.get_building_comfort())

    if update_internal_loads_dbf:
        internal_DB = pd.read_excel(locator.get_archetypes_properties(), 'INTERNAL_LOADS')

        # define comfort
        prop_internal_df = categories_df.merge(internal_DB, left_on='mainuse', right_on='Code')

        # write to shapefile
        fields = ['Name',
                  'Occ_m2pax',
                  'Qs_Wpax',
                  'X_ghpax',
                  'Ea_Wm2',
                  'El_Wm2',
                  'Ed_Wm2',
                  'Qcre_Wm2',
                  'Vww_lpdpax',
                  'Vw_lpdpax',
                  'Qhpro_Wm2',
                  'Qcpro_Wm2',
                  'Epro_Wm2']
        prop_internal_df_merged = names_df.merge(prop_internal_df, on="Name")
        prop_internal_df_merged = calculate_average_multiuse(fields,
                                                             prop_internal_df_merged,
                                                             occupant_densities,
                                                             list_uses,
                                                             internal_DB)

        dataframe_to_dbf(prop_internal_df_merged[fields], locator.get_building_internal())

    if update_schedule_operation_cea:
        if buildings == []:
            buildings = locator.get_zone_building_names()
        calc_mixed_schedule(locator, building_occupancy_df, buildings)

    if update_supply_systems_dbf:
        supply_DB = pd.read_excel(locator.get_archetypes_properties(), 'SUPPLY')
        supply_DB['Code'] = supply_DB.apply(lambda x: calc_code(x['building_use'], x['year_start'],
                                                                x['year_end'], x['standard']), axis=1)

        categories_df['cat_supply'] = calc_category(supply_DB, categories_df, 'HVAC', 'R')

        # define HVAC systems types
        prop_supply_df = categories_df.merge(supply_DB, left_on='cat_supply', right_on='Code')

        # write to shapefile
        prop_supply_df_merged = names_df.merge(prop_supply_df, on="Name")
        fields = ['Name',
                  'type_cs',
                  'type_hs',
                  'type_dhw',
                  'type_el']
        dataframe_to_dbf(prop_supply_df_merged[fields], locator.get_building_supply())


def get_list_of_uses_in_case_study(building_occupancy_df):
    """
    validates lists of uses in case study.
    refactored from data_helper function

    :param building_occupancy_df: dataframe of occupancy.dbf input (can be read in data-helper or in building-properties)
    :type building_occupancy_df: pandas.DataFrame
    :return: list of uses in case study
    :rtype: pandas.DataFrame.Index
    """
    columns = building_occupancy_df.columns
    # validate list of uses
    list_uses = []
    for name in columns:
        if name in COLUMNS_ZONE_OCCUPANCY:
            if building_occupancy_df[name].sum() > 0.0:
                list_uses.append(name)  # append valid uses
        elif name in {'Name', 'REFERENCE'}:
            pass  # do nothing with 'Name' and 'Reference'
        else:
            raise InvalidOccupancyNameException(
                'occupancy.dbf has use "{}". This use is not part of the database. Change occupancy.dbf'
                ' or customize archetypes database AND databases_verification.py.'.format(name))
    return list_uses


def calc_code(code1, code2, code3, code4):
    return str(code1) + str(code2) + str(code3) + str(code4)


def calc_mainuse(uses_df, uses):
    """
    Calculate a building's main use
    :param uses_df: DataFrame containing the share of each building that corresponds to each occupancy type
    :type uses_df: DataFrame
    :param uses: list of building uses actually available in the area
    :type uses: list

    :return mainuse: array containing each building's main occupancy
    :rtype mainuse: ndarray

    """

    # print a warning if there are equal shares of more than one "main" use
    # check if 'Name' is already the index, this is necessary because the function is used in data-helper
    #  and in building properties
    if uses_df.index.name not in ['Name']:
        # this is the behavior in data-helper
        indexed_df = uses_df.set_index('Name')
    else:
        # this is the behavior in building-properties
        indexed_df = uses_df.copy()
        uses_df = uses_df.reset_index()

    for building in indexed_df.index:
        mainuses = [use for use in uses if
                    (indexed_df.loc[building, use] == indexed_df.max(axis=1)[building]) and (use != 'PARKING')]
        if len(mainuses) > 1:
            print '%s has equal share of %s; the construction properties and systems for %s will be used.' % (
                building, ' and '.join(mainuses), mainuses[0])

    # get array of main use for each building
    databaseclean = uses_df[uses].transpose()
    array_max = np.array(databaseclean[databaseclean[:] > 0].idxmax(skipna=True), dtype='S10')
    for i in range(len(array_max)):
        if databaseclean[i][array_max[i]] != 1:
            databaseclean[i][array_max[i]] = 0
    array_second = np.array(databaseclean[databaseclean[:] > 0].idxmax(skipna=True), dtype='S10')
    mainuse = np.array(map(calc_comparison, array_second, array_max))

    return mainuse


def calc_comparison(array_second, array_max):
    if array_max == 'PARKING':
        if array_second != 'PARKING':
            array_max = array_second
    return array_max


def calc_category(archetype_DB, age, field, type):
    category = []
    for row in age.index:
        if age.loc[row, field] > age.loc[row, 'built']:
            try:
                category.append(archetype_DB[(archetype_DB['year_start'] <= age.loc[row, field]) & \
                                             (archetype_DB['year_end'] >= age.loc[row, field]) & \
                                             (archetype_DB['building_use'] == age.loc[row, 'mainuse']) & \
                                             (archetype_DB['standard'] == type)].Code.values[0])
            except IndexError:
                # raise warnings for e.g. using CH case study with SG construction
                warnings.warn(
                    'Specified building database does not contain renovated building properties. Buildings are treated as new construction.')
                category.append(archetype_DB[(archetype_DB['year_start'] <= age.loc[row, field]) & \
                                             (archetype_DB['year_end'] >= age.loc[row, field]) & \
                                             (archetype_DB['building_use'] == age.loc[row, 'mainuse']) & \
                                             (archetype_DB['standard'] == 'C')].Code.values[0])
        else:
            category.append(archetype_DB[(archetype_DB['year_start'] <= age.loc[row, 'built']) & \
                                         (archetype_DB['year_end'] >= age.loc[row, 'built']) & \
                                         (archetype_DB['building_use'] == age.loc[row, 'mainuse']) & \
                                         (archetype_DB['standard'] == 'C')].Code.values[0])
        if field != 'built':
            if 0 < age.loc[row, field] < age.loc[row, 'built']:
                print('Incorrect %s renovation year in building %s: renovation year is lower than building age' %
                      (field, age['Name'][row]))
            if age.loc[row, field] == age.loc[row, 'built']:
                print('Incorrect %s renovation year in building %s: if building is not renovated, the year needs to be '
                      'set to 0' % (field, age['Name'][row]))

    return category


def correct_archetype_areas(prop_architecture_df, architecture_DB, list_uses):
    """
    Corrects the heated area 'Hs_ag' and 'Hs_bg' for buildings with multiple uses.

    :var prop_architecture_df: DataFrame containing each building's occupancy, construction and renovation data as
        well as the architectural properties obtained from the archetypes.
    :type prop_architecture_df: DataFrame
    :var architecture_DB: architecture database for each archetype
    :type architecture_DB: DataFrame
    :var list_uses: list of all occupancy types in the project
    :type list_uses: list[str]

    :return Hs_ag_list, Hs_bg_list, Ns_list, Es_list: the corrected values for 'Hs_ag', 'Hs_bg', 'Ns' and 'Es' for each
    building
    :type Hs_ag_list, Hs_bg_list, Ns_list, Es_list:: list[float]
    """

    indexed_DB = architecture_DB.set_index('Code')

    # weighted average of values
    def calc_average(last, current, share_of_use):
        return last + current * share_of_use

    Hs_ag_list = []
    Hs_bg_list = []
    Ns_list = []
    Es_list = []
    for building in prop_architecture_df.index:
        Hs_ag = 0.0
        Hs_bg = 0.0
        Ns = 0.0
        Es = 0.0
        for use in list_uses:
            # if the use is present in the building, find the building archetype properties for that use
            if prop_architecture_df[use][building] > 0.0:
                # get archetype code for the current occupancy type
                current_use_code = use + str(prop_architecture_df['year_start'][building]) + \
                                   str(prop_architecture_df['year_end'][building]) + \
                                   str(prop_architecture_df['standard'][building])
                # recalculate heated floor area as an average of the archetype value for each occupancy type in the
                # building
                Hs_ag = calc_average(Hs_ag, indexed_DB['Hs_ag'][current_use_code], prop_architecture_df[use][building])
                Hs_bg = calc_average(Hs_bg, indexed_DB['Hs_bg'][current_use_code], prop_architecture_df[use][building])
                Ns = calc_average(Ns, indexed_DB['Ns'][current_use_code], prop_architecture_df[use][building])
                Es = calc_average(Es, indexed_DB['Es'][current_use_code], prop_architecture_df[use][building])
        Hs_ag_list.append(Hs_ag)
        Hs_bg_list.append(Hs_bg)
        Ns_list.append(Ns)
        Es_list.append(Es)

    return Hs_ag_list, Hs_bg_list, Ns_list, Es_list


def get_prop_architecture(categories_df, architecture_DB, list_uses):
    """
    This function obtains every building's architectural properties based on the construction and renovation years.

    :param categories_df: DataFrame containing each building's construction and renovation categories for each building
        component based on the construction and renovation years
    :type categories_df: DataFrame
    :param architecture_DB: DataFrame containing the archetypal architectural properties for each use type, construction
        and renovation year
    :type categories_df: DataFrame
    :return prop_architecture_df: DataFrame containing the architectural properties of each building in the area
    :rtype prop_architecture_df: DataFrame
    """

    # create databases from construction and renovation archetypes
    construction_DB = architecture_DB.drop(['type_leak', 'type_wall', 'type_roof', 'type_shade', 'type_win'], axis=1)
    envelope_DB = architecture_DB[['Code', 'type_leak', 'type_wall']].copy()
    roof_DB = architecture_DB[['Code', 'type_roof']].copy()
    window_DB = architecture_DB[['Code', 'type_win', 'type_shade']].copy()

    # create prop_architecture_df based on the construction categories and archetype architecture database
    prop_architecture_df = categories_df.merge(construction_DB, left_on='cat_built', right_on='Code').drop('Code',
                                                                                                           axis=1)
    # get envelope properties based on the envelope renovation year
    prop_architecture_df = prop_architecture_df.merge(envelope_DB, left_on='cat_envelope', right_on='Code').drop('Code',
                                                                                                                 axis=1)
    # get roof properties based on the roof renovation year
    prop_architecture_df = prop_architecture_df.merge(roof_DB, left_on='cat_roof', right_on='Code').drop('Code', axis=1)
    # get window properties based on the window renovation year
    prop_architecture_df = prop_architecture_df.merge(window_DB, left_on='cat_windows', right_on='Code').drop('Code',
                                                                                                              axis=1)

    # adjust share of floor space that is heated for multiuse buildings
    prop_architecture_df['Hs_ag'], prop_architecture_df['Hs_bg'], prop_architecture_df['Ns'],\
        prop_architecture_df['Es'] = correct_archetype_areas(prop_architecture_df, architecture_DB, list_uses)

    return prop_architecture_df


def calculate_average_multiuse(fields, properties_df, occupant_densities, list_uses, properties_DB):
    """
    This script calculates the average internal loads and ventilation properties for multiuse buildings.

    :param properties_df: DataFrame containing the building's occupancy type and the corresponding indoor comfort
        properties or internal loads.
    :type properties_df: DataFrame
    :param occupant_densities: DataFrame containing the number of people per square meter for each occupancy type based
        on the archetypes
    :type occupant_densities: Dict
    :param list_uses: list of uses in the project
    :type list_uses: list[str]
    :param properties_DB: DataFrame containing each occupancy type's indoor comfort properties or internal loads based
        on the corresponding archetypes
    :type properties_DB: DataFrame

    :return properties_df: the same DataFrame as the input parameter, but with the updated properties for multiuse
        buildings
    """
    properties_DB = properties_DB.set_index('Code')
    for column in fields:
        if column in ['Ve_lpspax', 'Qs_Wpax', 'X_ghpax', 'Vww_lpdpax', 'Vw_lpdpax']:
            # some properties are imported from the Excel files as int instead of float
            properties_df[column] = properties_df[column].astype(float)
            for building in properties_df.index:
                column_total = 0
                people_total = 0
                for use in list_uses:
                    if use in properties_df.columns:
                        column_total += (properties_df[use][building]
                                         * occupant_densities[use]
                                         * properties_DB[column][use])
                        people_total += properties_df[use][building] * occupant_densities[use]
                if people_total > 0.0:
                    properties_df.loc[building, column] = column_total / people_total
                else:
                    properties_df.loc[building, column] = 0

        elif column in ['Ea_Wm2', 'El_Wm2', 'Epro_Wm2', 'Qcre_Wm2', 'Ed_Wm2', 'Qhpro_Wm2', 'Qcpro_Wm2', 'Occ_m2pax']:
            for building in properties_df.index:
                average = 0.0
                for use in list_uses:
                    average += properties_df[use][building] * properties_DB[column][use]
                properties_df.loc[building, column] = average

    return properties_df


def main(config):
    """
    Run the properties script with input from the reference case and compare the results. This ensures that changes
    made to this script (e.g. refactorings) do not stop the script from working and also that the results stay the same.
    """

    print('Running data-helper with scenario = %s' % config.scenario)
    print('Running data-helper with archetypes = %s' % config.data_helper.databases)

    update_architecture_dbf = 'architecture' in config.data_helper.databases
    update_technical_systems_dbf = 'HVAC' in config.data_helper.databases
    update_indoor_comfort_dbf = 'comfort' in config.data_helper.databases
    update_internal_loads_dbf = 'internal-loads' in config.data_helper.databases
    update_supply_systems_dbf = 'supply' in config.data_helper.databases
    update_schedule_operation_cea = 'schedules' in config.data_helper.databases

    overwrite_technology_folder = config.data_helper.overwrite_technology_folder
    buildings = config.data_helper.buildings

    locator = cea.inputlocator.InputLocator(config.scenario)

    data_helper(locator=locator, region=config.data_helper.region,
                overwrite_technology_folder=overwrite_technology_folder,
                update_architecture_dbf=update_architecture_dbf,
                update_HVAC_systems_dbf=update_technical_systems_dbf,
                update_indoor_comfort_dbf=update_indoor_comfort_dbf,
                update_internal_loads_dbf=update_internal_loads_dbf,
                update_supply_systems_dbf=update_supply_systems_dbf,
                update_schedule_operation_cea=update_schedule_operation_cea,
                buildings=buildings)


if __name__ == '__main__':
    main(cea.config.Configuration())
