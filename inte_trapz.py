# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 10:58:29 2022

@author: Vincent
"""
import numpy as np
def inte_trapz(x,y):
    # Entrees : x: vecteur des abscisses
    #           y: vecteur des ordonnees 
    
    I=0
    for i in range(len(x)-1):
        I+= (x[i+1]-x[i])*(y[i]+y[i+1])/2
        
    return I