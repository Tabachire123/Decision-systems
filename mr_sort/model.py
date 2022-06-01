import random
import numpy as np
from gurobipy import *
'''Implémentation d'un model MR sort à partir des équations données 

   dans les articles de documentation (cf. références)'''


def MRSortmodel(grades, nb_matieres, nb_classes):

## Initialisation des paramètres
    eps, M = 0.001 , 999999
    thresh = []

    model = Model()
    lmbda = model.addVar(lb = 0.5, ub = 1)
    w = model.addMVar(shape = nb_matieres, lb = 0, ub = 1)


##Définition des seuils
    for i in range(nb_matieres):
        thresh.append(model.addMVar(vtype = GRB.INTEGER, shape =nb_classes - 1, lb = 1, ub = 19))

    alpha = model.addVar(lb = -GRB.INFINITY, ub = GRB.INFINITY)
    model.update()

#Mise à jour du modèle et ajout de contraintes issues des équations
##Somme des poids égale à 1
    model.addConstr(sum(w) == 1)

    for i in range(nb_classes - 1):
        if i >= 1:
            for j in range(nb_matieres):
                model.addConstr(thresh[j].tolist()[i] >= thresh[j].tolist()[i - 1] + 1)

        for j in range(len(grades)):

            if grades[j][-1] == i + 1 or grades[j][-1] == i: # Condition ajout de contrainte si l'élève valide

                c = []
                sigmas = model.addVar(lb = -GRB.INFINITY, ub = GRB.INFINITY)
                model.update()
                model.addConstr(sigmas >= alpha)

                for k in range(nb_matieres):
                    deltas = model.addVar(vtype = GRB.INTEGER, lb = 0, ub = 1)
                    c.append(model.addVar(lb = 0, ub = 1))
                    model.update()

                    model.addConstr(c[-1] <= w.tolist()[k])
                    model.addConstr(c[-1] <= deltas)
                    model.addConstr(c[-1] >= deltas + w.tolist()[k] - 1)
                    model.addConstr(M*(deltas) + eps >= grades[j][k] - thresh[k].tolist()[i])
                    model.addConstr(M*(deltas - 1) <= grades[j][k] - thresh[k].tolist()[i])

                #
                if grades[j][-1] == i + 1:
                    model.addConstr(sum(c) == lmbda + sigmas)
                else:
                    model.addConstr(sum(c) + sigmas + eps == lmbda)

    model.update()
##ITERATIONS SUP
    model.setObjective(alpha, GRB.MAXIMIZE)
    model.params.OutputFlag = 0
    model.optimize()

    return w.X, lmbda.X, model.objVal, [thresh[i].X for i in range(nb_matieres)]
