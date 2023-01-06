# GLOBAL IMPORTS
import numpy as np


# General purpose functions

def unpack_cursor_object(object, field: str) -> list:
    obj_list = []
    for obj in object:
        obj_list.append(obj[field])
    return obj_list

def unpack_cursor_object_multiple(object, field: list = []) -> dict:
    obj_dict = {}
    for obj in object:
        for f in field:
            if f in obj_dict:
                obj_dict[f].append(obj[f])
            else:
                obj_dict[f] = [obj[f]]
    return obj_dict

def dict_values_to_list_values_in_dict(dict_with_dicts: dict = {}) -> dict:
    dict_with_lists = {}
    for key,values in dict_with_dicts.items():
        value_list = []
        for k, v in values.items():
            value_list.append(v)
        dict_with_lists[key] = value_list
    return dict_with_lists


def compute_rolling_window(input_list: list = [], n_periods: int = 0) -> list:
    output_list = []
    for i in range (len(input_list)):
        rolling_value = sum(input_list[i:i+n_periods]) / n_periods
        output_list.append(rolling_value)
    return output_list

def get_list(set) -> list:
    list = []
    for key in set.keys():
        list.append(key)
         
    return list

def average_of_dict_keys_n_values(input_dict: dict = {}, keys: list = [], number_of_values_for_average: list = []) -> int:
    first_output_int = input_dict[keys[0]][0]
    second_output_int = np.average(np.asarray(input_dict[keys[1]][:5]))
    return first_output_int, second_output_int