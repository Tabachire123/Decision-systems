from mr_sort.model import *
from mr_sort.generate import *
import time
from sklearn.metrics import accuracy_score, f1_score

taille_data_test=200


def prediction(data_test,frontiers,weights,lmbda):
    res=[]
    notes = [i[:-1] for i in data_test]
    for r in range(len(notes)):
        accepted=0
        for j in range(nb_classes - 1):
                somme = 0
                for k in range(nb_matieres):
                    if notes[r][k] >= frontiers[k][j]:
                        somme += weights[k]

                if somme >= lmbda:
                    accepted += 1

        res.append(accepted)
    return res

start=time.time()

taille_total=nb_instances+taille_data_test
#Génération des données
data,parameters = generate_data(nb_matieres,nb_classes,taille_total)

#Première prédiction

result = MRSortmodel(data[:taille_total-taille_data_test], nb_matieres, nb_classes)

end=time.time()


weights_t=["{:.2f}".format(i) for i in parameters["w"]]
weights_mrsort=["{:.2f}".format(i) for i in result[0]]

print("Nombre de signaux bruités: "+str(parameters['nbr_bruit']))
print("lambda truth: "+str("{:.2f}".format(parameters["lmbda"])))
print("lambda mrsort: "+str("{:.2f}".format(result[1])))
print("weight truth: "+str(weights_t))
print("weight mrsort: "+str(weights_mrsort))

elapsed=end-start
print(f'Temps d\'exécution : {elapsed:.3}s')

data_test=data[taille_total-taille_data_test:]
list_class_test=[i[nb_matieres] for i in data_test]
list_class_prediction=prediction(data_test,result[3],result[0],result[1])

f1 = f1_score(list_class_test, list_class_prediction,average='macro')
accuracy = accuracy_score(list_class_test, list_class_prediction)

print("F1-score: "+str(f1))
print("accuracy: "+str(accuracy))
