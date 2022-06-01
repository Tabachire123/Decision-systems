# Project for SDP course CentraleSupelec 2022 

## Students 

- Benaija Ismail
- Bakoury Ayoub
- Baddou Othmane

## Context

This project is part of a class project for the SDP course in CentraleSupelec in the fall of 2022. We are expected to fit an optimization algorithm that can learn how to accept a student in a rogram based on an his/her grades and other decisional parameters.

## Project structure 

```
    MR-Sort
        ├── generate.py             # data generation 
        ├── model.py                # Mr-sort model 
        ├── main.py                 # Model applied on data generated
        ├── performance.py          # analytics

```

## Reminder of the mathematical context

Consider a situation in which a committee for a higher education program has to decide about the
admission of students on the basis of their evaluations in 4 courses: mathematics (M), physics (P),
literature (L) and history (H). Evaluations on all courses range in the [0,20] interval. To be accepted
(A) in the program, the committee considers that a student should obtain at least 12 on a “majority” of
courses, otherwise, the student is refused (R). From the committee point of view, all courses (criteria)
do not have the same importance. To define the required majority of courses, the committee attaches a
weight wj ≥ 0 to each course such that they sum to 1; a subset of courses C ⊆ {M, P, L, H} is considered
as a majority if P
j∈C wj ≥ λ, where λ ∈ [0, 1] is a required majority level.


# Mr sort 

## Data generation 

We define three functions in this file :


- parameters 
    - This one is used to initialize randomly the parameters of the model
- creation_note
    - This one is used to generate the results for an instance 
- generate_data
    - We finally use this function using the prior ones to generate the dataset for all instances and give the default parameters


| ID | Course 1  | Course 2  |Accepted|
| ------ | ------ | ------ |------ |
| 0 | 12 |15 |1 |
| 1 | 3 | 4 |0 |

The user may chose to add noise to the data by changing the variable "bruit" in the generator.py file. The value of this variable will correspond to the percentage of noisy data (a value of 3 for example will correspond to 3% of noisy data).

## The model 

Based on the paper [Learning the Parameters of a Multiple Criteria Sorting method Based on a Majority Rule](file:///Users/othmanebaddou/Downloads/2011-Leroy-Mousseau-Pirlot-ADT%20(2).pdf) by Agnes Leroy1 and Vincent Mousseau2 and Marc Pirlot.

Let's define the MS-sort algorithm


```math
\max \alpha
```

s.t.

- $`\sum_{i \in N}{w_i(s)} + \sigma_s + \epsilon = \lambda \quad \forall s \in R^*`$
- $`\sum_{i \in N} w_i(s) = \lambda +  \sigma_s \quad \forall s \in A^*`$
- $`\alpha \leq \sigma_s \quad \forall s \in A^*`$
- $`w_i(s) \leq w_i \quad \forall s \in A^* \cup R^*, \forall i \in N`$
- $`w_i(s) \leq \delta_i(s) \quad \forall s \in A^* \cup R^*, \forall i \in N`$
- $`w_i(s) \geq \delta_i(s) - 1 + w_i \quad \forall s \in A^* \cup R^*, \forall i \in N`$
- $`M\delta_i(s)+\epsilon \geq s_i - b_i \quad \forall s \in A^* \cup R^*, \forall i \in N`$
- $`M(\delta_i(s)-1) \leq s_i-b_i \quad \forall s \in A^* \cup R^*, \forall i \in N`$
- $`\sum_{i \in N}{w_i}=1, \quad \lambda \in [0.5, 1]`$
- $`w_i \in [0, 1] \quad \forall i \in N`$
- $`w_i(s) \in [0, 1], \quad \delta_i(s) \in \{0, 1\} \quad \forall s \in A^* \cup R^*, \forall i \in N`$
- $`\sigma_s \in \mathbb{R} \quad \forall s \in A^* \cup R^*`$
- $`\alpha \in \mathbb{R}`$


## Run code 

The main.py file is used to run the algorithm. We use the "generate_data()" function and the model from the two other files to fit the parameters. We set the default parameters as 

- nb_matieres = 5
- nb_classes = 3
- nb_instances = 1000

The reader may change these parameters directly in the generate.py file. 
 
# NCS Model

Please note that in order to use these algorithms you need to upload the correct gophersat version compatible with your OS and go to ncs_model_final file and maxsat file in order to change the path link to the gophersat solver.


## Project structure 



```
    NCS
        ├── generate.py             # data generation 
        ├── ncs_model_final.py      # NCS model 
        ├── main.py                 # Model applied on data generated
        ├── data.csv                # Example of dataset generated with generate.py
        ├── maxsat                  # maxsat model
        ├── gophersat               # gophersat file

```

This time we won't get into details about the functions in generate.py because the functions are similar to the ones prior. 

Same thing for using the code, we can run the code in main.py using the default parameters in generate.py or change these parameters prior to using the code. 


## The NCS algorithm 

(SAT encoding for U-NCS). Let A : X → C1 ≺···≺ Cp
an assignment. We define the boolean function φSAT
A with variables:

- xi, h, k, indexed by a criterion i ∈ N , a frontier between classes
1 ≤ h ≤ p − 1, and a value k ∈ X
i taken on criterion i by a reference alternative,
- yB indexed by a coalition of criteria B ⊆ N

We then create clauses that the algorithm must respect : 

- $`\forall i \in \mathcal{N}, \forall 1 \leq h \leq p-1, \forall k<k', \quad x_{i, h, k} \Rightarrow x_{i, h, k'}`$ (We can only consider adjacent grades) (1)
- $`\forall i \in \mathcal{N}, \forall 1 \leq h < h' \leq p-1, \forall k, \quad x_{i, h', k} \Rightarrow x_{i, h, k}`$ (we can only consider adjacent boundaries) (2)
- $`\forall B \subset B' \subseteq \mathcal{N}, \quad y_{B} \Rightarrow y_{B'}`$ (We can only consider $`B`$ and  $`B'`$ such that  $`|B' \setminus B| = 1`$) (3)
- $`\forall B \subseteq \mathcal{N}, \forall 1 \leq h \leq p-1 \forall u \in X^*: A(u) = C^{h-1}, \quad \bigwedge_{i \in B}{x_{i, h, u_i}} \Rightarrow \neg y_B`$ (4)
- $`\forall B \subseteq \mathcal{N}, \forall 1 \leq h \leq p-1 \forall a \in X^*: A(a) = C^{h}, \quad \bigwedge_{i \in B}{\neg x_{i, h, a_i}} \Rightarrow y_{\mathcal{N} \setminus B}`$  (5)


## MAXSAT VERSION

We updated the main.py for the NCS model so the user can chose which version of the algorithm to run. You may change the "mode" variable in the main.py to either "NCS" or "MAXSAT".
