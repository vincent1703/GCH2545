# -*- coding: utf-8 -*-
""" Fonction integrant avec la methode des trapeze composes

Entrées:
    - x : vecteur des abscisses
    - y : vecteur des ordonnees 
    

Sortie:
    I : Somme de l'integrale de y sur l'ensemble du vecteur x
"""

import numpy as np
def inte_trapz(x,y):
  
    I=0
    for i in range(len(x)-1):
        I+= np.abs(x[i+1]-x[i])*(y[i]+y[i+1])/2
        
    return I
