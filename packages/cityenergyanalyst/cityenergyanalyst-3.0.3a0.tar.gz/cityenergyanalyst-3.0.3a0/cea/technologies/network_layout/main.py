import os

import cea.config
import cea.inputlocator
from cea.technologies.network_layout.connectivity_potential import calc_connectivity_network
from cea.technologies.network_layout.steiner_spanning_tree import calc_steiner_spanning_tree
from cea.technologies.network_layout.substations_location import calc_substation_location

__author__ = "Jimeno A. Fonseca"
__copyright__ = "Copyright 2017, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Jimeno A. Fonseca"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Daren Thomas"
__email__ = "cea@arch.ethz.ch"
__status__ = "Production"


def layout_network(network_layout, locator, plant_building_names=None, output_name_network="", optimization_flag=False):
    # Local variables
    if plant_building_names is None:
        plant_building_names = []
    weight_field = 'Shape_Leng'
    total_demand_location = locator.get_total_demand()
    path_potential_network = locator.get_temporary_file("potential_network.shp")  # shapefile, location of output.

    type_mat_default = network_layout.type_mat
    pipe_diameter_default = network_layout.pipe_diameter
    type_network = network_layout.network_type
    create_plant = network_layout.create_plant
    connected_buildings = network_layout.connected_buildings
    consider_only_buildings_with_demand = network_layout.consider_only_buildings_with_demand
    allow_looped_networks = network_layout.allow_looped_networks

    path_streets_shp = locator.get_street_network()  # shapefile with the stations
    input_buildings_shp = locator.get_zone_geometry()
    output_substations_shp = locator.get_temporary_file("nodes_buildings.shp")
    # Calculate points where the substations will be located
    calc_substation_location(input_buildings_shp, output_substations_shp, connected_buildings,
                             consider_only_buildings_with_demand, type_network, total_demand_location)

    # Calculate potential network
    crs_projected = calc_connectivity_network(path_streets_shp, output_substations_shp,
                                              path_potential_network)

    # calc minimum spanning tree and save results to disk
    output_edges = locator.get_network_layout_edges_shapefile(type_network, output_name_network)
    output_nodes = locator.get_network_layout_nodes_shapefile(type_network, output_name_network)
    output_network_folder = locator.get_input_network_folder(type_network, output_name_network)

    if connected_buildings != []:
        building_names = locator.get_zone_building_names()
        disconnected_building_names = [x for x in connected_buildings if x not in building_names]
    else:
        # if connected_buildings is left blank, we assume all buildings are connected (no disconnected buildings)
        disconnected_building_names = []
    calc_steiner_spanning_tree(crs_projected, path_potential_network, output_network_folder, output_substations_shp,
                               output_edges, output_nodes, weight_field, type_mat_default, pipe_diameter_default,
                               type_network, total_demand_location, create_plant,
                               allow_looped_networks, optimization_flag, plant_building_names, disconnected_building_names)


class NetworkLayout(object):
    """Capture network layout information"""
    def __init__(self, network_layout=None):
        self.network_type = "DC"
        self.connected_buildings = []
        self.disconnected_buildings = []
        self.pipe_diameter = 150
        self.type_mat = "T1"
        self.create_plant = True
        self.allow_looped_networks = False
        self.consider_only_buildings_with_demand = False

        attributes = ["network_type", "pipe_diameter", "type_mat", "create_plant", "allow_looped_networks",
                      "consider_only_buildings_with_demand", "connected_buildings", "disconnected_buildings"]
        for attr in attributes:
            # copy any matching attributes in network_layout (because it could be an instance of NetworkInfo)
            if hasattr(network_layout, attr):
                setattr(self, attr, getattr(network_layout, attr))


def main(config):
    assert os.path.exists(config.scenario), 'Scenario not found: %s' % config.scenario
    locator = cea.inputlocator.InputLocator(scenario=config.scenario)
    network_layout = NetworkLayout(network_layout=config.network_layout)
    layout_network(network_layout, locator)


if __name__ == '__main__':
    main(cea.config.Configuration())
