#!/usr/bin/env python
# coding: utf-8

# In[ ]:


"""Michael Randall
mrandall@ucsd.edu"""

import tkinter as tk
import math
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure

def convert_parsec_to_cm(number_to_convert):
    return number_to_convert * 3.086E18

def column_density_calculator(depth, density):
    """
    Calculates and returns a column density of an object
    
    params:
    depth (float): Depth of object in parsecs
    density (float): uniform density of object in cm^-3
    
    returns:
    column_densiy (float): column density of object in cm^-3
    """
    
    converted_depth = convert_parsec_to_cm(depth)
    
    column_density = converted_depth / density
    return column_density

def cross_section_calculator(optical_depth, depth, density):
    """
    Calculates the cross_section required for a given 
    optical depth, depth, and uniform density
    
    params:
    optical_depth (float): optical depth of an object
    depth (float): Depth of object in parsecs
    density (float): uniform density of object in cm^-3
    
    returns:
    cross_section (float): cross section implied by the above parameters
    """
    
    column_density = column_density_calculator(depth, density)
    
    cross_section = optical_depth / column_density
    return cross_section



def specific_intensity_calculator(initial_intensity, source_function, cross_section, density, depth):
    """
    Calculates the specific intensity of light passing through an object
    by applying the radiative transfer function at a number of steps defined
    by number_of_steps.
    
    params:
    initial_intensity (float): specific radiative intensity entering the object
    source_function (float): radiative source function of the object
    cross_section (float): cross section of interactions in the object in cm^2
    density (float): density of the object in cm^-3
    depth (float): distance light passes through in object in parsec
    
    returns:
    intensity_list [float]: list of specific intensities calculated at each step
    """
    number_of_steps = 100000
    converted_depth = convert_parsec_to_cm(depth)
    step_size = converted_depth / number_of_steps
    
    d_optical_depth = cross_section * density * step_size
    intensity_list = [initial_intensity]
    for step in range(0, number_of_steps):
        current_intensity = intensity_list[step]
        d_intensity = (source_function - current_intensity) * d_optical_depth

        new_intensity = current_intensity + d_intensity
        
        intensity_list.append(new_intensity)
    return intensity_list

def generate_cross_section_list_gaussian(frequency_list, gaussian_maximum_frequency,
                                    gaussian_maximum_cross_section, gaussian_width):
    
    gaussian_cross_section_list = []
    
    for frequency in frequency_list:
        cross_section = calculate_gaussian(frequency,
                                          gaussian_maximum_cross_section,
                                          gaussian_maximum_frequency,
                                          gaussian_width)
        
        gaussian_cross_section_list.append(cross_section)
        
    return gaussian_cross_section_list


def calculate_gaussian(x, a, b, c):
    return a * math.exp(-((x-b)**2)/(2*c**2))

def main_menu():
    
    window_main_menu = tk.Tk()
    window_main_menu.lift()
    
    screen_width = window_main_menu.winfo_screenwidth()
    screen_height = window_main_menu.winfo_screenheight()
    
    window_main_menu.geometry("+{}+{}".format(int(screen_width/2), int(screen_height/2)))
                                              
    greeting = tk.Label(master=window_main_menu, text="PHYS 239 HW 2")
    greeting.grid(row=0, column=0)

    frm_problems= tk.Frame(master=window_main_menu)
    frm_problems.grid(row=1, column=0)

    btn_problem_1 = tk.Button(master=frm_problems, text="Problem 1",
                              command=lambda:[window_main_menu.destroy(),problem_1()])
    btn_problem_1.grid(row=0, column=0)

    btn_problem_2 = tk.Button(master=frm_problems, text="Problem 2",
                             command=lambda:[window_main_menu.destroy(),problem_2()])
    
    btn_problem_2.grid(row=0, column=1)

    btn_problem_3 = tk.Button(master=frm_problems, text="Problem 3",
                             command=lambda:[window_main_menu.destroy(),problem_3()])
    btn_problem_3.grid(row=0, column=2)
    
    btn_problem_4 = tk.Button(master=frm_problems, text="Problem 4",
                             command=lambda:[window_main_menu.destroy(),problem_4()])
    btn_problem_4.grid(row=0, column=3)
    
    btn_exit = tk.Button(master=frm_problems, text="Exit",
                        command=window_main_menu.destroy)
    btn_exit.grid(row=0, column=4)

    window_main_menu.mainloop()

