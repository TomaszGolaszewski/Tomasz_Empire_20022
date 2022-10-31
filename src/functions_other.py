

def remove_few_dead_elements(list):
# function removes dead elements - good for a few dead elements
    temp_list_of_indexes = []
    for i, element in enumerate(list):
        if not element.is_alive:
            temp_list_of_indexes.append(i)

    temp_list_of_indexes.reverse()

    for i in temp_list_of_indexes:
        list.pop(i)
    
    # return list


def remove_many_dead_elements(list):
# function removes dead elements - good for many dead elements

    # list = [element for element in list if element.is_alive]
    # return list

    temp_list = []
    for element in list:
        if element.is_alive:
            temp_list.append(element)

    return temp_list