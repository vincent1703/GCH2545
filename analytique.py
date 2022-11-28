# -*- coding: utf-8 -*-

import numpy as np

def ref_analytique(z,prm):
    """
    Parameters
    ----------
    z : Vecteur
        Vecteur comprenant les points sur la longueur en mètre
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

    Returns
    -------
    T : Vecteur
        Vecteur 1D comprenant la température sur la longueur en mètre.

    """
    m = np.sqrt(2*prm.h/(prm.k*prm.R))
    T = (prm.T_w-prm.T_inf)*(np.cosh(m*(prm.L-z))/np.cosh(m*prm.L))+prm.T_inf
    return T