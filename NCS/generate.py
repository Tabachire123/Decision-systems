import numpy as np
import os
import random


nb_matieres = 5
nb_classes = 2
nb_instances = 100
bruit= 0

def parameters(nb_matieres,nb_classes,nb_instances):
    lmbda=random.uniform(0.5, 0.75)
    frontiers = []
    for i in range(nb_matieres):
        randomFrontiers = random.sample(range(1, 20), nb_classes - 1)
        randomFrontiers.sort()
        frontiers.append(randomFrontiers)
    weights = [random.uniform(0, 1) for i in range(nb_matieres)]
    weights = [weight/sum(weights) for weight in weights]
    return lmbda,frontiers,weights



def creation_note(parametres_default):
    frontiers=parametres_default["criteres_note"]
    weights=parametres_default['w']
    lmbda=parametres_default['lmbda']
    res=[]
    notes = [random.randint(0, 20) for matiere in range(nb_matieres)]
    accepted=0
    for j in range(nb_classes - 1):
            somme = 0
            for k in range(nb_matieres):
                if notes[k] >= frontiers[k][j]:
                    somme += weights[k]
            if somme >= lmbda:
                accepted += 1
    res.append(notes + [accepted])

    return res


def generate_data(nb_matiere,nb_classes,nb_instances):
    data_list = []
    lmbda,frontiers,weights=parameters(nb_matiere,nb_classes,nb_instances)

    parametres_default = {
    "n_matiere": nb_matiere,
    "n_critere": nb_classes,
    "criteres_note": frontiers,
    "w": weights,
    "lmbda": lmbda,
    "N":nb_instances,
}
    nbr_bruit=0
    for _ in range(nb_instances):
        nouvelle_inst = creation_note(parametres_default)
        if bruit>0:
            rdm=np.random.randint(0, 100)
            if rdm < bruit:
                nouvelle_inst[0][nb_matieres]=np.abs(nouvelle_inst[0][nb_matieres]-1)
                nbr_bruit+=1
        data_list.append(nouvelle_inst[0])
        parametres_default['nbr_bruit']=nbr_bruit
    return data_list,parametres_default

