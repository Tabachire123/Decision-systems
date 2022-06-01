
import numpy as np
import pandas as pd
import subprocess
from itertools import combinations
from generate import *


'''Implémentation du modèle :
- Définition de i2v pour parcourir les données plus simplement
- Développement des clauses à partir de https://arxiv.org/pdf/1710.10098.pdf
- Conversion au format dimacs, et écriture du dimacs
- Développement de la fonction gophersat, à l'aide du TD
'''



maxsat_file="workingfile.wcnf"
gophersat_path="/Users/ayoubbakkoury/PycharmProjects/SDP/systeme-de-decision-master/NCS/gophersat"


data,params=generate_data(nb_matieres,nb_classes,nb_instances)
columns=[str(k) for k in range(nb_matieres)]
data=pd.DataFrame(data,columns=columns+['accepted'])
data.to_csv('data.csv')


def test_class(h):
    return data.index[data["accepted"] == h]


def clauses_maxsat(data,X,x,y,z,val, single_peak ):
    subjects=range(len(data.columns)-1)
    mix_subjects=[]
    for i in range(0, len(data.columns)):
        mix_subjects += list(combinations(range(len(data.columns)-1), i))
    ## Définition des clauses pour le MAXSAT, il faut ajouter la clause objectif, et inclure la variable z
    ## dans les deux dernieres clauses

    ## Clauses 2a et 2b : Si un élève valide avec la note k,
    ## alors tous ceux qui valident avec une note k'>k valident aussi
    ## Adaptation sous forme d'intervalle pour la version single peaked

    if single_peak :
        clause2a = []
        for i in subjects:
                for h in range(1, val):
                    for k in X[i]:
                        for k1 in X[i]:
                            for k2 in X[i]:
                                if k < k1 and k1 < k2:
                                    clause2a.append(
                                        [x[(i, h, k1)],-x[(i, h, k)],-x[(i, h, k2)]])
    else :
        clause2a = [
            [x[i, h, p], -x[i, h, k]] for h in range(1, val) for i in subjects for k in X[i] for p in X[i] if k < p
        ]

    clause2b = [
        [x[i, h, k], -x[i, p, k]]
        for i in subjects
        for k in X[i]
        for h in range(1, val)
        for p in range(1, val)
        if h < p
    ]
# Clause 2c : L'inclusion conserve la suffisance d'un ensemble
    clause2c = [[y[p,h], -y[k,h]]
        for h in range(1, val)
            for k in mix_subjects
                for p in mix_subjects
                if set(k).issubset(set(p)) and set(k) != set(p)
    ]
# Clause 4 : Comme la clause 2 mais avec y.
    clause2d = []
    for b in mix_subjects :
        for h in range(1, val):
            for p in range(1, val):
                if h<p : clause2d.append([y[b, h], -y[b, p]])
# Clause 5 : condition nécessaire et suffisante d'admission, à laquelle on intègre z
    clause2e = []
    for b in mix_subjects:
        for h in range(1, val):
            for j in test_class(h - 1):
                clause2e.append( [-y[b,h],-z[j]] + [-x[i, h, X[i, j]] for i in b])

# Clause 6 : Complémentaire => condition nécessaire et suffisante de refus, à laquelle on intègre z
    clause2f = []
    for h in range(1, val):
        for b in mix_subjects:
            BN = tuple([i for i in subjects if i not in b]) #Complémentaire de la clause précédente
            for j in test_class(h):
                clause2f.append([y[BN,h], -z[j]] + [x[i, h, X[i, j]] for i in b])



# Clause objectif : maximiser la somme des z vrais
    clausegoal = [[z[v]] for v in data.index]

    Clauses = clause2a + clause2b + clause2c +clause2d + clause2e + clause2f + clausegoal

#Définition des poids pour le weighted maxsat à partir de la documentation
#https://centralesupelec.edunao.com/pluginfile.php/209234/mod_label/intro/ecai20-maxsat-tutorial.pdf

# Le poids 1 est assigné à la clause objectif phigoal, et le poids maximal aux autres clauses.

    weights = [data.size] * (len(Clauses) - len(clausegoal)) + [1] * len(clausegoal)
    return Clauses, weights


def MAXSATModel(data, single_peak):
    val = max(data["accepted"]) + 1 #nombre de classes
    # Récupération de toutes les permutations possibles, utiles pour les clauses
   # mix_subjects = []
   # for i in range(0, len(data.columns)):
    mix_subjects = sum([list(combinations(range(len(data.columns)-1), i)) for i in range(0,len(data.columns))], [] )


