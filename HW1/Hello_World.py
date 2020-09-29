# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 23:48:21 2020

@author: Michael Randall
"""
from tkinter import Tk
from tkinter import messagebox

#Create dialogue box object and raise it to the topof the display
root = Tk()
root.lift()

#Create and display message box 
messagebox.showinfo("Hello", "Hello World!")

#Destroy the object after the message box is closed
root.destroy()