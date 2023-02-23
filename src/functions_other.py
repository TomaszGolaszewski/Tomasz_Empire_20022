

def remove_few_dead_elements_from_list(list):
# function removes dead elements from list - good for a few dead elements
    temp_list_of_indexes = []
    for i, element in enumerate(list):
        if element.to_remove:
        # if not element.is_alive:
            temp_list_of_indexes.append(i)

    temp_list_of_indexes.reverse()

    for i in temp_list_of_indexes:
        list.pop(i)

def remove_many_dead_elements_from_list(list):
# function removes dead elements from list - good for many dead elements

    # list = [element for element in list if element.is_alive]
    # return list

    new_list = []
    for element in list:
        if not element.to_remove:
        # if element.is_alive:
            new_list.append(element)

    return new_list

def remove_dead_elements_from_dict(dict):
# function removes dead elements from dictionary
    temp_list_of_indexes = []
    for id in dict:
        if dict[id].to_remove:
            temp_list_of_indexes.append(id)

    for id in temp_list_of_indexes:
        dict.pop(id)
