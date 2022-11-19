# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 15:34:32 2022

@author: Étienne
"""
import numpy as np
from mdf import mdf
try:
    from Parametres import *
except:
    pass
from inte_fluxBase import inte_fluxBase
from inte_fluxContour import inte_fluxContour
from analytique import ref_analytique
L = 1       # [m] Longueur
k = 1       # [W/m*K] Conductivité thermique
T_inf = 1     # [K] Température de l'air ambiant
T_w = 1     # [K] Température de base
R = 1       # [m] Rayon 
h = 1      # [W/m^2*K] Coefficient de convection
Bi = 1
N = 10       # [-] Nombre de points en z
    
prm = Parametres(L, k, T_inf, T_w, R, h, N)
print(mdf(2))
print(prm.R)
