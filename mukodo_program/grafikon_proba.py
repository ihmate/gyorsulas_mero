import matplotlib.pyplot as plt
import numpy as np
import psutil
import collections

from matplotlib.animation import FuncAnimation
from shared_memory_dict import SharedMemoryDict

#shared memory for wheel_speed data
smd_config = SharedMemoryDict(name='config', size=1024)

#font style for labels
font1 = {'family':'serif','color':'blue','size':20}
font2 = {'family':'serif','color':'darkred','size':15}

#number of x and y-points -- refresh rate in ms
ylim = 50
xlim = 250
ms = 100

# function to update the data
def my_function(i):
    # get data
    wheel_speed.popleft()
    wheel_speed.append(smd_config["status"])

    data_zone.popleft()
    data_zone.append(int(f.readline()))

    # clear axis
    ax.cla()

    # plot data_zone and wheel_speed
    ax.plot(data_zone, data_zone_ypoints, linewidth = '40')
    ax.plot(wheel_speed, wheel_speed_ypoints, linewidth = '7') 

    ax.set_ylim(0, ylim)
    ax.set_xlim(0, xlim)
    # Set ticks
    ax.set_xticks([0, 25, 50, 75, 100, 125, 150, 175, 200, 225, 250],
        [0, 25, 50, 75, 100, 125, 150, 175, 200, 225, 250])
    ax.set_yticks([])

    plt.title("Sebessegmérés", fontdict = font1)
    plt.xlabel("Speed", fontdict = font2)
    plt.ylabel(f"{ms} ms", fontdict = font2)

    plt.text(2, 4, f"Target Speed: {int(data_zone[49])} KM/H\nWheel Speed: {wheel_speed[49]:.0f} KM/H", fontdict = font2)
    plt.grid(color = 'black', linestyle = '--', linewidth = 1)


if __name__ == '__main__':
    #open file for reading
    f = open("proba_adat.txt", "r")

    # start collections with zeros and make ypoints for all xpoints
    wheel_speed = collections.deque(np.zeros(ylim))
    wheel_speed_ypoints = range(0, ylim)

    data_zone = collections.deque(np.zeros(ylim))
    data_zone_ypoints = range(0, ylim)

    # define and adjust figure - bgcolor
    fig = plt.figure(figsize=(12,6), facecolor='#DEDEDE')
    ax = plt.subplot()
    ax.set_facecolor('#DEDEDE')

    # animate
    ani = FuncAnimation(fig, my_function, interval=ms)
    plt.show()

