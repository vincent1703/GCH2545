# Importation des modules
import numpy as np

def position(X,Y,prm):
    """ Fonction générant deux matrices de discrétisation de l'espace

    Entrées:
        - X : Bornes du domaine en r, X = [r_min, r_max]
        - Y : Bornes du domaine en z, Y = [z_min, z_max]
        - prm : Objet class parametres()
        #                 L : [m] Longueur
        #                 k : [W/m*K] Conductivité thermique
        #                 T_inf : [K] Température de l'air ambiant
        #                 T_w : [K] Température de base
        #                 R : [m] Rayon 
        #                 h :[W/m^2*K] Coefficient de convection
        #                 Bi : [Bi] Nombre de Biot
        #                 N : [-] Nombre de points 

    Sorties (dans l'ordre énuméré ci-bas):
        - x : Matrice (array) de dimension (nz x nr) qui contient la position en r
        - y : Matrice (array) de dimension (nz x nr) qui contient la position en z
            * Exemple d'une matrice position :
            * Si X = [-1, 1] et Y = [0, 1]
            * Avec nr = 3 et nz = 3
                x = [-1    0    1]
                    [-1    0    1]
                    [-1    0    1]

                y = [1    1    1  ]
                    [0.5  0.5  0.5]
                    [0    0    0  ]
    """
    # Recuperation de parametres 
    nr = prm.nr
    nz = prm.nz

    # Calcul des pas de discretisation
    dr = (Y[1] - Y[0]) / (nr-1)
    dz = (X[1] - X[0]) / (nz-1)

    
    x_ligne=np.linspace(X[0], X[1], nz)
    x = np.zeros([nr,nz])
    x[:,:] = x_ligne
    
    y_ligne = np.linspace(Y[0], Y[1], nr)
    y = np.zeros([nr,nz])
    y[:,:] = y_ligne
    y = y.T
    y = np.flipud(y)
    
        
# =============================================================================
#     ## ANCIEN CODE 
#     # x = np.zeros([nz,nr])
#     # y = np.zeros([nz,nr])
#     
#     # x[:,0] = X[0]
#     # x[:,-1] = X[1]
#     # for i in range(1, nr-1):
#     #     x[:,i] = x[:,i-1] + dr
#         
#     # y[0,:] = Y[1]
#     # y[-1,:] = Y[0]
#     # for j in range(1, nz-1):
#     #     y[j,:] = y[j-1,:] - dz
#     
# =============================================================================
    return x, y
    

# def mdf(prm):
#     """Fonction qui calcule le profil de température le long de l'ailette

#     Entrées:
#         - prm : Objet class parametres()
#                 L : [m] Longueur
#                 k : [W/m*K] Conductivité thermique
#                 T_inf : [K] Température de l'air ambiant
#                 T_w : [K] Température de base
#                 R : [m] Rayon 
#                 h :[W/m^2*K] Coefficient de convection
#                 Bi : [Bi] Nombre de Biot
#                 N : [-] Nombre de points 

#     Sorties (dans l'ordre énuméré ci-bas):
#         - Matrice donnant la température tout au long de l'ailette en Kelvin et le long de son rayon
#         - Matrice donnant la position tout au long de l'ailette (axe z) et le long de son rayon en mètre
#     """
#     L = prm.L       # [m] Longueur
#     k = prm.k        # [W/m*K] Conductivité thermique
#     T_inf = prm.T_inf      # [K] Température de l'air ambiant
#     T_w = prm.T_w      # [K] Température de base
#     R = prm.R        # [m] Rayon 
#     h = prm.h       # [W/m^2*K] Coefficient de convection
#     Bi = prm.Bi 
#     N = prm.N        # [-] Nombre de points en z

#     # Fonction à écrire
         
#     # Méthode des différences finies
#     Mat = np.zeros([N,N])
    
#     b = np.zeros(N)
#     x = np.linspace(0,L,N)
    
#     Mat[0,0] = 1
#     b[0] = T_w
#     b[-1] = 0
    
#     Mat[-1,-1] = 3
#     Mat[-1,-2] = -4
#     Mat[-1,-3] = 1
    
#     dz = L/(N-1)
#     w = -(2 + 4 * h * dz ** 2 / (D*k))
#     s = (-4*h * dz**2 * T_a)/(D*k)
    
