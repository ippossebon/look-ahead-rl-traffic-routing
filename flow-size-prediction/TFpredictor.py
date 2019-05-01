from __future__ import absolute_import, division, print_function

import pathlib

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# tutorial from https://www.tensorflow.org/tutorials/keras/basic_regression
print(tf.__version__)

# dataset_path = 'example-data.csv'

# import dataset using pandas
# column_names = ['td','sp','dp','pr','fwd','stos','ipkt','ibyt','opkt','obyt','in','out','sas','das','smk','dmk','dtos','dir','svln','dvln','cl','sl','al','exid']

dataset_path = '../dataset/test/nfcapd_201706271035-tail.csv'
column_names = ['ts','te','td','sa','da','sp','dp','pr','flg','fwd','stos','ipkt','ibyt','opkt','obyt','in','out','sas','das','smk','dmk','dtos','dir','nh','nhb','svln','dvln','ismc','odmc','idmc','osmc','mpls1','mpls2','mpls3','mpls4','mpls5','mpls6','mpls7','mpls8','mpls9','mpls10','cl','sl','al','ra','eng','exid','tr']
raw_dataset = pd.read_csv(
    dataset_path,
    names=column_names,
    na_values = "?",
    comment='\t',
    sep=",",
    skipinitialspace=True
)
dataset = raw_dataset.copy()

# remove colunas com valores irrelevantes: parâmetro 1 é para colunas, 0 é para linhas
dataset = dataset.drop('ts', 1)
dataset = dataset.drop('te', 1)
dataset = dataset.drop('sa', 1) # infos qualitativas
dataset = dataset.drop('da', 1) # infos qualitativas
dataset = dataset.drop('mpls1', 1) # infos qualitativas
dataset = dataset.drop('mpls2', 1) # infos qualitativas
dataset = dataset.drop('mpls3', 1) # infos qualitativas
dataset = dataset.drop('mpls4', 1) # infos qualitativas
dataset = dataset.drop('mpls5', 1) # infos qualitativas
dataset = dataset.drop('mpls6', 1) # infos qualitativas
dataset = dataset.drop('mpls7', 1) # infos qualitativas
dataset = dataset.drop('mpls8', 1) # infos qualitativas
dataset = dataset.drop('mpls9', 1) # infos qualitativas
dataset = dataset.drop('mpls10', 1) # infos qualitativas
dataset = dataset.drop('flg', 1) # infos qualitativas
dataset = dataset.drop('idmc', 1) # infos qualitativas
dataset = dataset.drop('osmc', 1) # infos qualitativas
dataset = dataset.drop('ismc', 1) # infos qualitativas
dataset = dataset.drop('odmc', 1) # infos qualitativas

print(dataset.tail())
exit(1)

# clean data because it contains a few unknown values
dataset.isna().sum()


# convert "Origin" column that is categorical to numerical
# origin = dataset.pop('Origin')

# dataset['USA'] = (origin == 1)*1.0
# dataset['Europe'] = (origin == 2)*1.0
# dataset['Japan'] = (origin == 3)*1.0
# print(dataset.tail())

# Split dataset into a training set and a test set
train_dataset = dataset.sample(frac=0.8,random_state=0)
test_dataset = dataset.drop(train_dataset.index)

# inspect dataset - Have a quick look at the joint distribution of a few pairs of columns from the training set.
# sns.pairplot(
#     train_dataset[["MPG", "Cylinders", "Displacement", "Weight"]],
#     diag_kind="kde"
# )

# check overall statistics
# target class = obyt
train_stats = train_dataset.describe()
train_stats.pop("obyt")
train_stats = train_stats.transpose()
print(train_stats)


# split features from labels - Separate the target value (label) from features
train_labels = train_dataset.pop('obyt')
test_labels = test_dataset.pop('obyt')


# Normalize data
def norm(x):
    return (x - train_stats['mean']) / train_stats['std']


normed_train_data = norm(train_dataset)
normed_test_data = norm(test_dataset)

## Building the model ##
def buildModel():
    model = keras.Sequential([
        layers.Dense(64, activation=tf.nn.relu, input_shape=[len(train_dataset.keys())]),
        layers.Dense(64, activation=tf.nn.relu),
        layers.Dense(1)
    ])

    optimizer = tf.keras.optimizers.RMSprop(0.001)

    model.compile(
        loss='mean_squared_error',
        optimizer=optimizer,
        metrics=['mean_absolute_error', 'mean_squared_error']
    )
    return model

model = buildModel()

# Use the .summary method to print a simple description of the model
print(model.summary())

# Now try out the model. Take a batch of 10 examples from the training data and call model.predict on it.
example_batch = normed_train_data[:10]
example_result = model.predict(example_batch)
print(example_result)

## Training the model ##

# Train the model for 1000 epochs, and record the training and validation accuracy in the history object.
# Display training progress by printing a single dot for each completed epoch
class PrintDot(keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs):
        if epoch % 100 == 0: print('')
        print('.', end='')

EPOCHS = 1000

history = model.fit(
    normed_train_data,
    train_labels,
    epochs=EPOCHS,
    validation_split = 0.2,
    verbose=0,
    callbacks=[PrintDot()]
)

# Visualize the model's training progress using the stats stored in the history object.
hist = pd.DataFrame(history.history)
hist['epoch'] = history.epoch
print('')
print(hist.tail())

def plotHistory(history):
    hist = pd.DataFrame(history.history)
    hist['epoch'] = history.epoch

    plt.figure()
    plt.xlabel('Epoch')
    plt.ylabel('Mean Abs Error [MPG]')
    plt.plot(
        hist['epoch'],
        hist['mean_absolute_error'],
        label='Train Error'
    )
    plt.plot(
        hist['epoch'],
        hist['val_mean_absolute_error'],
        label = 'Val Error'
    )
    plt.ylim([0,5])
    plt.legend()

    plt.figure()
    plt.xlabel('Epoch')
    plt.ylabel('Mean Square Error [$MPG^2$]')
    plt.plot(
        hist['epoch'],
        hist['mean_squared_error'],
        label='Train Error'
    )
    plt.plot(
        hist['epoch'],
        hist['val_mean_squared_error'],
        label = 'Val Error'
    )
    plt.ylim([0,20])
    plt.legend()
    plt.show()


plotHistory(history)


############################
# model = buildModel()
#
# # The patience parameter is the amount of epochs to check for improvement
# early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=10)
#
# history = model.fit(
#     normed_train_data,
#     train_labels,
#     epochs=EPOCHS,
#     validation_split = 0.2,
#     verbose=0,
#     callbacks=[early_stop, PrintDot()]
# )
#
# plotHistory(history)
#
# loss, mae, mse = model.evaluate(normed_test_data, test_labels, verbose=0)
# print("Testing set Mean Abs Error: {:5.2f} MPG".format(mae))
#
#
# ## Make predictions ##
# test_predictions = model.predict(normed_test_data).flatten()
#
# plt.scatter(test_labels, test_predictions)
# plt.xlabel('True Values [obyt]')
# plt.ylabel('Predictions [obyt]')
# plt.axis('equal')
# plt.axis('square')
# plt.xlim([0,plt.xlim()[1]])
# plt.ylim([0,plt.ylim()[1]])
# _ = plt.plot([-100, 100], [-100, 100])
#
#
# # Error distribution
# error = test_predictions - test_labels
# plt.hist(error, bins = 25)
# plt.xlabel("Prediction Error [obyt]")
# _ = plt.ylabel("Count")
