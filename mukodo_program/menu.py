# importing tkinter for gui
import tkinter as tk
from tkinter import ttk
from tkinter import *  
import os

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

   Timing_input = tk.Spinbox(window, width = 71, from_=1, to=300, textvariable = Mintavetelezesi_gyakorisag)
   Timing_input.grid(row = 2, column = 1, sticky = 'w')

   return Mintavetelezesi_gyakorisag


def start(): 
   # creating window and setting attributes
   window = tk.Tk()
   window.state('zoomed')
   window.title("Hőmérés")

   #creating components
   wltp_fajl = wltp_files(window, getFolder())
   LOG_fajl_nev = Log_fajl(window)
   Mintavetelezesi_gyakorisag = mintavetelezesi_gyakorisag(window)

   # Create Start button
   Button(window, text = 'Program indítása!', bd = '5', command = window.destroy).grid(row = 3, column = 0, columnspan = 2, sticky = 'n') 

   window.mainloop()

   return(("./wltp_fajlok/" + wltp_fajl.get()), LOG_fajl_nev.get(), int(Mintavetelezesi_gyakorisag.get()))