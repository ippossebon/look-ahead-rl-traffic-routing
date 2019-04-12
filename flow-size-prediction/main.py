import csv

from predictor import FlowSizePredictor
from sklearn.model_selection import KFold

class FlowSizePredictorApplication(object):
    def __init__(self):
        self.data = []
        self.features = []
        self.readData()

        self.runPredictor()

    def readData(self):
        with open('example-data.csv') as csvfile:
            reader = csv.reader(csvfile)
            count = 0
            for row in reader:
                if count == 0:
                    self.features = row
                    count = count + 1
                else:
                    self.data.append(row)



    def runPredictor(self):
        total_bytes_index = self.features.index("obyt")
        training_set = []
        training_set_classification = []

        for item in self.data:
            training_set_classification.append(float(item[total_bytes_index]))
            del item[total_bytes_index]
            item_features = []

            for feature in item:
                item_features.append(float(feature))

            training_set.append(item_features)

        predictor = FlowSizePredictor(training_set, training_set_classification)

        test_set = training_set
        predictions = predictor.adaBoostMLP(test_set)
        print(predictions)




if __name__ == '__main__':
    FlowSizePredictorApplication()