## Définition de i2v, qui va nous permettre les affichages de
## variables et d'entiers sous formes de dictionnaires

    #Définition d'un compteur qui nous permet de parcourir les notes pour chacune des matières
    X = np.array([data.iloc[:, i] for i in range(len(data.columns)-1)])
#    criteria_grades = {i: sorted(dataset[str(i)].drop_duplicates()) for i in criteria}
    counter = iter(range(1, X.size * val + len(mix_subjects) + 1))
    #integers
    x = {}
    for i in range(len(data.columns)-1):
            for h in range(1, val):
                for k in X[i]:
                    if (i, h, k) not in x:
                        x[(i, h, k)] = next(counter)

    #variables y,définie différemment que dans le SAT solver
    y = {(b, p): next(counter) for b in mix_subjects for p in range(1, val)}

    #Ajout de la variable z, pour le weighted maxsat
    z = {u: next(counter) for u in data.index}

    variables = list(x.keys()) + list(y.keys()) + list(z.keys())
    i2v = {value: key for key, value in list(x.items()) + list(y.items()) + list(z.items())}
    clauses, weights =clauses_maxsat(data,X,x,y,z,val, single_peak)

    Dimacs = _clauses_to_dimacs_weighted(clauses,weights, numvar = len(variables))
    _write_dimacs_file_maxsat(Dimacs, maxsat_file)
    return i2v, x, y


## Conversion tirée du TD gophersat,
# ajustement pour prendre en compte les poids pour le MAXSAT
def _clauses_to_dimacs_weighted(clauses, weights, numvar):
    dimacs = "c This is it\np wcnf " + str(numvar) + " " + str(len(clauses)) + "\n"
    for clause, weight in zip(clauses, weights):
        dimacs += str(weight) + " " + " ".join(map(str, clause)) + " 0\n"
    return dimacs


def _write_dimacs_file_maxsat(dimacs, filename):
    with open(filename, "w", newline="") as wcnf:
        wcnf.write(dimacs)

def exec_maxsat(filename,i2v, encoding="utf8"):
    cmd = gophersat_path
    result = subprocess.run([cmd, filename], stdout=subprocess.PIPE, check=True, encoding=encoding)
    string = str(result.stdout)
    lines = string.splitlines()

    if lines[2] != "s OPTIMUM FOUND":
        return  False,[]

    model = lines[3][2:].split(" ")
    model = [int(x.replace("x", "")) for x in model if x != ""]
    values = [value for value in model if value != 0]
# Description de la solution
#    clauses = [int(x) for x in model if int(x) != 0]
    results = {i2v[abs(value)]: value > 0 for value in values}

    return True, values, results

def traduction_maxsat(groun, x , y) :
    val = max(data["accepted"]) + 1
    results = groun[2]
    solution = {}
#Détermination d'intervalles de confiance pour la frontière
    frontieres = [[[0, 20] for _ in range(nb_matieres)] for _ in range(val - 1)]
    front = [[[1] for _ in range(nb_matieres)] for _ in range(val - 1)]
    for var, sat in list(results.items())[: len(x)]:
        i, h, k = var
        if sat:  # marks validates criterion
            frontieres[h - 1][i][1] = min(frontieres[h - 1][i][1], k) #Borne maximale de l'intervalle de confiance
        else:
            frontieres[h - 1][i][0] = max(frontieres[h - 1][i][0], k) #Borne minimale de l'intervalle de confiance
        front[h-1][i] = frontieres[h - 1][i][0]
# Récupération des coalitions suffisantes, i, e les variables de y que l'on récupère True
# Pour rappel, les  coalitions de y sont déterminées en # parcourant toutes les coalitions possibles de matières,
# ainsi que les classes
    solution["coalitions"] = []
    for var, sufficient in list(results.items())[len(x) :len(x) + len(y)]:
#        b,classe= list(var)[0], list(var)[1] #b est une permutation possible de k compris entre 0 et 5 matières, h est la classe associée
        if sufficient:
            solution["coalitions"].append(var)
# Détermination des instances bien classifiées
    solution["classified"] = [] # indexes of correctly classified instances
    for instance, classified in list(results.items())[len(x) + len(y) :]:
#Parcourt bien le nombre d'instances Z
        if classified:
            solution["classified"].append(instance)

    return solution, front
