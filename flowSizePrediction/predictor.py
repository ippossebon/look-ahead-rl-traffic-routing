from sklearn.ensemble import AdaBoostClassifier
from sklearn.neural_network import MLPClassifier

class FlowSizePredictor(object):
    # Aprendizado supervisionado
    # tutorial: https://github.com/Rogerh91/Springboard-Blog-Tutorials/blob/master/Neural%20Networks%20/JMPortilla_SpringBoard_Blog_Neural_Network.ipynb
    def __init__(self, training_set, training_set_classification):
        self.training_set = training_set
        self.training_set_classification = training_set_classification


    def adaBoostMLP(self, test_set):
        classifier_mlp = MLPClassifier(
            solver='lbfgs',
            alpha=1e-5,
            hidden_layer_sizes=(60, 40), # configuração usada por Poupart2016: input de 106; saída de 1 neurônio, indicando se é mice ou elephant flow
            random_state=1)
        classifier_mlp.fit(self.training_set, self.training_set_classification)

        meta_learner = AdaBoostClassifier(
            base_estimator=classifier_mlp,
            n_estimators=15,
            algorithm='SAMME')
        meta_learner = meta_learner.fit(self.training_set, self.training_set_classification)

        result = meta_learner.predict(test_set)
        predictions = []
        predictions = list(result.tolist())

        return predictions
