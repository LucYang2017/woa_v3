# -*- coding: utf-8 -*-

# @Time    : 2019/1/1 19:02
# @Author  : Luc
# @Email   : lucyang0901@gmail.com
# @File    : load_data.py

import numpy as np
from scipy.interpolate import griddata
import time
import pickle as p


def scinum_2_float(sci_num):
    """
    转换科学计数法的数字或字符串为浮点类型
    :param sci_num: 科学计数法表达的数字，类型一般是字符串，比如 6.0000000e+000 "3.4717316e-009"
    :return: 返回浮点类型的数字
    """
    sci_num = str(sci_num)
    base = float(sci_num.split('E')[0])
    power = float(sci_num.split('E')[1])
    return base * pow(10, power)


def nodes_msgs_3d(file_name):
    raw_data = open('data/Mix_constantx/' + str(file_name) + '.txt', 'r', encoding='utf-8').readlines()[1:]
    nodes = []
    # for i in range(len(raw_data)):  # 这个for用于处理有风速信息的数据
    #     msg = raw_data[i].split(',')[1:]
    #     if round(scinum_2_float(msg[1]), 2) == height:
    #         x_coordinate = round(scinum_2_float(msg[0]), 2)
    #         y_coordinate = round(scinum_2_float(msg[1]), 2)
    #         z_coordinate = round(scinum_2_float(msg[2]), 2)
    #         position = [x_coordinate, y_coordinate, z_coordinate]
    #         x_airflow_velocity = scinum_2_float(msg[3])
    #         y_airflow_velocity = scinum_2_float(msg[4])
    #         z_airflow_velocity = scinum_2_float(msg[5])
    #         airflow_velocity = [x_airflow_velocity, y_airflow_velocity, z_airflow_velocity]
    #         concentration = [round(scinum_2_float(msg[6]), 3)]
    #         node_msg = position + airflow_velocity + concentration
    #         node_msgs.append(node_msg)
    for i in range(len(raw_data)):  # 这个for用于处理没有风速信息的数据
        msg = raw_data[i].split(',')[1:]
        x_coordinate = round(scinum_2_float(msg[0]), 2)
        y_coordinate = round(scinum_2_float(msg[1]), 2)
        z_coordinate = round(scinum_2_float(msg[2]), 2)
        position = [x_coordinate, y_coordinate, z_coordinate]
        concentration = [round(scinum_2_float(msg[-1]), 3)]
        node = position + concentration
        nodes.append(node)
    return nodes


def nodes_msgs_2d(file_name, del_axis, axis_value):
    raw_data = open('Mix_constantx/' + str(file_name) + '.txt', 'r', encoding='utf-8').readlines()[1:]
    nodes = []
    # for i in range(len(raw_data)):  # 这个for用于处理有风速信息的数据
    #     msg = raw_data[i].split(',')[1:]
    #     if round(scinum_2_float(msg[1]), 2) == height:
    #         x_coordinate = round(scinum_2_float(msg[0]), 2)
    #         y_coordinate = round(scinum_2_float(msg[1]), 2)
    #         z_coordinate = round(scinum_2_float(msg[2]), 2)
    #         position = [x_coordinate, y_coordinate, z_coordinate]
    #         x_airflow_velocity = scinum_2_float(msg[3])
    #         y_airflow_velocity = scinum_2_float(msg[4])
    #         z_airflow_velocity = scinum_2_float(msg[5])
    #         airflow_velocity = [x_airflow_velocity, y_airflow_velocity, z_airflow_velocity]
    #         concentration = [round(scinum_2_float(msg[6]), 3)]
    #         node_msg = position + airflow_velocity + concentration
    #         node_msgs.append(node_msg)

    for i in range(len(raw_data)):  # 这个for用于处理没有风速信息的数据
        msg = raw_data[i].split(',')[1:]
        if round(scinum_2_float(msg[del_axis]), 2) == axis_value:
            x_coordinate = round(scinum_2_float(msg[0]), 2)
            y_coordinate = round(scinum_2_float(msg[1]), 2)
            z_coordinate = round(scinum_2_float(msg[2]), 2)
            position = [x_coordinate, y_coordinate, z_coordinate]
            position.pop(del_axis)
            concentration = [round(scinum_2_float(msg[-1]), 3)]
            node = position + concentration
            nodes.append(node)
    return nodes


def get_c_2d(plane, positions):
    plane = np.array(plane)
    positions = np.array(positions)
    grid_c = griddata(plane[:, :2], plane[:, -1], positions, method='linear', )
    return grid_c


def get_c_3d(nodes, positions):
    nodes = np.array(nodes)
    positions = np.array(positions)
    grid_c = griddata(nodes[:, :3], nodes[:, -1], positions, method='linear', )
    return grid_c


def show_field_info(nodes):
    n = np.array(nodes)
    x = n[:, 0]
    y = n[:, 1]
    z = n[:, 2]
    print('x_max = %f   x_min = %f ' % (max(x), min(x)))
    print('y_max = %f   y_min = %f ' % (max(y), min(y)))
    print('z_max = %f   z_min = %f ' % (max(z), min(z)))

