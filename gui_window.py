import pandas as pd
import numpy as np
from live_df import LiveDF

#ldf = LiveDF()
#ldf._init_test_df()

from requests import get
from tkinter import Tk, Label, Button

from datetime import datetime
import os
import time
import threading

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 
from matplotlib.figure import Figure 

class MyFirstGUI:
    def __init__(self, master):
        self.master = master
        master.title('CryptoBOT')
        master.geometry('600x400')

        self.label = Label(self.master, text="This is our first GUI!")
        self.label.pack()

        self.startb = Button(self.master, text="Start", command=self.start_data)
        self.startb.pack()

        self.stopb = Button(self.master, text="Stop", command=self.stop_data)
        self.stopb.pack()
        self.stopb["state"] = "disabled"
        
        self.exitb = Button(self.master, text="Exit", command=self._exit)
        self.exitb.pack()
           
        self.ldf = LiveDF()
        self.exitf = False
        
        self.continuePlotting = False
        self.lab = Label(self.master, text="Live Plotting", bg = 'white').pack()   
        self.fig = Figure() 
        self.ax = self.fig.add_subplot(111) 
        self.ax.set_xlabel("DateTime") 
        self.ax.set_ylabel("Price") 
        self.ax.grid()
        self.graph = FigureCanvasTkAgg(self.fig, master=self.master) 
        self.graph.get_tk_widget().pack(side="top",fill='both',expand=True)
        
        #self.df = pd.DataFrame(data=self.time_window(), index=[0])
        
        #self.main_df = pd.DataFrame()
        #self.active_df_point = pd.DataFrame()       
        #self.loop = asyncio.get_event_loop()

    def start_data(self):
        self.ldf._init_test_df()
        self.ldf.start_data()
        print('start data ...')
        self.exitb["state"] = "disabled"
        self.startb["state"] = "disabled"
        self.stopb["state"] = "active"
        
        self.gui_handler()
                
    def stop_data(self):
        self.ldf.stop_data()
        print('stop data')
        self.stopb["state"] = "disabled"
        self.startb["state"] = "active"
        self.exitb["state"] = "active"
    
    def change_state(self):  
        if self.continuePlotting == True: 
            self.continuePlotting = False 
        else: 
            self.continuePlotting = True
    
    def plotter(self): 
        # waitin for signal and then get data
        #while self.continuePlotting:
        while not self.exitf:
            live_data = self.ldf.data_time_window(10)
            x_idx = list(live_data.index)
            x_ticks = list(live_data['Date'].astype(str))
            y = list(live_data['price_close'])
            
            print(x_idx)
            print(x_ticks)
            print(y)
            
            self.ax.cla() 
            self.ax.grid()
            
            # ADD REAL TIME DATA
            #dpts = data_points() 
            self.ax.plot(x_idx, y, marker='o', color='orange')
            
            self.ax.set_xticks(x_ticks)
            
            self.graph.draw() 
            time.sleep(1) 
 
    def gui_handler(self): 
        #self.change_state() 
        threading.Thread(target=self.plotter).start()
    
    def _exit(self):
        self.master.destroy()

root = Tk()
my_gui = MyFirstGUI(root)
root.mainloop()