#     for i in range(1,N-1):
#         Mat[i,i] = w
#         Mat[i,i-1] = 1
#         Mat[i,i+1] = 1
#         b[i] = s
        
#     T = np.linalg.solve(Mat,b)
    
#     return T, x      # à compléter

def mdf_assemblage(X,Y,prm):
    """ Fonction assemblant la matrice A et le vecteur b pour résoudre notre profil de température

    Entrées:
        - X : Bornes du domaine en x, X = [x_min, x_max]
        - Y : Bornes du domaine en y, Y = [y_min, y_max]
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
        #                 CL : condition limite, texte ("isole" ou "convection")

    Sorties (dans l'ordre énuméré ci-bas):
        - A : Matrice (array)
        - b : Vecteur (array)
    """
    # Representation de l'ailette (portion superieure, symetrique)
    #  
    #  CL = "isole" :
    #   
    #                     h @ T_inf         h @ T_inf
    #        i=0             ↗↗↗              ↗↗↗                   i=nz
    #    j=0 ________________________________________________________
    # ⭱      |                                                       |\
    # |  T_w |                                                       |\
    # R  q → |                                                       |\
    # |      |                                                       |\
    # ⭳      |_______________________________________________________|\
    #   j=nr \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    #       
    #        ⭰―――――――――――――――――――――――L――――――――――――――――――――――――――――――⭲
    #
    #
    #  CL = "convection" :
    #   
    #                     h @ T_inf         h @ T_inf
    #         i=0              ↗↗↗              ↗↗↗                 i=nz
    #    j=0  ________________________________________________________
    #  ⭱      |                                                       |
    #  |  T_w |                                                       | ↗ h @
    #  R  q → |                                                       | ↗ T_inf
    #  |      |                                                       | ↗
    #  ⭳      |_______________________________________________________|
    #    j=nr \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    #  
    #         ⭰―――――――――――――――――――――――L――――――――――――――――――――――――――――――⭲
    
    
    # Recuperation des parametres pour calculs
    nr = prm.nr
    nz = prm.nz
    T_w = prm.T_w
    T_inf = prm.T_inf
    R = prm.R
    L = prm.L
    h = prm.h
    k = prm.k
    Bi = prm.Bi
    CL = prm.CL
    
    N = nr*nz
    
    # Calculs des pas de discrtisation
    dr = (X[1] - X[0]) / (nr-1)
    dz = (Y[1] - Y[0]) / (nz-1)
    
    # Matrices de position pour indexation
    x, y = position(X,Y,prm)
    
    # Initialisation matrice et vecteur
    A = np.zeros([N,N])
    b = np.zeros(N)


    
    
    # Assemblage corps matrice
    for i in range(1, nr-1):
        for j in range(1, nz-1):        
            k =  i*nz + j
            
            A[k,k-nz] = -1/(x[j,i] * (2*dr)) + 1/(dr**2) 
            A[k,k-1] = 1/(dz**2)
            A[k,k] = -2/(dr**2) - 2/(dz)
            A[k,k+1] = 1/(dz**2)
            A[k,k+nz] = 1/(x[j,i] * (2*dr)) + 1/(dr**2)
    
    
    # Frontière gauche
    i = 0
    for j in range(0, nr):
        k = i * nr + j
        A[k,k] = 1
        b[k] = T_w
        
    # Frontière droite
    if CL=="isole":
        i = nz - 1
        for j in range(0, nr):
            k = i * nr + j
            A[k,k] = 3
            A[k,k-nr] = -4
            A[k,k-2*nr] = 1
            b[k] = 0
            
    elif CL=="convection":
        i = nz - 1
        for j in range(0, nr):
            k = i * nr + j
            A[k,k] = 3 + 2*dz*h/k
            A[k,k-nr] = -4
            A[k,k-2*nr] = 1
            b[k] = 2*dz*h*(T_inf)/k
    else:
        print("ERREUR: condition limite string non reconnu")
            
    # Frontière bas
    j = nr - 1
    for i in range(0, nz):
        k = i * nr + j
        A[k,k] = 3
        A[k,k-1] = -4
        A[k,k-2] = 1
        b[k] = 0
                   
            
    # Frontière haut
    j = 0
    for i in range(0, nz):
        k = i * nz + j
        A[k,k] = -3 + h*2*dr/k    
        A[k,k+1] = 4
        A[k,k+2] = -1
        b[k] = h*2*dr/k


    
    return A, b # à compléter

