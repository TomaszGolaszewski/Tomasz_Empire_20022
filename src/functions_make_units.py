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
    for i, place in enumerate(map.places_to_start):     
        if place[0] > map.map_sprite_width_world/2: angle = math.pi
        else: angle = 0   
        dict_with_units[id] = Commander(id, place, angle, i+1, i+1)
        id += 1
        dict_with_units[id] = Super_space_marine(id, [place[0] + 90, place[1]], angle, i+1, i+1)
        id += 1
    # dict_with_units[id] = Aircraft_carrier(id, [4000, 1000], 0, 3, 3)
    # id += 1
    # dict_with_units[id] = Battleship(id, [4000, 1200], 0, 3, 3)
    # id += 1
    # dict_with_units[id] = Battleship(id, [4000, 1400], 0, 3, 3)
    # id += 1
    # dict_with_units[id] = Fighter(id, [4000, 200], 0, 3, 3)
    # id += 1
    # dict_with_units[id] = Fighter(id, [4000, 300], 0, 3, 3)
    # id += 1
    # dict_with_units[id] = Fighter(id, [4000, 400], 0, 3, 3)
    # id += 1
    # dict_with_units[id] = Fighter(id, [4000, 500], 0, 3, 3)
    # id += 1
    dict_with_game_state["lowest_free_id"] = id

def make_more_units_for_title_scene(map, dict_with_game_state, dict_with_units):
# make units for animation on Title Scene
    id = dict_with_game_state["lowest_free_id"]
    dict_with_units[id] = Space_marine(id, [-50, random.randint(50, WIN_HEIGHT-50)], 0, 1, 1) # blue
    id += 1
    dict_with_units[id] = Space_marine(id, [WIN_WIDTH+50, random.randint(50, WIN_HEIGHT-50)], 0, 3, 3) # red
    id += 1
    dict_with_game_state["lowest_free_id"] = id