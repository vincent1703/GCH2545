# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 17:12:07 2022

@author: Étienne
"""
import numpy as np
from functions.inte_trapz import inte_trapz

def inte_fluxBase(T,r,prm):
    """Fonction qui intègre la conduction de chaleur a travers la base de l'ailette

    Entrées:
        - T : Matrice comprenant les températures  en Kelvin sur la longueur et le rayon de l'ailette
                pour une combinaison géométrique donnée
        - r : Vecteur comprenant les points sur la direction radiale
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

   
    dz=prm.L/(prm.nz-1)
    dtdz=(-T[:,2]+4*T[:,1]-3*T[:,0])/(2*dz)
    q=2*np.pi*inte_trapz(r,-prm.k*r*(dtdz))
    
    
    return q