# -*- coding: utf-8 -*-

# @Time    : 2019/1/2 0:00
# @Author  : Luc
# @Email   : lucyang0901@gmail.com
# @File    : for_test.py


import matplotlib.pyplot as plt
import numpy as np
import random

COUNTER_MAX = 100

leader = np.array([2, 2])
agent = np.array([1, 1])
plt.figure(figsize=(8, 6))

for i in range(10000):
    C = np.array([random.uniform(0, 1), random.uniform(0, 1)])
    A = np.array([random.uniform(-1, 1), random.uniform(-1, 1)])
    D = C * abs(leader - agent)
    print('leader = %s agent = %s abs = %s' % (leader, agent, abs(leader - agent)))
    print('A = %s  C = %s D = %s ' % (A, C, D))
    agent_new = leader - A * D
    # print('A = %f  C = %f  D = %s  A*D = %s' % (A, C, D, A * D))
    plt.scatter(agent_new[0], agent_new[1], c='g')

plt.scatter(leader[0], leader[1], c='r')
plt.text(leader[0], leader[1], 'leader: ' + str(leader))
plt.scatter(agent[0], agent[1], c='r')
plt.text(agent[0], agent[1], 'agent: ' + str(agent))
plt.show()
