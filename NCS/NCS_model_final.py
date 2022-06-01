
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



dimacs_file="workingfile.cnf"
gophersat_path="/Users/ayoubbakkoury/PycharmProjects/SDP/systeme-de-decision-master/NCS/gophersat"


data,params=generate_data(nb_matieres,nb_classes,nb_instances)
columns=[str(k) for k in range(nb_matieres)]
data=pd.DataFrame(data,columns=columns+['accepted'])
data.to_csv('data.csv')


def test_class(h):
    return data.index[data["accepted"] == h]


def clauses(data,mix_subjects,X,x,y,val):
    subjects=range(len(data.columns)-1)
    mix_subjects=[]
    for i in range(0, len(data.columns)):
        mix_subjects += list(combinations(range(len(data.columns)-1), i))
    ## Définition des clauses

    ## Clauses 2a et 2b : Si un élève valide avec la note k,
    ## alors tous ceux qui valident avec une note k'>k valident aussi
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
    clause2c = [[y[p], -y[k]]
        for k in mix_subjects
            for p in mix_subjects
            if set(k).issubset(set(p)) and set(k) != set(p)
    ]

# Clause 4 : condition nécessaire et suffisante d'admission
    print(x)
    print(y)
    clause2d = []
    for b in mix_subjects:
        for h in range(1, val):
            for j in test_class(h - 1):
                clause2d.append([-y[b]] + [-x[i, h, X[i, j]] for i in b])

# Clause 5 : condition nécessaire et suffisante de refus
    clause2e = []
    for h in range(1, val):
        for b in mix_subjects:
            BN = tuple([i for i in subjects if i not in b])
            for j in test_class(h):
                clause2e.append([y[BN]] + [x[i, h, X[i, j]] for i in b])

    Clauses = clause2a + clause2b + clause2c + clause2d + clause2e

    return Clauses


def NCSModel(data):
    val = max(data["accepted"]) + 1 #nombre de classes
    # Récupération de toutes les permutations possibles, utiles pour les clauses
   # mix_subjects = []
   # for i in range(0, len(data.columns)):
   # mix_subjects += list(combinations(range(len(data.columns)-1), i))
    mix_subjects = sum([list(combinations(range(len(data.columns)-1), i)) for i in range(0,len(data.columns))], [] )


## Définition de i2v, qui va nous permettre les affichages de
## variables et d'entiers sous formes de dictionnaires

    #Définition d'un compteur qui nous permet de parcourir les notes pour chacune des matières
    X = np.array([data.iloc[:, i] for i in range(len(data.columns)-1)])
    counter = iter(range(1, X.size * val + len(mix_subjects) + 1))
    #integers
    x = {}
    for i in range(len(data.columns)-1): #nombre de matières
            for h in range(1, val): # h parcourt les frontières entre classes
                for k in X[i]: #k parcourt toutes les notes
                    if (i, h, k) not in x:
                        x[(i, h, k)] = next(counter)

    #variables
    y = {v: next(counter) for v in mix_subjects}

    variables = list(x.keys()) + list(y.keys())
    i2v = {value: key for key, value in list(x.items()) + list(y.items())}
    Clauses=clauses(data,mix_subjects,X,x,y,val)

    Dimacs = _clauses_to_dimacs(Clauses, len(variables))
    _write_dimacs_file(Dimacs, dimacs_file)
    return i2v, x, y


## Conversion tirée du TD gophersat
def _clauses_to_dimacs(clauses, numvar):
    dimacs = "c This is it\np cnf " + str(numvar) + " " + str(len(clauses)) + "\n"
    for clause in clauses:
        for atom in clause:
            dimacs += str(atom) + " "
        dimacs += "0\n"
    return dimacs

def _write_dimacs_file(dimacs, filename):
    with open(filename, "w", newline="") as cnf:
        cnf.write(dimacs)

def exec_gophersat(filename,i2v, encoding="utf8"):
    cmd = gophersat_path
    result = subprocess.run([cmd, filename], stdout=subprocess.PIPE, check=True, encoding=encoding)
    string = str(result.stdout)
    lines = string.splitlines()

    if lines[1] != "s SATISFIABLE":
        return False,[]

    model = list(map(int, lines[2][2:].split(" ")))
    values = [value for value in model if value != 0]
# Description de la solution
#    clauses = [int(x) for x in model if int(x) != 0]
    results = {i2v[abs(value)]: value > 0 for value in values}

    return True, values, results


def traduction_NCS(groun, x , y) :
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
        b= var #b est une permutation possible de k compris entre 0 et 5 matières, h est la classe associée
        if sufficient:
            if b not in solution["coalitions"]:  #Ajout de la coalition à la solution
                solution["coalitions"].append(str(b))
    return solution, front
