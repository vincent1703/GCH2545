# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 16:40:11 2022

@author: Étienne
"""

class Parametres(object):
    L = 0       # [m] Longueur
    k = 0       # [W/m*K] Conductivité thermique
    T_inf = 0     # [K] Température de l'air ambiant
    T_w = 0     # [K] Température de base
    R = 0       # [m] Rayon 
    h = 0      # [W/m^2*K] Coefficient de convection
    Bi = 0
    N = 0       # [-] Nombre de points en z
    
    def __init__(self, L, k, T_inf, T_w, R, h, N):
        self.L = L
        self.k = k
        self.T_inf = T_inf
        self.T_w = T_w
        self.R = R
        self.h = h
        self.N = N
        self.Bi = 2*h*R/k
        
    def setBi(self,new_Bi):
        self.Bi = new_Bi
        self.h = self.Bi*self.k/(2*self.R)