import matplotlib.pyplot as plt
import numpy as np
import psutil
import collections

from matplotlib.animation import FuncAnimation
from shared_memory_dict import SharedMemoryDict

#shared memory for wheel_speed data
smd_config = SharedMemoryDict(name='config', size=1024)

#name of the .txt file
file_name = "proba_adat3.txt"

speed_list = [0, 25, 50, 75, 100, 125, 150, 175, 200, 225, 250]

#font style for labels
title_font = {'family':'serif','color':'black','size':20}
label_font = {'family':'serif','color':'darkred','size':15}

#number of x and y-points -- refresh rate in ms
ylim = 250
xlim = 50
ws_xlim = 26
ms = 100
wspd_idx = 25
tspd_idx = 25

#changing plot color depending on the speed difference
def plot_color():
    #target_speed color
    plt.title(f"{int(target_speed[tspd_idx])} KM/H (Target Speed)", fontdict = title_font, loc='left')

    #wheel_speed color 
    if (int(target_speed[tspd_idx]) + 5 > int(wheel_speed[wspd_idx]) and int(target_speed[tspd_idx]) - 5 < int(wheel_speed[wspd_idx])):
        line_color = "green"
    elif (int(target_speed[tspd_idx]) + 12 > int(wheel_speed[wspd_idx]) and int(target_speed[tspd_idx]) - 12 < int(wheel_speed[wspd_idx])):
        line_color = "orange"
    else:
        line_color = "red"

    plt.title(f"{wheel_speed[wspd_idx]:.0f} KM/H (Wheel Speed)", fontdict = title_font, loc='right', c = line_color)
    ax.plot(wheel_speed_ypoints, wheel_speed, linewidth = '7', color = line_color) 


# function to update the data
def my_function(i):
    # get data
    wheel_speed.popleft()
    wheel_speed.append(smd_config["status"])

    target_speed.popleft()
    target_speed.append(int(f.readline().rstrip('\n')))

    # clear axis
    ax.cla()

    # plot target_speed
    ax.plot(target_speed_ypoints, target_speed, linewidth = '30')

    ax.set_ylim(0, ylim)
    ax.set_xlim(0, xlim)

    # Set ticks frequency, position and text -- empty on y
    ax.set_yticks(speed_list, speed_list)
    ax.set_xticks([0, 5, 15, 25, 35, 45, 50], ["-2,5s", "-2s", "-1s", "0s", "+1s", "+2s", "-2,5s"])
    ax.yaxis.tick_right()
    ax.tick_params(axis='y', colors='darkred', size = 10)
    
    #set title and label texts
    plot_color()

    plt.xlabel(f"{ms} ms", fontdict = label_font)
    plt.ylabel("Speed", fontdict = label_font)

    plt.grid(color = 'black', linestyle = '--', linewidth = 1)


if __name__ == '__main__':
    #open file for reading
    f = open(file_name, "r")

    # start collections with zeros and make ypoints for all xpoints
    wheel_speed = collections.deque(np.zeros(ws_xlim))
    wheel_speed_ypoints = range(0, ws_xlim)

    target_speed = collections.deque(np.zeros(xlim))
    target_speed_ypoints = range(0, xlim)

    # define and adjust figure - bgcolor
    fig = plt.figure(figsize=(12,6), facecolor='#DEDEDE')
    ax = plt.subplot()
    ax.set_facecolor('#DEDEDE')

    # animate
    ani = FuncAnimation(fig, my_function, interval=ms)
    plt.show()

