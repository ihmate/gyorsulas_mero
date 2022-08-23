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

list = [0, 25, 50, 75, 100, 125, 150, 175, 200, 225, 250]

#font style for labels
title_font = {'family':'serif','color':'black','size':20}
label_font = {'family':'serif','color':'darkred','size':15}

#number of x and y-points -- refresh rate in ms
ylim = 50
xlim = 250
ms = 100

#changing plot color depending on the speed difference
def plot_color():
    #target_speed color
    plt.title(f"{int(target_speed[49])} KM/H (Target Speed)", fontdict = title_font, loc='left')

    #wheel_speed color 
    if (int(target_speed[49]) + 5 > int(wheel_speed[49]) and int(target_speed[49]) - 5 < int(wheel_speed[49])):
        plt.title(f"{wheel_speed[49]:.0f} KM/H (Wheel Speed)", fontdict = title_font, loc='right', c = "green")
        ax.plot(wheel_speed, wheel_speed_ypoints, linewidth = '7', color = 'green') 
    elif (int(target_speed[49]) + 15 > int(wheel_speed[49]) and int(target_speed[49]) - 15 < int(wheel_speed[49])):
        plt.title(f"{wheel_speed[49]:.0f} KM/H (Wheel Speed)", fontdict = title_font, loc='right', c = "orange")
        ax.plot(wheel_speed, wheel_speed_ypoints, linewidth = '7', color = 'orange') 
    else:
        plt.title(f"{wheel_speed[49]:.0f} KM/H (Wheel Speed)", fontdict = title_font, loc='right', c = "red")
        ax.plot(wheel_speed, wheel_speed_ypoints, linewidth = '7', color = 'red') 


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
    ax.plot(target_speed, target_speed_ypoints, linewidth = '30')

    ax.set_ylim(0, ylim)
    ax.set_xlim(0, xlim)

    # Set ticks frequency, position and text -- empty on y
    ax.set_xticks(list, list)
    ax.set_yticks([])
    ax.xaxis.tick_top()
    ax.tick_params(axis='x', colors='darkred', size = 10)
    
    #set title and label texts
    plot_color()

    plt.xlabel("Speed", fontdict = label_font)
    plt.ylabel(f"{ms} ms", fontdict = label_font)

    plt.grid(color = 'black', linestyle = '--', linewidth = 1)


if __name__ == '__main__':
    #open file for reading
    f = open(file_name, "r")

    # start collections with zeros and make ypoints for all xpoints
    wheel_speed = collections.deque(np.zeros(ylim))
    wheel_speed_ypoints = range(0, ylim)

    target_speed = collections.deque(np.zeros(ylim))
    target_speed_ypoints = range(0, ylim)

    # define and adjust figure - bgcolor
    fig = plt.figure(figsize=(12,6), facecolor='#DEDEDE')
    ax = plt.subplot()
    ax.set_facecolor('#DEDEDE')

    # animate
    print("asd")
    ani = FuncAnimation(fig, my_function, interval=ms)
    plt.show()

