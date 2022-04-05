# coding=utf8
import copy
from scipy.stats import norm
from math import *

# On simule maintenant une option d'échéance T réelle en passant le modèle de Cox-Rox-Rubinstein
# "à la limite"

# ---PARAMETRES

# Echéance de l'option
T = 20

# Précision de la subdivision de l'interval de temps [0, T]
N = 20

# Rendement certain anualisé de l'actif sans risque
R = 0.06

# Probabilité que le prix monte
p = 0.5
q = 1-p

# Variations possibles du cours de l'actif risqué à chaque instant
# (On suppose que d<r<u, car sinon l’actif risqué serait systématiquement préféré à l'actif non risqué ou vice-versa)
u = 0.20
d = -0.10

# Valeur initiale de l'actif risqué
S0 = 1000

# Prix d'éxercice de l'option
K = S0

# ---FONCTION AUXILLIERE

def pnorm(q,mean=0,sd=1):
    """
    Calculates the cumulative of the normal distribution
    """
    result=norm.cdf(x=q,loc=mean,scale=sd)
    return result

# ---CALCUL DU MODELE

# Rendement certain de l'actif sans rique entre deux instants
r = R*T/N

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

# ---AFFICHAGE DES RESULTATS

print("N = ", N)
# Valeur d'une option d'achat en t = 0
print("Valeur d'une option d'achat en t = 0 : ", C[0][0])

"""# Valeur d'une option de vente en t = 0
print("Valeur d'une option de vente en t = 0 : ", P[0][0])"""

# Comparaison avec la valeur théorique

