from settings import *


def player_color(player_id):
# return player color
    if player_id == 0:
        return BLACK
    elif player_id == 1:
        return BLUE
    elif player_id == 2:
        return GREEN
    elif player_id == 3:
        return RED
    else: return WHITE