def problem_1():
    window_problem_1=tk.Tk()
    window_problem_1.lift()
    
    screen_width = window_problem_1.winfo_screenwidth()
    screen_height = window_problem_1.winfo_screenheight()
    
    window_problem_1.geometry("+{}+{}".format(int(screen_width/3), int(screen_height/3)))
    
    lbl_problem_1 = tk.Label(master=window_problem_1, text = """Use the sliders to vary the parameters.
    Use the buttons on the right to change the multiplier.
    Use the 'Calculate' button at the bottom to calculate!""")
    lbl_problem_1.grid(row=0, column=0)
    
    
    #start sliders code
    frm_sliders = tk.Frame(master=window_problem_1)
    frm_sliders.grid(row=1, column=0)
    
    ##depth slider
    lbl_depth = tk.Label(master=frm_sliders, text="Depth (parsec)")
    lbl_depth.grid(row=0, column=0)
    
    scl_depth = tk.Scale(master=frm_sliders, from_=1, to=1000,
                         length=500, orient=tk.HORIZONTAL)
    scl_depth.grid(row=0, column=1)
    
    lbl_depth_multiplier = tk.Label(master=frm_sliders, text="1")
    btn_depth_minus_three = tk.Button(master=frm_sliders, text="10^-3",
                              command=lambda:[set_multiplier(lbl_depth_multiplier, 1E-3),
                                              depress_button(btn_depth_minus_three),
                                              lift_button(btn_depth_one),
                                              lift_button(btn_depth_plus_three)])
    btn_depth_minus_three.grid(row=0,column=2)
    
    btn_depth_one = tk.Button(master=frm_sliders, text="   1   ", relief=tk.SUNKEN,
                              command=lambda:[set_multiplier(lbl_depth_multiplier, 1),
                                              lift_button(btn_depth_minus_three),
                                              depress_button(btn_depth_one),
                                              lift_button(btn_depth_plus_three)])
    btn_depth_one.grid(row=0,column=3)
    
    btn_depth_plus_three = tk.Button(master=frm_sliders, text="10^3",
                              command=lambda:[set_multiplier(lbl_depth_multiplier, 1E3),
                                              lift_button(btn_depth_minus_three),
                                              lift_button(btn_depth_one),
                                              depress_button(btn_depth_plus_three)])
    btn_depth_plus_three.grid(row=0,column=4)
       
    
    ##density slider
    lbl_density = tk.Label(master=frm_sliders, text="Density (cm^-3)")
    lbl_density.grid(row=1, column=0)
    
    scl_density = tk.Scale(master=frm_sliders, from_=1, to=1000,
                         length=500, orient=tk.HORIZONTAL)
    scl_density.grid(row=1, column=1)
    
    lbl_density_multiplier = tk.Label(master=frm_sliders, text="1")
    btn_density_minus_three = tk.Button(master=frm_sliders, text="10^-3",
                              command=lambda:[set_multiplier(lbl_density_multiplier, 1E-3),
                                              depress_button(btn_density_minus_three),
                                              lift_button(btn_density_one),
                                              lift_button(btn_density_plus_three)])
    btn_density_minus_three.grid(row=1,column=2)
    
    btn_density_one = tk.Button(master=frm_sliders, text="   1   ", relief=tk.SUNKEN,
                              command=lambda:[set_multiplier(lbl_density_multiplier, 1),
                                              lift_button(btn_density_minus_three),
                                              depress_button(btn_density_one),
                                              lift_button(btn_density_plus_three)])
    btn_density_one.grid(row=1,column=3)
    
    btn_density_plus_three = tk.Button(master=frm_sliders, text="10^3",
                              command=lambda:[set_multiplier(lbl_density_multiplier, 1E3),
                                              lift_button(btn_density_minus_three),
                                              lift_button(btn_density_one),
                                              depress_button(btn_density_plus_three)])
    btn_density_plus_three.grid(row=1,column=4)
    ##optical depth slider
    scl_optical_depth = tk.Scale(master=frm_sliders, from_=1, to=1000,
                         length=500, orient=tk.HORIZONTAL)
    scl_optical_depth.grid(row=2, column=1)
    
    lbl_optical_depth = tk.Label(master=frm_sliders, text="Optical depth")
    lbl_optical_depth.grid(row=2, column=0)
    
    lbl_optical_depth_multiplier = tk.Label(master=frm_sliders, text="1")
    btn_optical_depth_minus_three = tk.Button(master=frm_sliders, text="10^-3",
                              command=lambda:[set_multiplier(lbl_optical_depth_multiplier,1E-3),
                                              depress_button(btn_optical_depth_minus_three),
                                              lift_button(btn_optical_depth_one),
                                              lift_button(btn_optical_depth_plus_three)])
    
    btn_optical_depth_minus_three.grid(row=2,column=2)
    
    btn_optical_depth_one = tk.Button(master=frm_sliders, text="   1   ", relief=tk.SUNKEN,
                              command=lambda:[set_multiplier(lbl_optical_depth_multiplier,1),
                                              lift_button(btn_optical_depth_minus_three),
                                              depress_button(btn_optical_depth_one),
                                              lift_button(btn_optical_depth_plus_three)])
    btn_optical_depth_one.grid(row=2,column=3)
    
    btn_optical_depth_plus_three = tk.Button(master=frm_sliders, text="10^3",
                              command=lambda:[set_multiplier(lbl_optical_depth_multiplier,1E3),
                                              lift_button(btn_optical_depth_minus_three),
                                              lift_button(btn_optical_depth_one),
                                              depress_button(btn_optical_depth_plus_three)])
    btn_optical_depth_plus_three.grid(row=2,column=4)
    
    #calculation section
    frm_calculations = tk.Frame(master=window_problem_1)
    frm_calculations.grid(row=2, column=0)
    
    lbl_column_density = tk.Label(master=frm_calculations,
                                  text=f"Column Density (cm^-2) = {column_density_calculator(1,1)}")
    lbl_column_density.grid(row=0, column=0)
    
    lbl_cross_section = tk.Label(master=frm_calculations,
                                 text=f"Cross Section (cm^2) = {cross_section_calculator(1,1,1)}")
    lbl_cross_section.grid(row=1, column=0)
    
    #start buttons code
    btn_main_menu = tk.Button(master=window_problem_1, text="Main Menu",
                              command=lambda:[window_problem_1.destroy(), main_menu()])
    btn_main_menu.grid(row=3, column=1)
    
    btn_calculate = tk.Button(master=window_problem_1, text="Calculate",
                              command=lambda:[calculate_problem_1(lbl_column_density,
                                                                  lbl_cross_section,
                                                                  scl_depth, lbl_depth_multiplier,
                                                                  scl_density, lbl_density_multiplier,
                                                                  scl_optical_depth, lbl_optical_depth_multiplier)])
    btn_calculate.grid(row=3, column=0)
    
    window_problem_1.mainloop()
    

