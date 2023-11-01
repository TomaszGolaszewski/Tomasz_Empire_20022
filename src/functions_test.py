import math

from classes_units import *
from classes_buildings import *


# ============== debug functions ============


def print_infos_about_view_position(offset_x, offset_y, scale):
# write information about view position in the console
    print("HORIZ:", end=" ")
    print(offset_x, end="\t")
    print("VERT:", end=" ")
    print(offset_y, end="\t")
    print("SCALE:", end=" ")
    print(scale)


def print_infos_about_amount_of_objects(dict_with_game_state, dict_with_units, list_with_bullets, list_with_windows):
# write information about amount of game objects in the console  

    # print amount of bullets objects   
    print("BULLETS:", end=" ")
    print(len(list_with_bullets), end="\t")

    # print amount of units objects 
    print("UNITS:", end=" ")
    print(len(dict_with_units), end="\t")

    # print amount of on-screen units objects 
    unit_count = 0
    for unit_id in dict_with_units:
        if dict_with_units[unit_id].is_on_screen: unit_count += 1
    print("UNITS ON SCREEN:", end=" ")
    print(unit_count, end="\t")

    # print amount of selected units objects
    unit_count = 0
    for unit_id in dict_with_units:
        if dict_with_units[unit_id].is_selected: unit_count += 1
    print("SELECTED UNITS:", end=" ")
    print(unit_count)

    # print infos about ui windows
    print("WINDOWS:", end=" ")
    print(len(list_with_windows), end="\t")

    # other infos
    print("MAX_ID:", end=" ")
    print(dict_with_game_state["lowest_free_id"], end="\t")
    print()


def print_infos_about_players(dict_with_game_state):
# write information about the energy processed by players in the console
    print("ENERGY:", end=" ")
    for player in range(1,5):
        print(dict_with_game_state["list_with_energy"][player], end="\t")
    print()
    print("SPENT:", end=" ")
    for player in range(1,5):
        print(dict_with_game_state["list_with_energy_spent"][player], end="\t")
    print()
    print("PROD.:", end=" ")
    for player in range(1,5):
        print(dict_with_game_state["list_with_energy_current_production"][player], end="\t")
    print()


# ============== make test units ============


