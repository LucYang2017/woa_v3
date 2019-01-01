# -*- coding: utf-8 -*-

# @Time    : 2019/1/1 19:08
# @Author  : Luc
# @Email   : lucyang0901@gmail.com
# @File    : woa_2d.py

import random
import math
from load_data import *

X_MIN = -2.23
Y_MIN = -2.64
Z_MIN = 0.01
X_MAX = 2.24
Y_MAX = 2.81
Z_MAX = 2.69


class Agent2D:
    def __init__(self):
        self.position = np.array([round(random.uniform(X_MIN, X_MAX), 3), round(random.uniform(Y_MIN, Y_MAX), 3)])
        self.concentration = float('-inf')
        self.history = []

    def update_msg(self, new_position, new_concentration):
        self.history.append([self.position, self.concentration])
        self.position = new_position
        self.concentration = new_concentration


class Agent3D:
    def __init__(self):
        self.position = np.array([round(random.uniform(X_MIN, X_MAX), 3), round(random.uniform(Y_MIN, Y_MAX), 3),
                                  round(random.uniform(Z_MIN, Z_MAX), 3)])
        self.concentration = float('-inf')
        self.history = []

    def update_msg(self, new_position, new_concentration):
        self.history.append([self.position, self.concentration])
        self.position = new_position
        self.concentration = new_concentration


def check_boundary_2d(position):
    if position[0] < X_MIN:
        position[0] = X_MIN + 0.05
    elif position[0] > X_MAX:
        position[0] = X_MAX - 0.05

    if position[1] < Y_MIN:
        position[1] = Y_MIN + 0.05
    elif position[1] > Y_MAX:
        position[1] = Y_MAX - 0.05
    return position


def get_agents_positions(agents):
    positions = []
    for agent in agents:
        positions.append(agent.position)
    return np.array(positions)


def woa():
    pass


def woa_2d(plane, search_agents_no, max_counter):
    agents = []
    for i in range(search_agents_no):
        agents.append(Agent2D())
    agents_c = get_c_2d(plane, get_agents_positions(agents))
    for i in range(search_agents_no):
        agents[i].concentration = agents_c[i]
    leader_agent = Agent2D()
    leader_agent.position = np.array([0, 0])
    leader_agent.concentration = float('-inf')

    counter = 0

    while counter < max_counter:
        print("++++++++++++++++++++++++++")
        print("counter = " + str(counter))
        for agent in agents:  # 这个循环更新leader
            if agent.concentration > leader_agent.concentration:
                leader_agent.update_msg(agent.position, agent.concentration)

        for agent in agents:  # 这个循环逐个更新agent的坐标
            print("agent no. " + str(agents.index(agent)) + " position: " + str(agent.position) + " con : " +
                  str(agent.concentration))
            c_gradient = np.array([0, 0])
            if counter > 0:
                if agent.concentration > agent.history[-1][1]:
                    c_gradient = agent.position - agent.history[-1][0]
            a = 2 - counter * (2.0 / float(max_counter))

            # print("distance before  = " + str(np.linalg.norm(leader_agent_position - agent.position)))
            p = random.uniform(0, 1)

            A = 2 * a * random.uniform(0, 1) - a
            C = 2 * random.uniform(0, 1)
            chioce = 0
            if p < 0.5:
                if abs(A) < 1:
                    chioce = 0
                    D = abs(C * leader_agent.position - agent.position)
                    new_position = leader_agent.position - A * D
                elif abs(A) >= 1:
                    chioce = 1
                    # D = abs(C * leader_agent_position - agent.position)
                    # new_position = leader_agent_position - A * D
                    random_agent_no = random.randint(0, search_agents_no - 1)
                    random_agent = agents[random_agent_no]
                    D = abs(C * random_agent.position - agent.position)
                    new_position = random_agent.position - A * D
            elif p >= 0.5:
                chioce = 2
                D = abs(leader_agent.position - agent.position)
                b = 1  # 用来定义螺旋大小的常数
                l = random.uniform(-1, 1)
                new_position = D * math.exp(b * l) * math.cos(2 * math.pi * l) + leader_agent.position
            new_position = check_boundary_2d(new_position)
            agent.position = new_position
            # print("choice = " + str(chioce))
            # print("distance after  = " + str(np.linalg.norm(leader_agent_position - agent.position)))
        agents_c = get_c_2d(plane, get_agents_positions(agents))
        for i in range(search_agents_no):
            agents[i].concentration = agents_c[i]
        for agent in agents:
            agent.update_msg(agent.position, agent.concentration)
        counter = counter + 1
        print("agent leader position: " + str(leader_agent.position) + " con : " + str(leader_agent.concentration))


plane = nodes_msgs_2d(200, 2, 2.68)

woa_2d(plane, 3, 100)

