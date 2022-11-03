import math

from classes_units import *


def make_test_units():
# make test units

    # test vehicles for blue team
    number_of_test_vehicles = 7
    angle = math.pi * 2 / number_of_test_vehicles
    id = 0
    LIST_WITH_UNITS = []
    for i in range(number_of_test_vehicles):
        LIST_WITH_UNITS.append(Light_tank(move_point([600, 500], 300, i*angle), i*angle, 1, 1)) # - math.pi
        LIST_WITH_UNITS[i].base.movement_target = [[600, 500]]
        id += 1

    for i in range(10):
        LIST_WITH_UNITS.append(Light_tank([500 + 50*i, 100], math.pi/2, 1, 1))
        id += 1

    LIST_WITH_UNITS[8].base.movement_target = [[250, 400], [250, 600], [600, 700]]
    LIST_WITH_UNITS[9].base.movement_target = [[400, 400]]

    LIST_WITH_UNITS.append(Main_battle_tank([450, 100], math.pi/2, 1, 1))
    LIST_WITH_UNITS[id].base.movement_target = [[450, 400]]
    id += 1


    # test vehicles for green team
    red_id = 0
    for i in range(15):
        if red_id == 6 or red_id == 7: LIST_WITH_UNITS.append(Main_battle_tank([300 + 100*i, 1500], -math.pi/2, 2, 2)) # 2500      
        else: LIST_WITH_UNITS.append(Light_tank([300 + 100*i, 1500], -math.pi/2, 2, 2))
        LIST_WITH_UNITS[id].base.movement_target = [[500 + 50*i, 400]]
        id += 1
        red_id += 1

    # test vehicles for red team
    LIST_WITH_UNITS.append(Light_tank([1700, 100], -math.pi, 3, 3))
    LIST_WITH_UNITS.append(Light_tank([1700, 150], -math.pi, 3, 3))
    LIST_WITH_UNITS.append(Main_battle_tank([1700, 200], -math.pi, 3, 3))
    LIST_WITH_UNITS.append(Main_battle_tank([1700, 250], -math.pi, 3, 3))

    return LIST_WITH_UNITS