def calculate_problem_1(lbl_column_density,
                        lbl_cross_section,
                        scl_depth, lbl_depth_multiplier,
                        scl_density, lbl_density_multiplier,
                        scl_optical_depth, lbl_optical_depth_multiplier):
    
    depth = scl_depth.get() * float(lbl_depth_multiplier["text"]) 
    density = scl_density.get() * float(lbl_density_multiplier["text"]) 
    optical_depth = scl_optical_depth.get() * float(lbl_optical_depth_multiplier["text"]) 
    
    column_density = column_density_calculator(depth,density)
    cross_section = cross_section_calculator(optical_depth, depth, density)
    
    lbl_column_density["text"] = f"Column Density (cm^-2) = {column_density}"
    lbl_cross_section["text"] = f"Cross Section (cm^2) = {cross_section}"

def set_multiplier(lbl_multiplier, new_multiplier):
    lbl_multiplier["text"] = f"{new_multiplier}"

def lift_button(button):
    button.config(relief=tk.RAISED)
    
def depress_button(button):
    button.config(relief=tk.SUNKEN)
    
def problem_2():
    window_problem_1=tk.Tk()
    window_problem_1.lift()
    
    screen_width = window_problem_1.winfo_screenwidth()
    screen_height = window_problem_1.winfo_screenheight()
    
    window_problem_1.geometry("+{}+{}".format(int(screen_width/3), int(screen_height/3)))
    
    lbl_problem_1 = tk.Label(master=window_problem_1, text = """Use the sliders to vary the parameters.
    Use the buttons on the right to change the multiplier.
    Use the 'Calculate' button at the bottom to calculate!""")
    lbl_problem_1.grid(row=0, column=0)
    
    #start sliders code
    frm_sliders = tk.Frame(master=window_problem_1)
    frm_sliders.grid(row=1, column=0)
    
    ##depth slider
    lbl_depth = tk.Label(master=frm_sliders, text="Depth (parsec)")
    lbl_depth.grid(row=0, column=0)
    
    scl_depth = tk.Scale(master=frm_sliders, from_=1, to=1000,
                         length=500, orient=tk.HORIZONTAL)
    scl_depth.grid(row=0, column=1)
    
    lbl_depth_multiplier = tk.Label(master=frm_sliders, text="1")
    btn_depth_minus_three = tk.Button(master=frm_sliders, text="10^-3",
                              command=lambda:[set_multiplier(lbl_depth_multiplier, 1E-3),
                                              depress_button(btn_depth_minus_three),
                                              lift_button(btn_depth_one),
                                              lift_button(btn_depth_plus_three)])
    btn_depth_minus_three.grid(row=0,column=2)
    
    btn_depth_one = tk.Button(master=frm_sliders, text="   1   ", relief=tk.SUNKEN,
                              command=lambda:[set_multiplier(lbl_depth_multiplier, 1),
                                              lift_button(btn_depth_minus_three),
                                              depress_button(btn_depth_one),
                                              lift_button(btn_depth_plus_three)])
    btn_depth_one.grid(row=0,column=3)
    
    btn_depth_plus_three = tk.Button(master=frm_sliders, text="10^3",
                              command=lambda:[set_multiplier(lbl_depth_multiplier, 1E3),
                                              lift_button(btn_depth_minus_three),
                                              lift_button(btn_depth_one),
                                              depress_button(btn_depth_plus_three)])
    btn_depth_plus_three.grid(row=0,column=4)
       
    
    ##density slider
    lbl_density = tk.Label(master=frm_sliders, text="Density (cm^-3)")
    lbl_density.grid(row=1, column=0)
    
    scl_density = tk.Scale(master=frm_sliders, from_=1, to=1000,
                         length=500, orient=tk.HORIZONTAL)
    scl_density.grid(row=1, column=1)
    
    lbl_density_multiplier = tk.Label(master=frm_sliders, text="1")
    btn_density_minus_three = tk.Button(master=frm_sliders, text="10^-3",
                              command=lambda:[set_multiplier(lbl_density_multiplier, 1E-3),
                                              depress_button(btn_density_minus_three),
                                              lift_button(btn_density_one),
                                              lift_button(btn_density_plus_three)])
    btn_density_minus_three.grid(row=1,column=2)
    
    btn_density_one = tk.Button(master=frm_sliders, text="   1   ", relief=tk.SUNKEN,
                              command=lambda:[set_multiplier(lbl_density_multiplier, 1),
                                              lift_button(btn_density_minus_three),
                                              depress_button(btn_density_one),
                                              lift_button(btn_density_plus_three)])
    btn_density_one.grid(row=1,column=3)
    
    btn_density_plus_three = tk.Button(master=frm_sliders, text="10^3",
                              command=lambda:[set_multiplier(lbl_density_multiplier, 1E3),
                                              lift_button(btn_density_minus_three),
                                              lift_button(btn_density_one),
                                              depress_button(btn_density_plus_three)])
    btn_density_plus_three.grid(row=1,column=4)
    ##cross slider
    lbl_cross = tk.Label(master=frm_sliders, text="Cross section (cm^2)")
    lbl_cross.grid(row=2, column=0)
    
    scl_cross = tk.Scale(master=frm_sliders, from_=1, to=1000,
                         length=500, orient=tk.HORIZONTAL)
    scl_cross.grid(row=2, column=1)
    
    lbl_cross_multiplier = tk.Label(master=frm_sliders, text="10E-19")
    btn_cross_minus_three = tk.Button(master=frm_sliders, text="10^-16",
                              command=lambda:[set_multiplier(lbl_cross_multiplier, 1E-16),
                                              depress_button(btn_cross_minus_three),
                                              lift_button(btn_cross_one),
                                              lift_button(btn_cross_plus_three)])
    btn_cross_minus_three.grid(row=2,column=2)
    
    btn_cross_one = tk.Button(master=frm_sliders, text="10^-19", relief=tk.SUNKEN,
                              command=lambda:[set_multiplier(lbl_cross_multiplier, 1E-19),
                                              lift_button(btn_cross_minus_three),
                                              depress_button(btn_cross_one),
                                              lift_button(btn_cross_plus_three)])
    btn_cross_one.grid(row=2,column=3)
    
    btn_cross_plus_three = tk.Button(master=frm_sliders, text="10^-22",
                              command=lambda:[set_multiplier(lbl_cross_multiplier, 1E-22),
                                              lift_button(btn_cross_minus_three),
                                              lift_button(btn_cross_one),
                                              depress_button(btn_cross_plus_three)])
    btn_cross_plus_three.grid(row=2,column=4)
       
    
    ##density slider
    lbl_intensity = tk.Label(master=frm_sliders, text="Initial Intensity (W/cm^2)")
    lbl_intensity.grid(row=3, column=0)
    
    scl_intensity = tk.Scale(master=frm_sliders, from_=1, to=1000,
                         length=500, orient=tk.HORIZONTAL)
    scl_intensity.grid(row=3, column=1)
    
    lbl_intensity_multiplier = tk.Label(master=frm_sliders, text="1")
    btn_intensity_minus_three = tk.Button(master=frm_sliders, text="10^-3",
                              command=lambda:[set_multiplier(lbl_intensity_multiplier, 1E-3),
                                              depress_button(btn_intensity_minus_three),
                                              lift_button(btn_intensity_one),
                                              lift_button(btn_intensity_plus_three)])
    btn_intensity_minus_three.grid(row=3,column=2)
    
    btn_intensity_one = tk.Button(master=frm_sliders, text="   1   ", relief=tk.SUNKEN,
                              command=lambda:[set_multiplier(lbl_intensity_multiplier, 1),
                                              lift_button(btn_intensity_minus_three),
                                              depress_button(btn_intensity_one),
                                              lift_button(btn_intensity_plus_three)])
    btn_intensity_one.grid(row=3,column=3)
    
    btn_intensity_plus_three = tk.Button(master=frm_sliders, text="10^3",
                              command=lambda:[set_multiplier(lbl_intensity_multiplier, 1E3),
                                              lift_button(btn_intensity_minus_three),
                                              lift_button(btn_intensity_one),
                                              depress_button(btn_intensity_plus_three)])
    btn_intensity_plus_three.grid(row=3,column=4)
    ##optical depth slider
    scl_source = tk.Scale(master=frm_sliders, from_=1, to=1000,
                         length=500, orient=tk.HORIZONTAL)
    scl_source.grid(row=4, column=1)
    
    lbl_source = tk.Label(master=frm_sliders, text="Source Function")
    lbl_source.grid(row=4, column=0)
    
    lbl_source_multiplier = tk.Label(master=frm_sliders, text="1")
    btn_source_minus_three = tk.Button(master=frm_sliders, text="10^-3",
                              command=lambda:[set_multiplier(lbl_source_multiplier,1E-3),
                                              depress_button(btn_source_minus_three),
                                              lift_button(btn_source_one),
                                              lift_button(btn_source_plus_three)])
    
    btn_source_minus_three.grid(row=4,column=2)
    
    btn_source_one = tk.Button(master=frm_sliders, text="   1   ", relief=tk.SUNKEN,
                              command=lambda:[set_multiplier(lbl_source_multiplier,1),
                                              lift_button(btn_source_minus_three),
                                              depress_button(btn_source_one),
                                              lift_button(btn_source_plus_three)])
    btn_source_one.grid(row=4,column=3)
    
    btn_source_plus_three = tk.Button(master=frm_sliders, text="10^3",
                              command=lambda:[set_multiplier(lbl_source_multiplier,1E3),
                                              lift_button(btn_source_minus_three),
                                              lift_button(btn_source_one),
                                              depress_button(btn_source_plus_three)])
    btn_source_plus_three.grid(row=4,column=4)
    
    #calculation section
    frm_calculations = tk.Frame(master=window_problem_1)
    frm_calculations.grid(row=2, column=0)
    
    lbl_final_intensity = tk.Label(master=frm_calculations,
                                  text=f"Final Intensity (W/cm^2) = {specific_intensity_calculator(1,1,1E-19,1,1)[-1]}")
    lbl_final_intensity.grid(row=0, column=0)
   
    #start buttons code
    btn_main_menu = tk.Button(master=window_problem_1, text="Main Menu",
                              command=lambda:[window_problem_1.destroy(), main_menu()])
    btn_main_menu.grid(row=3, column=1)
    
    btn_calculate = tk.Button(master=window_problem_1, text="Calculate",
                              command=lambda:[calculate_problem_2(lbl_final_intensity,
                                                                  scl_depth, lbl_depth_multiplier,
                                                                  scl_density, lbl_density_multiplier,
                                                                  scl_cross, lbl_cross_multiplier,
                                                                  scl_intensity, lbl_intensity_multiplier,
                                                                  scl_source, lbl_source_multiplier)])
    btn_calculate.grid(row=3, column=0)
    
    window_problem_1.mainloop()
    
