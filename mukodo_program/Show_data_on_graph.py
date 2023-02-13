import multiprocessing
import matplotlib.pyplot as plt
import numpy as np
import collections
import time
import sys 
from matplotlib.animation import FuncAnimation
from multiprocessing import Process
#import gyorsulas_menu as menu
#import Can_data_reader
import shutil
from canlib import canlib
import tkinter as tk
from tkinter import ttk
from tkinter import *  
import os

#number of x and y-points -- refresh rate in ms -- error margin
error_margin = 4                #színváltáshoz
y_lim = 125                     #25-el osztható legyen
wheel_speed_x_limit = 6        #ezt kell megváltoztatni,hogy hol legyen a "karakter" - scan_idx - egggyel kissebb
scan_idx = wheel_speed_x_limit - 1
x_lim = wheel_speed_x_limit * 4
futas_darab_szam = 0
shared_value = multiprocessing.Value('d', 0.0)  #processek között megosztott változó


#can adatok kiolvasásához 2 függvény
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


def monitor_channel(shared_value):
    ticktime = 0
    ch = canlib.openChannel(0, bitrate = canlib.Bitrate.BITRATE_500K, flags=canlib.canOPEN_ACCEPT_VIRTUAL)
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


#menühöz 5 darab függvény
def getFolder():
   path = "./wltp_fajlok/"
   dir_list  = os.listdir(path)
   return dir_list 

def wltp_files(window, dir_list):
   tk.Label(window, text="WLTP fájlok:").grid(row = 0, column = 0, sticky = 'w')

   wltp_file = tk.StringVar()
   wltp_input = ttk.Combobox(window, width = 70, values = dir_list, state = "readonly", textvariable = wltp_file)
   wltp_input.grid(row = 0, column = 1, sticky = 'w')

   return wltp_file

def Log_fajl(window):
   tk.Label(window, text="Log fájl neve:").grid(row = 1, column = 0, sticky = 'w')

   LOG_fajl_nev = tk.StringVar()
   LOG_input = tk.Entry(window, width = 73, textvariable = LOG_fajl_nev)
   LOG_input.grid(row = 1, column = 1, sticky = 'w')

   return LOG_fajl_nev


def mintavetelezesi_gyakorisag(window):
   tk.Label(window, text="Mintavetelezési gyakoriság(ms):").grid(row = 2, column = 0, sticky = 'w')

   Mintavetelezesi_gyakorisag = tk.StringVar()

   Timing_input = tk.Spinbox(window, width = 71, from_=100, to=300, textvariable = Mintavetelezesi_gyakorisag)
   Timing_input.grid(row = 2, column = 1, sticky = 'w')

   return Mintavetelezesi_gyakorisag


def start(): 
   # creating window and setting attributes
   window = tk.Tk()
   window.state('zoomed')
   window.title("WLTP mérés")

   #creating components
   wltp_fajl = wltp_files(window, getFolder())
   LOG_fajl_nev = Log_fajl(window)
   Mintavetelezesi_gyakorisag = mintavetelezesi_gyakorisag(window)

   # Create Start button
   Button(window, text = 'Program indítása!', bd = '5', command = window.destroy).grid(row = 3, column = 0, columnspan = 2, sticky = 'n') 

   window.mainloop()

   return(("./wltp_fajlok/" + wltp_fajl.get()), LOG_fajl_nev.get(), int(Mintavetelezesi_gyakorisag.get()))


def lista_feltoltes(ms):
    #tengelyek listáinak létrehozása
    speed_list = []
    time_tick_list = []
    time_number_list = []

    #helyek, értékek meghatározása
    for x in range(0,6):
        speed_list.append(x * 25)
        time_tick_list.append(x * scan_idx)

    # x tengely számozása és azoknak helyeinek kialakítása
    time_number_list = [
        f"-{ms * scan_idx / 1000} s"
        ]
    for x in range(0,5):
        time_number_list.append(
            f"+{(x * ms * scan_idx) / 1000} s"
        )
    return speed_list, time_tick_list, time_number_list

#megállítás és kilépés
def on_press(event):
    if event.key.isspace():
        if anim.running:
            anim.event_source.stop()
        else:
            anim.event_source.start()
        anim.running ^= True
    elif event.key == 'q':
        anim.event_source.stop()
        sys.exit("Kilepes gomb")  
        

