import multiprocessing
import matplotlib.pyplot as plt
import numpy as np
import collections
import time
import sys 
from matplotlib.animation import FuncAnimation
from multiprocessing import Process
import gyorsulas_menu as menu
import Can_data_reader

#number of x and y-points -- refresh rate in ms -- error margin
error_margin = 4                #színváltáshoz
y_lim = 125                     #25-el osztható legyen
wheel_speed_x_limit = 6        #ezt kell megváltoztatni,hogy hol legyen a "karakter" - scan_idx - egggyel kissebb
scan_idx = wheel_speed_x_limit - 1
x_lim = wheel_speed_x_limit * 4
futas_darab_szam = 0
shared_value = multiprocessing.Value('d', 0.0)  #processek között megosztott változó

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
    p1 = Process(target=Can_data_reader.monitor_channel, args=(shared_value, ))
    p1.daemon = True #azért, hogy leálljon a programmal együtt a process
    p1.start()

    #paraméterek kiolvasása a menüből (log fájl neve , késleltetés ideje) 
    data_file_name, log_file_name, ms = menu.start()    
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