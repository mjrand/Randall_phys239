# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 23:48:21 2020

@author: Michael Randall
"""
from tkinter import Tk
from tkinter import messagebox

root = Tk()
root.lift()
messagebox.showinfo("Hello", "Hello World!")

root.destroy()