def plot_color():
    #wheel_speed and title color 
    if (int(target_speed[scan_idx]) + error_margin > int(wheel_speed[scan_idx]) and int(target_speed[scan_idx]) - error_margin < int(wheel_speed[scan_idx])):
        line_color = "green"
    elif (int(target_speed[scan_idx]) + (error_margin * 2) > int(wheel_speed[scan_idx]) and int(target_speed[scan_idx]) - (error_margin * 2) < int(wheel_speed[scan_idx])):
        line_color = "orange"
    else:
        line_color = "red"

    #target_speed-(left) and wheel_speed-(right) title color and position
    plt.title(f"{float(target_speed[scan_idx * 2])} KM/H (Target Speed)", size = 40, loc='left')
    plt.title(f"{wheel_speed[scan_idx]:.0f} KM/H (Wheel Speed)", size = 40, loc='right', c = line_color)

    # wheel_speed plotolása és színezése || függőleges vonal behúzása és színezése
    ax.plot(wheel_speed_xpoints, wheel_speed, linewidth = '20', color = line_color) 
    plt.axvline(x = scan_idx, color = line_color)


# function to update the data
def my_function(i, kezdes_ido, speed_list, time_tick_list, time_number_list):
    global futas_darab_szam
    futas_darab_szam = futas_darab_szam + 1

    # get data
    wheel_speed.popleft()
    wheel_speed.append(shared_value.value)

    target_speed.popleft()
    target_speed.append(float(read_data_file.readline().rstrip('\n')))

    # clear and set axis
    ax.cla()
    ax.set_ylim(0, y_lim)
    ax.set_xlim(0, x_lim)

    # plot target_speed
    ax.plot(target_speed_xpoints, target_speed, linewidth = '80')

    # tengely tickek létrehozása, beállítása
    ax.set_yticks(speed_list, speed_list)
    ax.set_xticks(time_tick_list, time_number_list)
    ax.yaxis.tick_right()
    ax.tick_params(axis='both', which='major', labelsize=25)
    ax.tick_params(axis='y', colors='darkred', size = 50)

    #színek beállítása
    plot_color()

    #calculate latency and wait for predetermined ms - a loop futásának darabszámával visszaosztva az egységnyi idő kiszámolására
    latency = time.time() - kezdes_ido
    while((latency * 1000)/futas_darab_szam < ms):
        latency = time.time() - kezdes_ido

    plt.xlabel(f"Latency: {(latency/futas_darab_szam) * 1000:.0f} ms || Pause: 'SPACE' || QUIT: 'Q'", size = 20)
    plt.ylabel("Speed", size = 20)
    plt.grid(color = 'black', linestyle = '--', linewidth = 1)

    #logging wheel speed into file
    write_log = open("./log_fajlok/" + log_file_name + ".txt", "a")
    write_log.write(f"{str(wheel_speed[wheel_speed_x_limit - 1])} \n")
    write_log.close()


if __name__ == '__main__':
    multiprocessing.freeze_support()
    #processként a beolvasás futtatása || megosztott változó átadásával
    #p1 = Process(target=Can_data_reader.monitor_channel, args=(shared_value, ))
    p1 = Process(target=monitor_channel, args=(shared_value, ))
    p1.daemon = True #azért, hogy leálljon a programmal együtt a process
    p1.start()

    #paraméterek kiolvasása a menüből (log fájl neve , késleltetés ideje) 
    data_file_name, log_file_name, ms = start()    
    read_data_file = open(data_file_name, "r")  #open file for reading

    # start collections with zeros and make xpoints for all ypoints
    wheel_speed = collections.deque(np.zeros(wheel_speed_x_limit))
    wheel_speed_xpoints = range(0, wheel_speed_x_limit)

    target_speed = collections.deque(np.zeros(x_lim))
    target_speed_xpoints = range(0, x_lim)

    # define and adjust figure - bgcolor
    fig = plt.figure(figsize=(12,6), facecolor='#DEDEDE')
    ax = plt.subplot()
    ax.set_facecolor('#DEDEDE')
    kezdes_ido = time.time()

    #listák létrehozása és feltöltése
    speed_list, time_tick_list, time_number_list = lista_feltoltes(ms)
    
    #billentyű lenyomások érzékelése
    fig.canvas.mpl_connect('key_press_event', on_press)

    # animate - fargs: paraméterek átadása
    anim = FuncAnimation(fig, my_function, cache_frame_data = False, interval = 0, fargs=(kezdes_ido,speed_list, time_tick_list, time_number_list,))

    anim.running = True
    anim.direction = +1

    plt.show()
    read_data_file.close()
    p1.join()