def make_test_units(dict_with_game_state, dict_with_units):
# make test units

    # test vehicles for blue team
    number_of_test_vehicles = 7
    angle = math.pi * 2 / number_of_test_vehicles
    id = dict_with_game_state["lowest_free_id"]

    for i in range(number_of_test_vehicles):
        dict_with_units[id] = Small_artillery_ship(id, move_point([600, 500], 300, i*angle), i*angle, 1, 1) # - math.pi
        dict_with_units[id].base.movement_target = [[600, 500]]
        id += 1

    for i in range(10):
        dict_with_units[id] = Small_artillery_ship(id, [500 + 50*i, 100], math.pi/2, 1, 1)
        id += 1

    dict_with_units[8].base.movement_target = [[250, 400], [250, 600], [600, 700]]
    dict_with_units[9].base.movement_target = [[400, 400]]

    dict_with_units[id] = Battle_cruiser(id, [400, 100], math.pi/2, 1, 1)
    dict_with_units[id].base.movement_target = [[450, 400]]
    id += 1


    # test vehicles for green team
    red_id = 0
    for i in range(15):
        if red_id == 6 or red_id == 7: dict_with_units[id] = Main_battle_tank(id, [600 + 100*i, 2000], 3*math.pi/2, 2, 2) # 2500      
        else: dict_with_units[id] = Light_tank(id, [600 + 100*i, 2500], 3*math.pi/2, 2, 2)
        # LIST_WITH_UNITS[id].base.movement_target = [[500 + 50*i, 400]]
        id += 1
        red_id += 1
    
    for i in range(5):
        dict_with_units[id] = Fighter(id, [400 + 100*i, 2600], 3*math.pi/2, 2, 2)
        id += 1

    dict_with_units[id] = Destroyer(id, [300, 3000], 3*math.pi/2, 2, 2)
    id += 1
    dict_with_units[id] = Battleship(id, [100, 3000], 3*math.pi/2, 2, 2)
    id += 1
    dict_with_units[id] = Battleship(id, [500, 3000], 3*math.pi/2, 2, 2)
    id += 1

    # test vehicles for red team
    dict_with_units[id] = Light_tank(id, [1700, 700], math.pi, 3, 3)
    id += 1
    dict_with_units[id] = Light_tank(id, [1700, 750], math.pi, 3, 3)
    id += 1
    dict_with_units[id] = Main_battle_tank(id, [1700, 800], math.pi, 3, 3)
    id += 1
    dict_with_units[id] = Main_battle_tank(id, [1700, 850], math.pi, 3, 3)
    id += 1
    dict_with_units[id] = Spider_tank(id, [1700, 900], math.pi, 3, 3)
    id += 1
    dict_with_units[id] = Spider_tank(id, [1700, 950], math.pi, 3, 3)
    id += 1
    dict_with_units[id] = Heavy_tank(id, [1700, 1010], math.pi, 3, 3)
    id += 1
    dict_with_units[id] = Heavy_tank(id, [1700, 1070], math.pi, 3, 3)
    id += 1
    dict_with_units[id] = Heavy_artillery(id, [1700, 1130], math.pi, 3, 3)
    id += 1
    dict_with_units[id] = Heavy_artillery(id, [1700, 1190], math.pi, 3, 3)
    id += 1

    dict_with_units[id] = Small_artillery_ship(id, [1900, 100], math.pi, 3, 3)
    id += 1
    dict_with_units[id] = Small_artillery_ship(id, [1900, 150], math.pi, 3, 3)
    id += 1
    dict_with_units[id] = Small_AA_ship(id, [1900, 200], math.pi, 3, 3)
    id += 1
    dict_with_units[id] = Small_AA_ship(id, [1900, 250], math.pi, 3, 3)
    id += 1
    dict_with_units[id] = Battle_cruiser(id, [1900, 320], math.pi, 3, 3)
    id += 1
    dict_with_units[id] = Battle_cruiser(id, [1900, 400], math.pi, 3, 3)
    id += 1
    dict_with_units[id] = Destroyer(id, [1900, 510], math.pi, 3, 3)
    id += 1
    # dict_with_units[id] = Destroyer(id, [1900, 640], math.pi, 3, 3)
    # id += 1
    dict_with_units[id] = Battleship(id, [1700, 200], math.pi, 3, 3)
    id += 1

    dict_with_units[id] = Fighter(id, [2300, 100], math.pi, 3, 3)
    id += 1
    dict_with_units[id] = Fighter(id, [2300, 150], math.pi, 3, 3)
    id += 1
    dict_with_units[id] = Bomber(id, [2300, 200], math.pi, 3, 3)
    id += 1
    dict_with_units[id] = Bomber(id, [2300, 260], math.pi, 3, 3)
    id += 1
    dict_with_units[id] = Strategic_bomber(id, [2300, 350], math.pi, 3, 3)
    id += 1
    dict_with_units[id] = Strategic_bomber(id, [2300, 450], math.pi, 3, 3)
    id += 1

    # for i in range(10):
    #     dict_with_units[id] = Bomber(id, [2500, 100 + 50*i], math.pi, 3, 3)
    #     id += 1

    # for i in range(10):
    #     dict_with_units[id] = Strategic_bomber(id, [2600, 100 + 70*i], math.pi, 3, 3)
    #     id += 1

    # test buildings
    dict_with_units[id] = Land_factory(id, [2200, 1000], math.pi, 3, 3) # red land
    id += 1
    dict_with_units[id] = Navy_factory(id, [2650, 1000], 0, 3, 3) # red shelf
    id += 1
    dict_with_units[id] = Land_factory(id, [2200, 2500], math.pi, 2, 2) # green land
    id += 1
    dict_with_units[id] = Navy_factory(id, [2650, 2700], 0, 2, 2) # green shelf
    id += 1

    for i in range(7):
        dict_with_units[id] = Generator(id, [1900, 1000 + 290*i], 0, 3, 3)
        id += 1

    # space marines
    dict_with_units[id] = Space_marine(id, [1450, 700], math.pi/2, 3, 3) # red
    id += 1
    dict_with_units[id] = Super_space_marine(id, [1500, 700], math.pi/2, 3, 3) # red
    id += 1
    dict_with_units[id] = Commander(id, [1550, 700], math.pi/2, 3, 3) # red
    id += 1

    dict_with_units[id] = Space_marine(id, [1450, 2000], 3*math.pi/2, 2, 2) # green
    id += 1
    dict_with_units[id] = Super_space_marine(id, [1500, 2000], 3*math.pi/2, 2, 2) # green
    id += 1
    dict_with_units[id] = Commander(id, [1550, 2000], 3*math.pi/2, 2, 2) # green
    id += 1

    dict_with_units[id] = Small_AA_ship(id, [2800, 200], math.pi, 3, 3)
    id += 1

    dict_with_game_state["lowest_free_id"] = id


def make_test_units_2(dict_with_game_state, dict_with_units):
# make test units
    id = dict_with_game_state["lowest_free_id"]

    # test vehicles for blue team
    number_of_test_vehicles = 30

    # test vehicles for green team
    for i in range(number_of_test_vehicles):       
        dict_with_units[id] = Light_tank(id, [1000 + 100*i, 2000], 3*math.pi/2, 2, 2)
        id += 1
        dict_with_units[id] = Light_tank(id, [1000 + 100*i, 2100], 3*math.pi/2, 2, 2)
        id += 1
        dict_with_units[id] = Main_battle_tank(id, [1000 + 100*i, 2200], 3*math.pi/2, 2, 2)
        id += 1

    # test vehicles for red team
    for i in range(number_of_test_vehicles):       
        dict_with_units[id] = Light_tank(id, [1000 + 100*i, 700], math.pi/2, 3, 3)
        id += 1
        dict_with_units[id] = Light_tank(id, [1000 + 100*i, 600], math.pi/2, 3, 3)
        id += 1
        dict_with_units[id] = Main_battle_tank(id, [1000 + 100*i, 500], math.pi/2, 3, 3)
        id += 1

    dict_with_game_state["lowest_free_id"] = id

