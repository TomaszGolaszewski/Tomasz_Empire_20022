import math

from classes_units import *
from classes_buildings import *


def make_naval_factories(map, dict_with_game_state, dict_with_units):
# make naval factories
    id = dict_with_game_state["lowest_free_id"]
    for place in map.places_for_naval_factories:    
        # make factory      
        dict_with_units[id] = Navy_factory(id, place, 0, 0, 0)
        # set default target for newly produced units (oriented to the center of the map)
        place_but_in_ids = map.world2id(place)
        if place_but_in_ids[0] > map.map_width/2: angle = math.pi
        else: angle = 0
        # if the center of the map is not water, turn the angle
        if map.BOARD[map.map_height//2][map.map_width//2].type not in ["water", "shallow"]:
            angle += math.pi
        dict_with_units[id].target_for_units = [move_point(place, 200, angle)]
        # increase id
        id += 1
    dict_with_game_state["lowest_free_id"] = id

def make_land_factories(map, dict_with_game_state, dict_with_units):
# make land factories
    id = dict_with_game_state["lowest_free_id"]
    for place in map.places_for_land_factories:      
        # make factory  
        dict_with_units[id] = Land_factory(id, place, 0, 0, 0)
        # set default target for newly produced units (oriented to the center of the map)
        place_but_in_ids = map.world2id(place)
        if place_but_in_ids[0] > map.map_width/2: angle = math.pi
        else: angle = 0
        dict_with_units[id].target_for_units = [move_point(place, 200, angle)]
        # increase id
        id += 1
    dict_with_game_state["lowest_free_id"] = id

def make_generators(map, dict_with_game_state, dict_with_units):
# make generators
    id = dict_with_game_state["lowest_free_id"]
    for place in map.places_for_generators:        
        dict_with_units[id] = Generator(id, place, 0, 0, 0)
        id += 1
    dict_with_game_state["lowest_free_id"] = id

def make_start_units(map, dict_with_game_state, dict_with_units):
# make start units
    id = dict_with_game_state["lowest_free_id"]
    dict_with_units[id] = Super_space_marine(id, [1000, 1000], 0, 1, 1) # blue
    id += 1
    dict_with_units[id] = Super_space_marine(id, [2500, 1000], 0, 3, 3) # red
    id += 1
    dict_with_units[id] = Super_space_marine(id, [2500, 2500], 0, 2, 2) # green
    id += 1
    dict_with_units[id] = Super_space_marine(id, [1000, 2500], 0, 4, 4) # yellow
    id += 1
    dict_with_game_state["lowest_free_id"] = id