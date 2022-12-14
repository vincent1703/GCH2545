# -*- coding: utf-8 -*-

class Parametres(object):
    L = 0       # [m] Longueur
    k = 0       # [W/m*K] Conductivité thermique
    T_inf = 0   # [K] Température de l'air ambiant
    T_w = 0     # [K] Température de base
    R = 0       # [m] Rayon 
    h = 0       # [W/m^2*K] Coefficient de convection
    Bi = 0      # Nombre de Biot [-]
    nr = 0      # Nombre de noeuds (direction radiale, r=0 à r=R)
    nz = 0      # Nombre de noeuds (direction axiale, de z=0 à z=L)
    CL = ""     # Condition limite ("isole" ou "convection")
    


    def __init__(self, L, k, T_inf, T_w, R, h, nr, nz,CL):
        self.L = L
        self.k = k
        self.T_inf = T_inf
        self.T_w = T_w
        self.R = R
        self.h = h
        self.Bi = 2*h*R/k
        self.nr = nr
        self.nz = nz        
        self.CL = CL
        
    # Fonction permettant la modification du nombre de Biot qui recalcule et 
    # definit le h correspondant 
    def setBi(self,new_Bi):
        self.Bi = new_Bi
        self.h = self.Bi*self.k/(2*self.R)
        
    # Fonction permettant la modification de la condition limite au bout de 
    # l'ailette
    def setCL(self, newCL):
        self.CL = newCL