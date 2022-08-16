import argparse
import shutil

from canlib import canlib

bitrates = {
    '1M': canlib.Bitrate.BITRATE_1M,
    '500K': canlib.Bitrate.BITRATE_500K,
    '250K': canlib.Bitrate.BITRATE_250K,
    '125K': canlib.Bitrate.BITRATE_125K,
    '100K': canlib.Bitrate.BITRATE_100K,
    '62K': canlib.Bitrate.BITRATE_62K,
    '50K': canlib.Bitrate.BITRATE_50K,
    '83K': canlib.Bitrate.BITRATE_83K,
    '10K': canlib.Bitrate.BITRATE_10K,
}


def printframe(frame, width):
    factor = 0.0075
    msg = bytearray(frame.data)

    front_right_wheel = (msg[7] << 8) | msg[6]
    front_right_wheel *= factor

    front_left_wheel = (msg[5] << 8) | msg[4]
    front_left_wheel *= factor

    avarage_speed = (front_right_wheel + front_left_wheel) / 2

    print("Front left: ", front_left_wheel, "km/h, Front right: ", front_right_wheel, "km/h")
    print("Avarage speed: ", avarage_speed)


def monitor_channel(channel_number, bitrate, ticktime):
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
            printframe(frame, width)
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

# hol halgasson milyen beállításokkal
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Listen on a CAN channel and print all frames received."
    )
    parser.add_argument('channel', type=int, default=0, nargs='?')
    parser.add_argument(
        '--bitrate', '-b', default='500k', help=("Bitrate, one of " + ', '.join(bitrates.keys()))
    )
    parser.add_argument(
        '--ticktime',
        '-t',
        type=float,
        default=0,
        help=("If greater than zero, display 'tick' every this many seconds"),
    )
    parser.add_argument
    args = parser.parse_args()

    monitor_channel(args.channel, bitrates[args.bitrate.upper()], args.ticktime)