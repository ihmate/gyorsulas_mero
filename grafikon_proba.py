import matplotlib.pyplot as plt
import numpy as np
import psutil
import collections

from matplotlib.animation import FuncAnimation
from shared_memory_dict import SharedMemoryDict

smd_config = SharedMemoryDict(name='config', size=1024)

# function to update the data
def my_function(i):
    # get data
    wheel_speed.popleft()
    wheel_speed.append(smd_config["status"])

    # clear axis
    ax.cla()

    # plot wheel_speed
    ax.plot(wheel_speed,ypoints)
    ax.scatter(len(wheel_speed)-1, wheel_speed[-1])
    ax.text(wheel_speed[-1]+2, len(wheel_speed)-1, "{}".format(wheel_speed[-1]))
    ax.set_ylim(0,9)
    ax.set_xlim(0,400)


if __name__ == '__main__':
    # start collections with zeros
    wheel_speed = collections.deque(np.zeros(10))
    ypoints = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    # define and adjust figure
    fig = plt.figure(figsize=(12,6), facecolor='#DEDEDE')
    ax = plt.subplot()
    ax.set_facecolor('#DEDEDE')

    # animate
    ani = FuncAnimation(fig, my_function, interval=100)
    plt.show()