def calculate_problem_2(lbl_final_intensity,
                        scl_depth, lbl_depth_multiplier,
                        scl_density, lbl_density_multiplier,
                        scl_cross, lbl_cross_multiplier,
                        scl_intensity, lbl_intensity_multiplier,
                        scl_source, lbl_source_multiplier):
    
    depth = scl_depth.get() * float(lbl_depth_multiplier["text"]) 
    density = scl_density.get() * float(lbl_density_multiplier["text"]) 
    cross = scl_cross.get() * float(lbl_cross_multiplier["text"]) 
    intensity = scl_intensity.get() * float(lbl_intensity_multiplier["text"]) 
    source = scl_source.get() * float(lbl_source_multiplier["text"]) 
    
    final_intensity = specific_intensity_calculator(intensity, source, cross, density, depth)
    
    lbl_final_intensity["text"] = f"Final Intensity (W/cm^2) = {final_intensity[-1]}"
        
    
def problem_3():
    frequency_list = []
    
    for i in range(0,100):
        frequency_list.append(i)
        
    cross_list = generate_cross_section_list_gaussian(frequency_list, 1, 1, 1)
    fig = Figure(figsize=(6,6))
    ax = fig.add_subplot(111)
    ax.set_title("Gaussian Cross Section)")
    ax.set_ylabel("Cross Section (cm^2 * 10^-19)")
    ax.set_xlabel("Frequency (Hz)")
    ax.plot(frequency_list, cross_list)
    
    window_problem_3=tk.Tk()
    
    screen_width = window_problem_3.winfo_screenwidth()
    screen_height = window_problem_3.winfo_screenheight()
    
    window_problem_3.geometry("+{}+{}".format(int(screen_width/3), int(screen_height/3)))

    lbl_problem_3 = tk.Label(master=window_problem_3, text = "Change the paramaters and press update to update the graph!")
    lbl_problem_3.grid(row=0, column=0)
    
    #start sliders code
    frm_sliders = tk.Frame(master=window_problem_3)
    frm_sliders.grid(row=1, column=0)
    
    ##cross slider
    lbl_cross = tk.Label(master=frm_sliders, text="Maximum Cross Section (cm^2 * 10^-19)")
    lbl_cross.grid(row=0, column=0)
    
    scl_cross = tk.Scale(master=frm_sliders, from_=1, to=1000,
                         length=500, orient=tk.HORIZONTAL)
    scl_cross.grid(row=0, column=1)
    
    ##depth slider
    lbl_gauss_max = tk.Label(master=frm_sliders, text="Gaussian max frequency (Hz)")
    lbl_gauss_max.grid(row=1, column=0)
    
    scl_gauss_max = tk.Scale(master=frm_sliders, from_=1, to=100,
                         length=500, orient=tk.HORIZONTAL)
    scl_gauss_max.grid(row=1, column=1)
    
    ##depth slider
    lbl_gauss_width = tk.Label(master=frm_sliders, text="Gaussian width at half maximum (Hz)")
    lbl_gauss_width.grid(row=2, column=0)
    
    scl_gauss_width = tk.Scale(master=frm_sliders, from_=1, to=100,
                         length=500, orient=tk.HORIZONTAL)
    scl_gauss_width.grid(row=2, column=1)
    
        
    canvas = FigureCanvasTkAgg(fig, master=window_problem_3)
    canvas.draw()
    canvas.get_tk_widget().grid(row=2, column=0)
    
    btn_update = tk.Button(master=window_problem_3, text="Update",
                              command=lambda:[calculate_problem_3(frequency_list,
                                                                  scl_cross,
                                                                  scl_gauss_max,
                                                                  scl_gauss_width,
                                                                  fig, canvas)])
    btn_update.grid(row=3, column=0)
    
    btn_main_menu = tk.Button(master=window_problem_3, text="Main Menu",
                              command=lambda:[window_problem_3.destroy(), main_menu()])
    btn_main_menu.grid(row=3, column=1)
    
    window_problem_3.mainloop()
    
