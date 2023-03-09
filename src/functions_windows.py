from classes_ui import *


def make_windows_from_dict_with_units(dict_with_units, list_with_windows):
    # function adds new windows to list when conditions are met

    number_of_selected_units = 0
    current_unit_id = 0
    for unit_id in dict_with_units:
        if dict_with_units[unit_id].is_selected: 
            number_of_selected_units += 1
            current_unit_id = unit_id

    if number_of_selected_units == 1 and not len(list_with_windows) and dict_with_units[current_unit_id].unit_type == "building":
        if dict_with_units[current_unit_id].name == "Land factory":
            list_with_windows.append(Notebook_land_factory(current_unit_id, dict_with_units))
            list_with_windows.append(Building_queue(current_unit_id))
        elif dict_with_units[current_unit_id].name == "Navy factory":
            list_with_windows.append(Notebook_navy_factory(current_unit_id, dict_with_units))
            list_with_windows.append(Building_queue(current_unit_id))

    if number_of_selected_units == 1 and not len(list_with_windows) and dict_with_units[current_unit_id].unit_type != "building":
        list_with_windows.append(Info_about_unit(current_unit_id, dict_with_units))

def make_windows_from_right_mouse_button(dict_with_units, list_with_windows, screen_coord, world_coord):
    # function adds new windows to list when conditions are met
        selected_unit_type = "none"
        for unit_id in dict_with_units:
            if dict_with_units[unit_id].is_selected: 
                selected_unit_type = dict_with_units[unit_id].unit_type
                break
        
        if selected_unit_type == "air" or selected_unit_type == "land" or selected_unit_type == "navy":
            list_with_windows.append(Base_slide_button(screen_coord, world_coord))
        elif selected_unit_type == "building":
            pass
        else:
            pass
            
    
