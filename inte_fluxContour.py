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
        - T : Vecteur comprenant les températures  en Kelvin sur la longueur de l'ailette
                pour une combinaison géométrique donnée
        - z : Vecteur comprenant les points sur la longueur en mètre
        - prm : Objet class parametres()
            - k : Conductivité thermique
            - T_a : Température ambiante
            - T_w : Température du mur
            - h : Coefficient de convection
            - N : Nombre de points utilisés pour la méthode

    Sortie:
        - Valeur numérique de l'intégrale résultante (perte en W)
    """
    "T[r,z]"

    # Fonction à écrire
    # I=0
    # for i in range(1,len(z)):
    #     f_i = (T[-1,i]-prm.T_inf)*prm.h
    #     f_i_1 = (T[-1,i-1]-prm.T_inf)*prm.h
    #     I += (z[i]-z[i-1])*(f_i+f_i_1)/2
    # q = 2*np.pi*prm.R*I
    # return q# à compléter
    
    if D==2:
        q = 2*np.pi*prm.R*inte_trapz(z, prm.h*(T[0,:]-prm.T_inf))
    elif D==1:
        q = 2*np.pi*prm.R*inte_trapz(z, prm.h*(T-prm.T_inf))
    else:
        print("Specifiez le nb de dimensions de l'analyse.")
    
    if prm.CL=="convection" and bout == True and D==2 :
        #print(r*prm.h*(T[:,-1]-prm.T_inf))

        q_bout = 2*np.pi*inte_trapz(r, r*prm.h*(T[:,-1]-prm.T_inf))
        q=q+q_bout
        
        #print("q_bout: " + str(q_bout))    
    
    return q