def calculate_problem_3(frequency_list, scl_cross, scl_gauss_max, scl_gauss_width, fig, canvas):
    cross = scl_cross.get()
    gauss_max = scl_gauss_max.get()
    gauss_width = scl_gauss_width.get()
    
    cross_list = generate_cross_section_list_gaussian(frequency_list, gauss_max, cross, gauss_width)
    
    fig.clear()
    ax = fig.add_subplot(111)
    ax.set_title("Gaussian Cross Section (cm^2 * 10^-19)")
    ax.set_ylabel("Cross Section (cm^2)")
    ax.set_xlabel("Frequency (Hz)")
    ax.plot(frequency_list, cross_list)
    canvas.draw()
    
def problem_4():
    depth = 1
    density = 1
    frequency_list = []
    
    for i in range(0,100):
        frequency_list.append(i)
    
    low_cross_list = make_low_cross_list(frequency_list, depth, density)
    high_cross_list = make_high_cross_list(frequency_list, depth, density)
    gauss_cross_list = generate_cross_section_list_gaussian(frequency_list, 0, high_cross_list[0], 10) 
    fig = Figure(figsize=(6,6))
 
    window_problem_4=tk.Tk()
    
    screen_width = window_problem_4.winfo_screenwidth()
    screen_height = window_problem_4.winfo_screenheight()
    
    window_problem_4.geometry("+{}+{}".format(int(screen_width/3), int(screen_height/3)))

    lbl_problem_4 = tk.Label(master=window_problem_4, text = """Press a Button to change the plot parameters! Loading takes a few seconds!""")
    lbl_problem_4.grid(row=0, column=0)
    
    canvas = FigureCanvasTkAgg(fig, master=window_problem_4)
    canvas.draw()
    canvas.get_tk_widget().grid(row=1, column=0)
    
    frm_button = tk.Frame(master=window_problem_4)
    frm_button.grid(row=2, column=0)
    
    btn_a = tk.Button(master=frm_button, text="   A   ",
                              command=lambda:[calculate_problem_4(frequency_list, 
                                                                  low_cross_list,
                                                                  0, 1, depth, density,
                                                                  fig, canvas)])
    btn_a.grid(row=0, column=0)
    
    btn_b = tk.Button(master=frm_button, text="   B   ",
                              command=lambda:[calculate_problem_4(frequency_list, 
                                                                  low_cross_list,
                                                                  10, 1, depth, density,
                                                                  fig, canvas)])
    btn_b.grid(row=0, column=1)
    
    btn_c = tk.Button(master=frm_button, text="   C   ",
                              command=lambda:[calculate_problem_4(frequency_list, 
                                                                  low_cross_list,
                                                                  1, 10, depth, density,
                                                                  fig, canvas)])
    btn_c.grid(row=0, column=2)
    
    btn_d = tk.Button(master=frm_button, text="   D   ",
                              command=lambda:[calculate_problem_4(frequency_list, 
                                                                  high_cross_list,
                                                                  10, 1, depth, density,
                                                                  fig, canvas)])
    btn_d.grid(row=0, column=3)
    
    btn_e = tk.Button(master=frm_button, text="   E   ",
                              command=lambda:[calculate_problem_4(frequency_list, 
                                                                  gauss_cross_list,
                                                                  1, 10, depth, density,
                                                                  fig, canvas)])
    btn_e.grid(row=0, column=4)
    
    btn_f = tk.Button(master=frm_button, text="   F   ",
                              command=lambda:[calculate_problem_4(frequency_list, 
                                                                  gauss_cross_list,
                                                                  10, 1, depth, density,
                                                                  fig, canvas)])
    btn_f.grid(row=0, column=5)
    
    
    
    btn_main_menu = tk.Button(master=frm_button, text="Main Menu",
                              command=lambda:[window_problem_4.destroy(), main_menu()])
    btn_main_menu.grid(row=0, column=6)
    
    window_problem_4.mainloop()

def make_low_cross_list(frequency_list, depth, density):
    new_cross_list = []
    for frequency in frequency_list:
        cross = 0.1 / (convert_parsec_to_cm(depth) * density)
        new_cross_list.append(cross)
    
    return new_cross_list

def make_high_cross_list(frequency_list, depth, density):
    new_cross_list = []
    for frequency in frequency_list:
        cross = 100 / (convert_parsec_to_cm(depth) * density)
        new_cross_list.append(cross)
    
    return new_cross_list
    
def calculate_problem_4(frequency_list, cross_list, intensity, source, depth, density, fig, canvas):
    final_intensity_list = []
    
    for i in range (0, len(frequency_list)):
        final_intensity = specific_intensity_calculator(intensity, source, cross_list[i], density, depth)[-1]
        final_intensity_list.append(final_intensity)
    
    fig.clear()
    ax = fig.add_subplot(111)
    ax.set_title(f"Intensity = {intensity}, Source = {source}")
    ax.set_ylabel("Specific Intensity (at D)")
    ax.set_xlabel("Frequency (Hz)")
    ax.plot(frequency_list, final_intensity_list)
    canvas.draw() 
    
if __name__ == "__main__":
    main_menu()


# In[ ]:




