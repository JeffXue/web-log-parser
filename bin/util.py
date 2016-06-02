# -*- coding:utf-8 -*-
import os


def get_parameter_lists(parameters):
    parameter_list = []
    for i, each_arg in enumerate(parameters):
        if i != 0:
            parameter_list.append(each_arg)
    return parameter_list


def get_dir_files(directory="../result"):
    files = [files for files in os.listdir(directory)]
    return files


def is_value(char):
    value_flag = 0
    if char in "0123456789.":
        value_flag = 1
    return value_flag


def get_max_index(my_list):
    return my_list.index(max(my_list))


def get_max_value(my_list):
    return float(max(my_list))


def get_min_index(my_list):
    return my_list.index(min(my_list))


def get_min_value(my_list):
    return float(min(my_list))


def get_avg_value(my_list):
    sum_value = sum(my_list)
    avg_value = "%0.2f" % float(sum_value / len(my_list))
    return float(avg_value)


def get_p9_value(my_list):
    """return the value which is > 90% list value"""
    new_list = my_list[:]
    new_list.sort()
    p9_value = new_list[int(len(new_list) * 0.9)]
    return p9_value






