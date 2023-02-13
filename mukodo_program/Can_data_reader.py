#import argparse
import shutil

from canlib import canlib
from shared_memory_dict import SharedMemoryDict


def printframe(frame, width, shared_value):
    factor = 0.0075
    
    if(frame.id == 178):
        msg = bytearray(frame.data)

        front_right_wheel = (msg[7] << 8) | msg[6]
        front_right_wheel *= factor

        front_left_wheel = (msg[5] << 8) | msg[4]
        front_left_wheel *= factor

        avarage_speed = (front_right_wheel + front_left_wheel) / 2
        print("Avarage speed: ", avarage_speed)
        shared_value.value = avarage_speed


def monitor_channel(channel_number, bitrate, ticktime, shared_value):
    ch = canlib.openChannel(channel_number, bitrate=bitrate, flags=canlib.canOPEN_ACCEPT_VIRTUAL)
    ch.setBusOutputControl(canlib.canDRIVER_NORMAL)
    ch.busOn()

    width, height = shutil.get_terminal_size((80, 20))

    timeout = 0.5
    tick_countup = 0
    if ticktime <= 0:
        ticktime = None
    elif ticktime < timeout:
        timeout = ticktime

    print("Listening...")
    while True:
        try:
            frame = ch.read(timeout=int(timeout * 1000))
            printframe(frame, width, shared_value)
        except canlib.CanNoMsg:
            if ticktime is not None:
                tick_countup += timeout
                while tick_countup > ticktime:
                    print("tick")
                    tick_countup -= ticktime
        except KeyboardInterrupt:
            print("Stop.")
            break

    ch.busOff()
    ch.close()