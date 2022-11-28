# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 17:14:55 2022

@author: Étienne
"""

import numpy as np
from inte_trapz import inte_trapz

def inte_fluxContour(T,z,r,bout,D,prm):
    """Fonction qui intègre la convection sur la surface de l'ailette.

    Entrées:
        - T : Matrice 2D contenant les temperatures selon le rayon et la 
            longueur de l'ailette OU vecteur 1D avec les temperatures exterieures
            selon la longueur de l'ailette (si methode analytique et 1D)
        - z : Vecteur comprenant les points sur la longueur en mètre
        - r : Vecteur comprenant les points sur la direction radiale
        - bout : Valeur bouleene (True or False) determinant si on veut calculer
                ou non le transfert de chaleur par convection au bout de 
                l'ailette si les autres conditions sont satisfaites
        - D : Nombre de dimensions a analyser selon T (1 si analytique, 2
            si pas analytique)
            
        - prm : Objet class parametres()
        #                 L : [m] Longueur
        #                 k : [W/m*K] Conductivité thermique
        #                 T_inf : [K] Température de l'air ambiant
        #                 T_w : [K] Température de base
        #                 R : [m] Rayon 
        #                 h :[W/m^2*K] Coefficient de convection
        #                 Bi : [Bi] Nombre de Biot
        #                 nr : Nombre de noeuds (direction radiale, r=0 à r=R)
        #                 nz : Nombre de noeuds (direction axiale, de z=0 à z=L)
        #                 N : [-] Nombre de points 

    Sortie:
        - Valeur numérique de l'intégrale résultante (perte en W)
    """

    
    if D==2:
        q = 2*np.pi*prm.R*inte_trapz(z, prm.h*(T[0,:]-prm.T_inf))
    elif D==1:
        q = 2*np.pi*prm.R*inte_trapz(z, prm.h*(T-prm.T_inf))
    else:
        print("Specifiez le nb de dimensions de l'analyse (1 ou 2)")
    
    if prm.CL=="convection" and bout == True and D==2 :
        q_bout = 2*np.pi*inte_trapz(r, r*prm.h*(T[:,-1]-prm.T_inf))
        q=q+q_bout
 
    
    return q

