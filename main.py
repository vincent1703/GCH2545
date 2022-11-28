# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 15:34:32 2022

@author: Étienne
"""
import numpy as np
import matplotlib.pyplot as plt

try:
    from Parametres import *
    from profil import *
except:
    pass
from inte_fluxBase import inte_fluxBase
from inte_fluxContour import inte_fluxContour
from analytique import ref_analytique

L = .2       # [m] Longueur
k = 10       # [W/m*K] Conductivité thermique
T_inf = 0+273.15     # [K] Température de l'air ambiant
T_w = 100+273.15     # [K] Température de base
R = .2       # [m] Rayon 
h = 1      # [W/m^2*K] Coefficient de convection
Bi = 1
nr = 100       # [-] Nombre de points en z
nz = 100
CL = "isole"
    
prm = Parametres(L, k, T_inf, T_w, R, h, nr, nz,CL)

# Paramètres
X = [0,prm.L]       #Position selon l'axe des z (rayon)
Y = [0,prm.R]       #Position selon l'axe des r

x,y = position(X, Y, prm)
#Conditons limites frontières à z=L

#Condion d'isolation

#Condition de convection

#=========================1ere analyse=========================
z = np.linspace(0, prm.L, prm.nz)
T = ref_analytique(z,prm)
#plt.plot(z, T, '--r', label="Profil analytique")
list_Bi = [0.05,0.1, 1, 10, 20, 100]
#list_Bi = [20]

for Bi_i in list_Bi:
    prm.setBi(Bi_i)
    A,b = mdf_assemblage(X,Y,prm)
    c = np.linalg.solve(A,b) 
    c_reshaped = c.reshape(prm.nz,prm.nr).transpose()
    c_R = c_reshaped[0,:].transpose()
    c_0 = c_reshaped[-1,:].transpose()
    # label_0 = "Profil r=0 "+str(prm.Bi)
    # label_R = "Profil r="+str(prm.R)+" Bi="+str(prm.Bi)
    label_0 = "Profil r=0 "
    label_R = "Profil r="+str(prm.R)
    plt.plot(x[0,:],c_R,label=label_R)  
    plt.plot(x[-1,:],c_0,label=label_0)  
    if prm.Bi<0.1:
        plt.plot(z, T, '--r', label="Profil analytique")
    plt.legend()
    plt.title("Profil de température Bi: "+str(prm.Bi))
    plt.ylabel("Température (K)")
    plt.xlabel("Position z (m)")
    plt.savefig("ComparaisonProfilTemperature_Bi"+str(prm.Bi)+".png", dpi=400)
    plt.show()

# plt.legend()
# plt.title("Profil de température")
# plt.ylabel("Température (K)")
# plt.xlabel("Position z (m)")
# plt.savefig("ComparaisonProfilTemperature.png", dpi=400)
# plt.show()
#=========================2e analyse - Base=========================



#=========================2e analyse - Contour=========================
# list_Bi = [0.1, 1, 10, 20, 100]
# z = np.linspace(0, prm.L, prm.nz)

# T = prm.T_w

# q_contour_isole = inte_fluxContour(T,z,prm)
# prm.setCL("convection")
# q_contour_convection = inte_fluxContour(T,z,prm)
# # =========================Analyse Bonus=========================
list_Bi = [0.1, 1, 10, 20, 100]
for Bi_i in list_Bi:
    prm.setBi(Bi_i)
    A,b = mdf_assemblage(X,Y,prm)
    c = np.linalg.solve(A,b)
    c_reshaped = c.reshape(prm.nz,prm.nr).transpose()
    fig,ax = plt.subplots(nrows=1,ncols=1)
    fig1 = ax.pcolormesh(x,y, c_reshaped)
    plt.colorbar(fig1, ax=ax)
    ax.set_title("Profil Bi="+str(prm.Bi))
    ax.set_xlabel("Position z")
    ax.set_ylabel("Position r")
    plt.savefig("Profil2D_Bi"+str(prm.Bi)+".png", dpi=400)
    plt.show()