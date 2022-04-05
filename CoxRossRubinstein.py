# coding=utf8
import copy
import random
from math import *


# Implémentation du modèle de Cox-Rox-Rubinstein

# ---PARAMETRES

# Date d'échéance de l'option
N = 10

# Rendement certain de l'actif sans rique
r = 0.06

# Probabilité que le prix monte
# Remarque : le prix de l'option en t=0 ne dépend pas de la probabilité choisi
p = 0.2
q = 1-p

# Variations possibles du cours de l'actif risqué à chaque instant
# (On suppose que d<r<u, car sinon l’actif risqué serait systématiquement préféré à l'actif non risqué ou vice-versa)
u = 0.20
d = -0.10

# Valeur initiale de l'actif risqué
S0 = 1000

# Prix d'éxercice de l'option
K = S0


# ---CALCUL DU MODELE

# Simulation de l'arbre binomial des prix de l'actif risqué possibles

S = [[S0]]
for i in range(1, N+1):
    S.append([])
    for j in range(len(S[i-1])):
        S[i].append(S[i-1][j]*(1+u))
        S[i].append(S[i-1][j]*(1+d))


# Calcul des valeurs possibles des options d'achats

C = copy.deepcopy(S)
p0 = (d - r)/(d - u)
q0 = 1-p0

for i in range(len(C[N])):
    C[N][i] = max(0, C[N][i]-K)

for i in range(1, N+1):
    for j in range(len(C[N-i])):
        C[N-i][j] = 1/(1+r)*(p0*C[N-i+1][2*j] + q0*C[N-i+1][2*j+1])


# Calcul des valeurs possibles des options de vente à partir de la parité call-put

P = copy.deepcopy(C)
for i in range(len(P)):
    for j in range(len(P[i])):
        P[i][j] += K*(1+r)**(-(N-i)) - S[i][j]


# Calcul de la stratégie parfaite de couverture d'une option d'achat

H = []
H0 = []
for i in range(N):
    H.append([])
    H0.append([])
    for j in range(len(S[i])):
        H[i].append((1/(S[i][j]*(d-u))) * (C[i+1][2*j+1] - C[i+1][2*j]))
        H0[i].append((1/(u-d)*(1+r)**(i-1)) *
                     ((1+u)*C[i+1][2*j+1] - (1+d)*C[i+1][2*j]))

# ---SIMULATION D'UNE TRAJECTOIRE

_Chemin = [0]
_S = [S[0][0]]
_C = [C[0][0]]
_H = [H[0][0]]
_H0 = [H0[0][0]]

_V = [C[0][0]]

# Création d'un chemin aléatoire dans l'arbre binaire associé à l'ensemble des prix possibles
for i in range(1, N+1):
    delta = 0
    if random.uniform(0, 1) >= p:
        delta = 1
    _Chemin.append(2*_Chemin[i-1]+delta)
    _S.append(S[i][_Chemin[i]])
    _C.append(C[i][_Chemin[i]])
    if i != N:
        _H.append(H[i][_Chemin[i]])
        _H0.append(H[i][_Chemin[i]])
# Calcul de la valeur du portefeuille de la banque lorsque elle suit la stratégie de couverture parfaite
for i in range(1, N+1):
    cash = _V[i-1] - _H[i-1]*_S[i-1]  # autofinancement
    _V.append(_S[i]*_H[i-1] + cash*(1+r))


# ---AFFICHAGE DES RESULTATS

# Valeur d'une option d'achat en t = 0
print("Valeur d'une option d'achat en t = 0 : ", C[0][0])

"""# Valeur d'une option de vente en t = 0
print("Valeur d'une option de vente en t = 0 : ", P[0][0])"""

# Simulation du cours de l'actif risqué
print("Simulation du cours de l'actif risqué : ", _S)

# Quantité de l'actif risqué que doit possèder la banque à chaque instant
print("Quantité de l'actif risqué que doit possèder la banque à chaque instant 1,...,N: ", _H)

# Valeur du portefeuille de la banque à chaque instant
# Remarque : à l'échéance, la valeur du portefeuille de la banque est égal au payoff du call, ce qui justifie la couverture parfaite
print("Valeur du portefeuille de la banque à chaque instant : ",  _V)

# Payoff du call
print("Payoff du call : ", max(0, _S[N]-K))
