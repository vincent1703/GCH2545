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
nr = 20     # [-] Nombre de points en z  "prendre plus que 20 n'est pas necessaire selon erreur avec analytique"
nz = 20
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
list_Bi = [0.05,0.1, 1, 10, 20, 100]

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
    if prm.Bi<200:
        T = ref_analytique(z,prm)
        plt.plot(z, T, '--r', label="Profil analytique")
    plt.legend()
    plt.title("Profil de température Bi: "+str(prm.Bi))
    plt.ylabel("Température (K)")
    plt.xlabel("Position z (m)")
    plt.savefig("ComparaisonProfilTemperature_Bi"+str(prm.Bi)+".png", dpi=400)
    plt.show()

#=========================2e analyse - Base=========================
list_Bi = np.linspace(.01,100,100)
r = np.linspace(prm.R, 0, prm.nr)
z = np.linspace(0, prm.L, prm.nz)
q_base_isole = []
q_base_convection = []
q_contour_isole = []
q_contour_convection_bout = []
q_contour_convection_sansbout = []
for i in range(len(list_Bi)):
    prm.setBi(list_Bi[i])
    prm.setCL("isole")
    A,b = mdf_assemblage(X,Y,prm)
    c = np.linalg.solve(A,b) 
    c_reshaped = c.reshape(prm.nz,prm.nr).transpose()
    T = c_reshaped
    q_base_isole.append(inte_fluxBase(T,r,prm))
    prm.setCL("convection")
    A,b = mdf_assemblage(X,Y,prm)
    c = np.linalg.solve(A,b) 
    c_reshaped = c.reshape(prm.nz,prm.nr).transpose()
    T = c_reshaped
    q_base_convection.append(inte_fluxBase(T,r,prm))
    bout = True
    D=2
    
    prm.setBi(list_Bi[i])
    prm.setCL("isole")
    A,b = mdf_assemblage(X,Y,prm)
    c = np.linalg.solve(A,b) 
    c_reshaped = c.reshape(prm.nz,prm.nr).transpose()
    T= c_reshaped
    q_contour_isole.append(inte_fluxContour(T,z,r,bout,D,prm))
    prm.setCL("convection")
    A,b = mdf_assemblage(X,Y,prm)
    c = np.linalg.solve(A,b) 
    c_reshaped = c.reshape(prm.nz,prm.nr).transpose()
    T = c_reshaped
    q_contour_convection_bout.append(inte_fluxContour(T,z,r,bout,D,prm))
    bout = False
    q_contour_convection_sansbout.append(inte_fluxContour(T,z,r,bout,D,prm))
    
plt.title("Q en fonction du nombre de Bi")    
plt.plot(list_Bi,q_base_isole,label="cond isole - flux base")  
plt.plot(list_Bi,q_base_convection,label="cond convection - flux base")  
plt.plot(list_Bi,q_contour_isole,label="cond isole - flux contour")  
plt.plot(list_Bi,q_contour_convection_sansbout,label="cond convection - flux contour") 
plt.plot(list_Bi,q_contour_convection_bout,'--', color="orange",label="cond convection + bout - flux contour") 
plt.ylabel("q (W)")
plt.xlabel("Bi") 
plt.legend()
plt.savefig("q_flux.png", dpi=400)
plt.show()
#=========================2e analyse - Contour=========================
list_Bi = np.linspace(.01,100,100)
q_contour_isole = []
q_contour_convection_bout = []
q_contour_convection_sansbout = []
q_analytique=[]
r = np.linspace(prm.R, 0, prm.nr)
z = np.linspace(0, prm.L, prm.nz)
for Bi_i in list_Bi:
    bout = True
    D=2
    
    prm.setBi(Bi_i)
    prm.setCL("isole")
    A,b = mdf_assemblage(X,Y,prm)
    c = np.linalg.solve(A,b) 
    c_reshaped = c.reshape(prm.nz,prm.nr).transpose()
    T= c_reshaped
    q_contour_isole.append(inte_fluxContour(T,z,r,bout,D,prm))
    prm.setCL("convection")
    A,b = mdf_assemblage(X,Y,prm)
    c = np.linalg.solve(A,b) 
    c_reshaped = c.reshape(prm.nz,prm.nr).transpose()
    T = c_reshaped
    q_contour_convection_bout.append(inte_fluxContour(T,z,r,bout,D,prm))
    bout = False
    q_contour_convection_sansbout.append(inte_fluxContour(T,z,r,bout,D,prm))
    D=1
    bout = False
    T = ref_analytique(z,prm)
    q_analytique.append(inte_fluxContour(T, z,r,bout,D, prm))

plt.title("Q en fonction du nombre de Bi et flux contour")    
plt.plot(list_Bi,q_contour_isole,label="cond isole")  
plt.plot(list_Bi,q_contour_convection_bout,'--', color="orange",label="cond convection + bout")  
plt.plot(list_Bi,q_contour_convection_sansbout,label="cond convection")  
plt.plot(list_Bi,q_analytique,'--r',label="analytique")  
plt.ylabel("q (W)")
plt.xlabel("Bi")
plt.legend()
plt.savefig("q_fluxContour.png", dpi=400)
plt.show()
# # =========================2e analyse - Erreur =========================
erreur=[]
for i in range(len(list_Bi)):
    erreur.append(abs(q_analytique[i]-q_contour_isole[i])/q_analytique[i]*100)
plt.title("Erreur entre analytique et isole flux contour")    
plt.plot(list_Bi,erreur,label="erreur")  
plt.ylabel("Pourcentage (%)")
plt.xlabel("Bi")
plt.legend()
plt.savefig("q_erreur_fluxContour.png", dpi=400)
plt.show()

# # =========================Analyse Bonus=========================
list_Bi = [0.1, 1, 10, 20, 100]

condition_limite = ["isole","convection"]
for Bi_i in list_Bi:
    for cl in condition_limite:
        prm.setBi(Bi_i)
        prm.setCL(cl)
        A,b = mdf_assemblage(X,Y,prm)
        c = np.linalg.solve(A,b)
        c_reshaped = c.reshape(prm.nz,prm.nr).transpose()
        fig,ax = plt.subplots(nrows=1,ncols=1)
        fig1 = ax.pcolormesh(x,y, c_reshaped)
        plt.colorbar(fig1, ax=ax)
        ax.set_title("Profil Temperature (K) Bi="+str(prm.Bi)+"CL="+str(prm.CL))
        ax.set_xlabel("Position z")
        ax.set_ylabel("Position r")
        plt.savefig("Profil2D_Bi"+str(prm.Bi)+"_"+str(prm.CL)+".png", dpi=400)
        plt.show()