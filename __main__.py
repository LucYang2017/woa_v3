# -*- coding: utf-8 -*-

# @Time    : 2019/1/1 19:09
# @Author  : Luc
# @Email   : lucyang0901@gmail.com
# @File    : __main__.py

from woa_3d import *
from show_trajectory import *
from load_data import *

if __name__ == "__main__":
    agents_no = 3
    t = 1
    c_field = nodes_msgs_3d(t)
    plume_finding_threshold = 0.2
    woa_threshold = 0.6
    state = 0
    serial_no = str(time.strftime("%Y%m%d-%H%M%S", time.localtime()))

    # agents, leader = init_agents_random(agents_no, c_field)

    init_position = [-1, -1, 0.5]
    agents, leader = init_agents_fixed(agents_no, c_field, init_position)
    show_info(agents, leader, t, state)

    while leader.concentration <= plume_finding_threshold and len(leader.history) < COUNTER_MAX:
        t = len(leader.history) * 2
        if t >= 200:
            t = 200
        c_field = nodes_msgs_3d(t)
        agents, leader = plume_finding(agents, leader, c_field)
        show_trajectory(agents, leader, serial_no)
        show_info(agents, leader, t, state)

    finding_end = len(leader.history)

    state = 1
    while leader.concentration <= woa_threshold and len(leader.history) < COUNTER_MAX:
        t = len(leader.history) * 2
        if t >= 200:
            t = 200
        c_field = nodes_msgs_3d(t)
        agents, leader = plume_tracking(agents, leader, c_field)
        show_trajectory(agents, leader, serial_no)
        show_info(agents, leader, t, state)

    save_trajectory(agents, leader, serial_no)
    save_results(agents, leader, serial_no, finding_end)
    # copy_console_output(serial_no)
