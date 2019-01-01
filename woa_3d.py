# -*- coding: utf-8 -*-

# @Time    : 2019/1/1 19:08
# @Author  : Luc
# @Email   : lucyang0901@gmail.com
# @File    : woa_3d.py

import random
import math
import numpy as np
from print_colours import *
from load_data import *
import time

X_MIN = -2.23
Y_MIN = -2.64
Z_MIN = 0.01
X_MAX = 2.24
Y_MAX = 2.81
Z_MAX = 2.69
COUNTER_MAX = 100
STEP_LEN = 0.3


class Agent3D:
    def __init__(self):
        self.position = np.array([round(random.uniform(X_MIN, X_MAX), 2), round(random.uniform(Y_MIN, Y_MAX), 2),
                                  round(random.uniform(Z_MIN, Z_MAX), 2)])
        self.concentration = float('-inf')
        self.history = []

    def update_msg(self, new_position, new_concentration):
        self.history.append([self.position, self.concentration])
        self.position = new_position
        self.concentration = new_concentration


def check_boundary_3d(position):
    if position[0] < X_MIN:
        position[0] = X_MIN + abs(X_MIN - position[0]) + 0.05
    elif position[0] > X_MAX:
        position[0] = X_MAX - abs(X_MAX - position[0]) - 0.05

    if position[1] < Y_MIN:
        position[1] = Y_MIN + abs(Y_MIN - position[1]) + 0.05
    elif position[1] > Y_MAX:
        position[1] = Y_MAX - abs(Y_MAX - position[1]) - 0.05

    if position[2] < Z_MIN:
        position[2] = Z_MIN + abs(Z_MIN - position[2]) + 0.05
    elif position[2] > Z_MAX:
        position[2] = Z_MAX - abs(Z_MAX - position[2]) - 0.05

    position[0] = round(position[0], 2)
    position[1] = round(position[1], 2)
    position[2] = round(position[2], 2)
    return position


def get_agents_positions(agents):
    positions = []
    for agent in agents:
        positions.append(agent.position)
    return np.array(positions)


def init_agents_random(agents_no, c_field):
    leader = Agent3D()
    leader.position = np.array([0, 0, 0])
    leader.concentration = float('-inf')
    agents = []
    for i in range(agents_no):
        agents.append(Agent3D())

    agents = update_agents_c(agents, c_field)
    agents = update_agents_history(agents)
    leader = update_leader(agents, leader)
    return agents, leader


def init_agents_fixed(agents_no, c_field, init_position):
    leader = Agent3D()
    leader.position = np.array([0, 0, 0])
    leader.concentration = float('-inf')
    agents = []
    x = init_position[0]
    y = init_position[1]
    z = init_position[2]
    for i in range(agents_no):
        agents.append(Agent3D())
        agents[-1].position = np.array(
            [x + random.uniform(-0.5, 0.5), y + random.uniform(-0.5, 0.5), z + random.uniform(-0.5, 0.5)])
    agents = update_agents_c(agents, c_field)
    agents = update_agents_history(agents)
    leader = update_leader(agents, leader)
    return agents, leader


def update_agents_c(agents, c_field):
    agents_c = get_c_3d(c_field, get_agents_positions(agents))
    for i in range(len(agents)):
        agents[i].concentration = agents_c[i]
    return agents


def update_agents_history(agents):
    for agent in agents:
        agent.update_msg(agent.position, agent.concentration)
    return agents


def update_leader(agents, leader):
    agents_no = len(agents)
    max_c = float('-inf')
    max_index = 0
    for i in range(agents_no):  # 这个循环更新leader
        if agents[i].concentration > max_c:
            max_c = agents[i].concentration
            max_index = i
    if max_c > leader.concentration:
        leader.position = agents[max_index].position
        leader.concentration = agents[max_index].concentration
    leader.update_msg(leader.position, leader.concentration)
    return leader


