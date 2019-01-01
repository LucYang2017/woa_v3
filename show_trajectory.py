# -*- coding: utf-8 -*-

# @Time    : 2019/1/1 19:06
# @Author  : Luc
# @Email   : lucyang0901@gmail.com
# @File    : show_trajectory.py


from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
from woa_3d import *


def save_trajectory(agents, leader, serial_no):
    fig = plt.figure(figsize=(8, 6))
    ax = fig.gca(projection='3d')
    ax.set_title(str(serial_no))
    ax.set_xlabel('X')
    ax.set_xlim(X_MIN, X_MAX)
    ax.set_ylabel('Y')
    ax.set_ylim(Y_MIN, Y_MAX)
    ax.set_zlabel('Z')
    ax.set_zlim(Z_MIN, Z_MAX)
    colours = ['b', 'g', 'c', 'm', 'y', 'k', 'w', 'r']

    for agent in agents:
        x = []
        y = []
        z = []
        for p in agent.history:
            x.append(p[0][0])
            y.append(p[0][1])
            z.append(p[0][2])
        colour_no = agents.index(agent) % len(colours)
        ax.plot(np.array(x), np.array(y), np.array(z), c=colours[colour_no])
        for i in range(len(agent.history)):
            ax.scatter(x[i], y[i], z[i], marker='.', c='k')
            ax.text(x[i], y[i], z[i], i + 1, color=colours[colour_no])

    x = []
    y = []
    z = []
    for p in leader.history:
        x.append(p[0][0])
        y.append(p[0][1])
        z.append(p[0][2])
    colour_no = agents.index(agent) % len(colours)
    ax.plot(np.array(x), np.array(y), np.array(z), c=colours[colour_no])
    for i in range(len(agent.history)):
        ax.scatter(x[i], y[i], z[i], marker='*', c='r')
        ax.text(x[i], y[i], z[i], '    ' + str(i + 1), color='r', fontsize='large')
    import os
    path = 'result/' + str(serial_no)
    is_exists = os.path.exists(path)

    if not is_exists:
        os.mkdir(path)

    plt.savefig(path + '/%s-%s.png' % (serial_no, str(len(leader.history))))
    plt.show()


def show_trajectory(agents, leader, serial_no):
    fig = plt.figure(figsize=(8, 6))
    ax = fig.gca(projection='3d')
    ax.set_title(str(serial_no))
    ax.set_xlabel('X')
    ax.set_xlim(X_MIN, X_MAX)
    ax.set_ylabel('Y')
    ax.set_ylim(Y_MIN, Y_MAX)
    ax.set_zlabel('Z')
    ax.set_zlim(Z_MIN, Z_MAX)

    colours = ['b', 'g', 'c', 'm', 'y', 'k', 'w', 'r']
    for agent in agents:
        x = []
        y = []
        z = []
        for p in agent.history:
            x.append(p[0][0])
            y.append(p[0][1])
            z.append(p[0][2])
        colour_no = agents.index(agent) % len(colours)
        ax.plot(np.array(x), np.array(y), np.array(z), c=colours[colour_no])
        for i in range(len(agent.history)):
            ax.scatter(x[i], y[i], z[i], marker='.', c='k')
            ax.text(x[i], y[i], z[i], i + 1, color=colours[colour_no])
    x = []
    y = []
    z = []
    for p in leader.history:
        x.append(p[0][0])
        y.append(p[0][1])
        z.append(p[0][2])
    colour_no = agents.index(agent) % len(colours)
    ax.plot(np.array(x), np.array(y), np.array(z), c=colours[colour_no])
    for i in range(len(agent.history)):
        ax.scatter(x[i], y[i], z[i], marker='*', c='r')
        ax.text(x[i], y[i], z[i], '    ' + str(i + 1), color='r', fontsize='large')
    plt.show()
