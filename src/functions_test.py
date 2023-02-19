import math

from classes_units import *
from classes_buildings import *


def make_test_units():
# make test units

    # test vehicles for blue team
    number_of_test_vehicles = 7
    angle = math.pi * 2 / number_of_test_vehicles
    id = 0
    LIST_WITH_UNITS = []
    for i in range(number_of_test_vehicles):
        LIST_WITH_UNITS.append(Small_artillery_ship(move_point([600, 500], 300, i*angle), i*angle, 1, 1)) # - math.pi
        LIST_WITH_UNITS[i].base.movement_target = [[600, 500]]
        id += 1

    for i in range(10):
        LIST_WITH_UNITS.append(Small_artillery_ship([500 + 50*i, 100], math.pi/2, 1, 1))
        id += 1

    LIST_WITH_UNITS[8].base.movement_target = [[250, 400], [250, 600], [600, 700]]
    LIST_WITH_UNITS[9].base.movement_target = [[400, 400]]

    LIST_WITH_UNITS.append(Battle_cruiser([400, 100], math.pi/2, 1, 1))
    LIST_WITH_UNITS[id].base.movement_target = [[450, 400]]
    id += 1


    # test vehicles for green team
    red_id = 0
    for i in range(15):
        if red_id == 6 or red_id == 7: LIST_WITH_UNITS.append(Main_battle_tank([600 + 100*i, 2000], 3*math.pi/2, 2, 2)) # 2500      
        else: LIST_WITH_UNITS.append(Light_tank([600 + 100*i, 2500], 3*math.pi/2, 2, 2))
        # LIST_WITH_UNITS[id].base.movement_target = [[500 + 50*i, 400]]
        id += 1
        red_id += 1
    
    for i in range(5):
        LIST_WITH_UNITS.append(Fighter([400 + 100*i, 2600], 3*math.pi/2, 2, 2))

    LIST_WITH_UNITS.append(Destroyer([300, 3000], 3*math.pi/2, 2, 2))
    LIST_WITH_UNITS.append(Battleship([100, 3000], 3*math.pi/2, 2, 2))
    LIST_WITH_UNITS.append(Battleship([500, 3000], 3*math.pi/2, 2, 2))


    # test vehicles for red team
    LIST_WITH_UNITS.append(Light_tank([1700, 700], math.pi, 3, 3))
    LIST_WITH_UNITS.append(Light_tank([1700, 750], math.pi, 3, 3))
    LIST_WITH_UNITS.append(Main_battle_tank([1700, 800], math.pi, 3, 3))
    LIST_WITH_UNITS.append(Main_battle_tank([1700, 850], math.pi, 3, 3))
    LIST_WITH_UNITS.append(Spider_tank([1700, 900], math.pi, 3, 3))
    LIST_WITH_UNITS.append(Spider_tank([1700, 950], math.pi, 3, 3))
    LIST_WITH_UNITS.append(Heavy_tank([1700, 1010], math.pi, 3, 3))
    LIST_WITH_UNITS.append(Heavy_tank([1700, 1070], math.pi, 3, 3))
    LIST_WITH_UNITS.append(Heavy_artillery([1700, 1130], math.pi, 3, 3))
    LIST_WITH_UNITS.append(Heavy_artillery([1700, 1190], math.pi, 3, 3))

    LIST_WITH_UNITS.append(Small_artillery_ship([1900, 100], math.pi, 3, 3))
    LIST_WITH_UNITS.append(Small_artillery_ship([1900, 150], math.pi, 3, 3))
    LIST_WITH_UNITS.append(Small_AA_ship([1900, 200], math.pi, 3, 3))
    LIST_WITH_UNITS.append(Small_AA_ship([1900, 250], math.pi, 3, 3))
    LIST_WITH_UNITS.append(Battle_cruiser([1900, 320], math.pi, 3, 3))
    LIST_WITH_UNITS.append(Battle_cruiser([1900, 400], math.pi, 3, 3))
    LIST_WITH_UNITS.append(Destroyer([1900, 510], math.pi, 3, 3))
    LIST_WITH_UNITS.append(Destroyer([1900, 640], math.pi, 3, 3))
    LIST_WITH_UNITS.append(Battleship([1700, 200], math.pi, 3, 3))

    LIST_WITH_UNITS.append(Fighter([2300, 100], math.pi, 3, 3))
    LIST_WITH_UNITS.append(Fighter([2300, 150], math.pi, 3, 3))
    LIST_WITH_UNITS.append(Bomber([2300, 200], math.pi, 3, 3))
    LIST_WITH_UNITS.append(Bomber([2300, 260], math.pi, 3, 3))
    LIST_WITH_UNITS.append(Strategic_bomber([2300, 350], math.pi, 3, 3))
    LIST_WITH_UNITS.append(Strategic_bomber([2300, 450], math.pi, 3, 3))

    for i in range(10):
        LIST_WITH_UNITS.append(Bomber([2500, 100 + 50*i], math.pi, 3, 3))

    for i in range(10):
        LIST_WITH_UNITS.append(Strategic_bomber([2600, 100 + 70*i], math.pi, 3, 3))

    # test buildings
    LIST_WITH_UNITS.append(Building([2200, 1000], math.pi, 3, 3))
    LIST_WITH_UNITS.append(Building([2200, 2500], math.pi, 2, 2))

    return LIST_WITH_UNITS

def make_test_units_2():
# make test units
    LIST_WITH_UNITS = []

    # test vehicles for blue team
    number_of_test_vehicles = 30

    # test vehicles for green team
    for i in range(number_of_test_vehicles):       
        LIST_WITH_UNITS.append(Light_tank([1000 + 100*i, 2000], 3*math.pi/2, 2, 2))
        LIST_WITH_UNITS.append(Light_tank([1000 + 100*i, 2100], 3*math.pi/2, 2, 2))
        LIST_WITH_UNITS.append(Main_battle_tank([1000 + 100*i, 2200], 3*math.pi/2, 2, 2)) 

    # test vehicles for red team
    for i in range(number_of_test_vehicles):       
        LIST_WITH_UNITS.append(Light_tank([1000 + 100*i, 700], math.pi/2, 3, 3))
        LIST_WITH_UNITS.append(Light_tank([1000 + 100*i, 600], math.pi/2, 3, 3))
        LIST_WITH_UNITS.append(Main_battle_tank([1000 + 100*i, 500], math.pi/2, 3, 3)) 
    

    return LIST_WITH_UNITS