def go_forward(agents):
    for agent in agents:
        if len(agent.history) <= 1:
            gradient = np.array([round(random.uniform(X_MIN, X_MAX), 2), round(random.uniform(Y_MIN, Y_MAX), 2),
                                 round(random.uniform(Z_MIN, Z_MAX), 2)])
        else:
            gradient = agent.history[-1][0] - agent.history[-2][0]  # 当前位置减去上一步的位置，得到方向向量
        gradient_len = np.linalg.norm(gradient)
        if gradient_len == 0:
            direction = np.array([round(random.uniform(0, 1), 2), round(random.uniform(0, 1), 2),
                                  round(random.uniform(0, 1), 2)])
        else:
            direction = gradient / gradient_len
        new_position = agent.position + STEP_LEN * direction
        new_position = check_boundary_3d(new_position)
        agent.position = new_position
    return agents


def woa_3d(agents, leader):
    agents_no = len(agents)
    counter = len(leader.history)
    for agent in agents:

        # c_gradient = np.array([0, 0, 0])
        # if counter > 0:
        #     if agent.concentration > agent.history[-1][1]:
        #         c_gradient = agent.position - agent.history[-1][0]

        a = 2 - counter * (2.0 / float(COUNTER_MAX))

        """为了避免后期步长过小，对a进行处理"""
        if a < 0.3:
            a += random.uniform(0, 1)

        p = random.uniform(0, 1)

        A = 2 * a * random.uniform(0, 1) - a
        C = 2 * random.uniform(0, 1)

        chioce = 0
        if p < 0.5:
            if abs(A) < 1:
                chioce = 0
                D = abs(C * leader.position - agent.position)
                # print(leader.position)
                # print(A * D)
                new_position = leader.position - A * D
            elif abs(A) >= 1:
                chioce = 1
                random_agent_no = random.randint(0, agents_no - 1)
                random_agent = agents[random_agent_no]
                D = abs(C * random_agent.position - agent.position)
                new_position = random_agent.position - A * D
        elif p >= 0.5:
            chioce = 2
            D = abs(leader.position - agent.position)
            b = 1  # 用来定义螺旋大小的常数
            l = random.uniform(-1, 1)
            new_position = D * math.exp(b * l) * math.cos(2 * math.pi * l) + leader.position

        new_position = check_boundary_3d(new_position)
        agent.position = new_position
    return agents


def plume_finding(agents, leader, c_field):
    agents = go_forward(agents)
    agents = update_agents_c(agents, c_field)
    agents = update_agents_history(agents)
    leader = update_leader(agents, leader)
    return agents, leader


def plume_tracking(agents, leader, c_field):
    agents = woa_3d(agents, leader)
    agents = update_agents_c(agents, c_field)
    agents = update_agents_history(agents)
    leader = update_leader(agents, leader)
    return agents, leader


def show_info(agents, leader, t, state):
    print('********')
    if state == 0:
        print_green('FINDING')
    elif state == 1:
        print_red('TRACING')
    print('ITER NO. %d\tTIME %d' % (len(leader.history), t))
    print('********')
    for i in range(len(agents)):
        print('agent no. %d\t\tp: %s\tc: %s' % (i, str(agents[i].position), str(agents[i].concentration)))
    print('********')
    print_yellow('AGENT LEADER\tp: %s\tc: %s' % (leader.position, leader.concentration))
    print('********')


def save_results(agents, leader, serial_no, finding_end):
    import os
    path = 'result/' + str(serial_no)
    is_exists = os.path.exists(path)

    if not is_exists:
        os.mkdir(path)

    f = open(path + '/%s.txt' % (serial_no), 'w')
    for i in range(len(leader.history)):
        if i < finding_end:
            f.write('FINDING  ITER NO. %d\tTIME %d\n' % (i, 2 * i))
        else:
            f.write('FINDING  ITER NO. %d\tTIME %d\n' % (i, 2 * i))
        for j in range(len(agents)):
            f.write('agent no. %d\t\tp: %s\tc: %s\n' % (j, str(agents[j].position), str(agents[j].concentration)))
        f.write('AGENT LEADER\tp: %s\tc: %s\n' % (str(leader.history[i][0]), str(leader.history[i][1])))
    print('Result have been saved to result/%s.txt' % (serial_no))
