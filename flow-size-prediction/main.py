from math import sqrt
from random import shuffle
from sklearn import svm, tree
from sklearn.ensemble import VotingClassifier, AdaBoostClassifier, BaggingClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import KFold
from sklearn.neural_network import MLPClassifier

class FlowSizePredictor(object):
    # Aprendizado supervisionado
    # tutorial: https://github.com/Rogerh91/Springboard-Blog-Tutorials/blob/master/Neural%20Networks%20/JMPortilla_SpringBoard_Blog_Neural_Network.ipynb
    def __init__(self):
        pass

    def adaBoostMLP(self):
        classifier_mlp = MLPClassifier(
            solver='lbfgs',
            alpha=1e-5,
            hidden_layer_sizes=(60, 40), # configuração usada por Poupart2016: input de 106; saída de 1 neurônio, indicando se é mice ou elephant flow
            random_state=1
        )

        meta_learner = AdaBoostClassifier(
        base_estimator=classifier_dt,
        n_estimators=15,
        algorithm='SAMME'
        )
    meta_learner = meta_learner.fit(training_set, training_set_classification)

    result = meta_learner.predict(evaluation_set)
    predictions = []
    predictions = list(result.tolist())
