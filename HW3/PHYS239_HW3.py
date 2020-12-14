# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 02:44:56 2020

@author: Michael
"""

import math
import cmath
import matplotlib.pyplot as plt 
from scipy import signal
import numpy as np
import tkinter as tk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure

ELECTRON_MASS = 9.109E-31
ELECTRON_CHARGE = 1.602E-19
COULOMB_CONSTANT = 8.987E9

class Electron:
    
    def __init__(self, initial_distance, initial_velocity, impact_parameter):
        self.initial_distance = initial_distance
        self.initial_velocity = initial_velocity
        self.impact_parameter = impact_parameter
        
        self.time_list = [0]
        self.position_dict = {"x": [initial_distance], "y": [impact_parameter]}
        self.velocity_dict = {"x": [-initial_velocity], "y": [0]}
        
        self.acceleration_dict = {"x": [], "y":[]}
        
    def reset_electron(self):
        self.time_list = [0]
        self.position_dict = {"x": [self.initial_distance], "y": [self.impact_parameter]}
        self.velocity_dict = {"x": [self.initial_velocity], "y": [0]}
        
        self.acceleration_dict = {"x": [], "y":[]}
        
def fire_electron(electron, nucleus_charge, run_time, step_time):
    
    electron.reset_electron()
    number_of_steps = int(run_time / step_time)
    initial_x_acc, initial_y_acc = calculate_acceleration(nucleus_charge,
                                                          electron.initial_distance,
                                                          electron.impact_parameter)
    
    electron.acceleration_dict["x"].append(initial_x_acc)
    electron.acceleration_dict["y"].append(initial_y_acc)
    
    for step in range(1, number_of_steps + 1):
        current_time = step * step_time
        current_x_position = electron.position_dict["x"][step-1]
        current_y_position = electron.position_dict["y"][step-1]
        current_x_velocity = electron.velocity_dict["x"][step-1]
        current_y_velocity = electron.velocity_dict["y"][step-1]
        current_x_acc = electron.acceleration_dict["x"][step-1]
        current_y_acc = electron.acceleration_dict["y"][step-1]
        
        new_x_position = current_x_position + (current_x_velocity * step_time)
        new_y_position = current_y_position + (current_y_velocity * step_time)
        new_x_velocity = current_x_velocity + (current_x_acc * step_time)
        new_y_velocity = current_y_velocity + (current_y_acc * step_time)
        new_x_acc, new_y_acc = calculate_acceleration(nucleus_charge,
                                                      current_x_position,
                                                      current_y_position)
        
        
        electron.time_list.append(current_time)
        electron.position_dict["x"].append(new_x_position)
        electron.position_dict["y"].append(new_y_position)
        electron.velocity_dict["x"].append(new_x_velocity)
        electron.velocity_dict["y"].append(new_y_velocity)
        electron.acceleration_dict["x"].append(new_x_acc)
        electron.acceleration_dict["y"].append(new_y_acc)
        
        if new_x_position == 0 and new_y_position == 0:
            return
        
def calculate_acceleration(nucleus_charge, current_x_position, current_y_position):
    r_squared = current_x_position**2 + current_y_position**2
    r = math.sqrt(r_squared)
    r_cube = r**3

    force_x = -(COULOMB_CONSTANT * nucleus_charge * ELECTRON_CHARGE**2 / r_cube) * current_x_position
    force_y = -(COULOMB_CONSTANT * nucleus_charge * ELECTRON_CHARGE**2 / r_cube) * current_y_position
    
    acceleration_x = force_x / ELECTRON_MASS
    acceleration_y = force_y / ELECTRON_MASS
    
    return acceleration_x, acceleration_y
            
def graph_electron_path(electron):
    plt.figure(figsize=(10,10))
    electron_x_path = electron.position_dict["x"]
    electron_y_path = electron.position_dict["y"]
    
    r_list = []
    theta_list = []
    for position in range(0, len(electron_x_path)):
        current_x_pos = electron_x_path[position]
        current_y_pos = electron_y_path[position]
        
        c = complex(current_x_pos, current_y_pos)
        r,theta = cmath.polar(c)
        
        r_list.append(r)
        theta_list.append(theta)
    
    plt.polar(theta_list,r_list)
    
def get_psd(times, data):
    fsample = 1/np.nanmedian(np.diff(times))
    detrend = 'constant'
    nperseg = 2**7
    fs, Pxx = signal.welch(data, nperseg=nperseg, fs=fsample, detrend=detrend)
    return fs, Pxx

def convert_bohr_to_meter(distance):
    return distance * (5.29E-11)

def get_total_acc_list(x_acc_list, y_acc_list):
    acc_list = []
    for i in range(0, len(x_acc_list)):
        x_acc = x_acc_list[i]
        y_acc = y_acc_list[i]
        
        acc = math.sqrt(x_acc**2 + y_acc**2)
        acc_list.append(acc)
        
    return acc_list

def main_menu():
    fig_list = []
    canvas_list = []
    
    window_main_menu = tk.Tk()
    window_main_menu.lift()
    
    screen_width = window_main_menu.winfo_screenwidth()
    screen_height = window_main_menu.winfo_screenheight()
    
    window_main_menu.geometry("+{}+{}".format(int(screen_width/4), int(screen_height/6)))
                                              
    greeting = tk.Label(master=window_main_menu, text="PHYS 239 HW 3")
    greeting.grid(row=0, column=0)
    
    frm_left = tk.Frame(master=window_main_menu)
    frm_left.grid(row=1,column=0)
    
    frm_sliders= tk.Frame(master=frm_left)
    frm_sliders.grid(row=0, column=0)
    
    lbl_initial_distance = tk.Label(master=frm_sliders, text="Initial Distance (a_0)")
    lbl_initial_distance.grid(row=0, column=0)
    scl_initial_distance = tk.Scale(master=frm_sliders, from_=1, to=1000,
                         length=500, orient=tk.HORIZONTAL)
    scl_initial_distance.grid(row=0, column=1)
    
    lbl_impact_parameter = tk.Label(master=frm_sliders, text="Impact Parameter (a_0))")
    lbl_impact_parameter.grid(row=1, column=0)
    scl_impact_parameter = tk.Scale(master=frm_sliders, from_=1, to=1000,
                         length=500, orient=tk.HORIZONTAL)
    scl_impact_parameter.grid(row=1, column=1)
    
    lbl_initial_velocity = tk.Label(master=frm_sliders, text="Initial Velocity (m/s * 10^4))")
    lbl_initial_velocity.grid(row=2, column=0)
    scl_initial_velocity = tk.Scale(master=frm_sliders, from_=1, to=1000,
                         length=500, orient=tk.HORIZONTAL)
    scl_initial_velocity.grid(row=2, column=1)
    
    lbl_nucleus_charge = tk.Label(master=frm_sliders, text="Nucleus Charge (e-)")
    lbl_nucleus_charge.grid(row=3, column=0)
    scl_nucleus_charge = tk.Scale(master=frm_sliders, from_=1, to=100,
                         length=500, orient=tk.HORIZONTAL)
    scl_nucleus_charge.grid(row=3, column=1)
    
    frm_graphs_1 = tk.Frame(master=frm_left)
    frm_graphs_1.grid(row=2, column=0)
    
    fig_position = Figure(figsize=(6,4))
    ax_position = fig_position.add_subplot(111)
    ax_position.set_title("Electron Position")
    ax_position.set_ylabel("Distance from Atom (a_0)")
    ax_position.set_xlabel("Time (s)")
    canvas_position = FigureCanvasTkAgg(fig_position, master=frm_graphs_1)
    canvas_position.draw()
    canvas_position.get_tk_widget().grid(row=0, column=0)
    fig_list.append(fig_position)
    canvas_list.append(canvas_position)
    
    fig_velocity = Figure(figsize=(6,4))
    ax_velocity = fig_velocity.add_subplot(111)
    ax_velocity.set_title("Electron Velocity")
    ax_velocity.set_ylabel("Velocity (m/s * 10^4)")
    ax_velocity.set_xlabel("Time (s)")
    canvas_velocity = FigureCanvasTkAgg(fig_velocity, master=frm_graphs_1)
    canvas_velocity.draw()
    canvas_velocity.get_tk_widget().grid(row=0, column=1)
    fig_list.append(fig_velocity)
    canvas_list.append(canvas_velocity)
    
    fig_acc = Figure(figsize=(6,4))
    ax_acc = fig_acc.add_subplot(111)
    ax_acc.set_title("Electron Acceleration")
    ax_acc.set_ylabel("Acceleration (m/s)")
    ax_acc.set_xlabel("Time (s)")
    canvas_acc = FigureCanvasTkAgg(fig_acc, master=frm_graphs_1)
    canvas_acc.draw()
    canvas_acc.get_tk_widget().grid(row=1, column=0)
    fig_list.append(fig_acc)
    canvas_list.append(canvas_acc)
    
    fig_psd = Figure(figsize=(6,4))
    ax_psd = fig_psd.add_subplot(111)
    ax_psd.set_title("Electron PSD")
    ax_psd.set_ylabel("Power / Frequency")
    ax_psd.set_xlabel("Frequency (s)")
    canvas_psd = FigureCanvasTkAgg(fig_psd, master=frm_graphs_1)
    canvas_psd.draw()
    canvas_psd.get_tk_widget().grid(row=1, column=1)
    fig_list.append(fig_psd)
    canvas_list.append(canvas_psd)
    
    btn_calculate = tk.Button(master=frm_left, text="Calculate",
                              command=lambda:[calculate(scl_initial_distance,
                                                       scl_impact_parameter,
                                                       scl_initial_velocity,
                                                       scl_nucleus_charge,
                                                       fig_list, canvas_list)])
    btn_calculate.grid(row=1, column=0)
    
    window_main_menu.mainloop()

def calculate(scl_distance, scl_impact, scl_velocity, scl_charge, fig_list, canvas_list):
    initial_distance = convert_bohr_to_meter(scl_distance.get())
    impact_parameter = convert_bohr_to_meter(scl_impact.get())
    initial_velocity = scl_velocity.get() * 1E4
    nucleus_charge = scl_charge.get()
    
    electron = Electron(initial_distance, initial_velocity, impact_parameter)
    radius  = math.sqrt(initial_distance**2 + impact_parameter**2)
    rough_orbit_time = 2 * math.pi * radius / initial_velocity
    
    run_time = rough_orbit_time * 3
    step_time = run_time * 10E-7
    fire_electron(electron, nucleus_charge, run_time, step_time)
    
    t = electron.time_list
    x_pos = electron.position_dict["x"]
    y_pos = electron.position_dict["y"]
    x_v = electron.velocity_dict["x"]
    y_v = electron.velocity_dict["y"]
    x_acc = electron.acceleration_dict["x"]
    y_acc = electron.acceleration_dict["y"]
    acc_list = get_total_acc_list(x_acc, y_acc)

    fs, p = get_psd(t, acc_list)
    
    fig_list[0].clear()
    ax_position = fig_list[0].add_subplot(111)
    ax_position.set_title("Electron Position")
    ax_position.set_ylabel("Distance from Atom (a_0)")
    ax_position.set_xlabel("Time (s)")
    ax_position.plot(t, x_pos, label="x-axis")
    ax_position.plot(t, y_pos, label="y-axis")
    ax_position.legend()
    canvas_list[0].draw()
    
    fig_list[1].clear()
    ax_velocity = fig_list[1].add_subplot(111)
    ax_velocity.set_title("Electron Velocity")
    ax_velocity.set_ylabel("Velocity (m/s * 10^4)")
    ax_velocity.set_xlabel("Time (s)")
    ax_velocity.plot(t, x_v, label="x-axis")
    ax_velocity.plot(t, y_v, label="y-axis")
    ax_velocity.legend()
    canvas_list[1].draw()
    
    fig_list[2].clear()
    ax_acc = fig_list[2].add_subplot(111)
    ax_acc.set_title("Electron Acceleration")
    ax_acc.set_ylabel("Acceleration (m/s)")
    ax_acc.set_xlabel("Time (s)")
    ax_acc.plot(t, x_acc, label="x-axis")
    ax_acc.plot(t, y_acc, label="y-axis")
    ax_acc.legend()
    canvas_list[2].draw()
    
    fig_list[3].clear()
    ax_psd = fig_list[3].add_subplot(111)
    ax_psd.set_title("Electron PSD")
    ax_psd.set_ylabel("Power / Frequency")
    ax_psd.set_xlabel("Frequency (s)")
    ax_psd.loglog(fs, p)
    canvas_list[3].draw()
    
if __name__ == "__main__":
    main_menu()