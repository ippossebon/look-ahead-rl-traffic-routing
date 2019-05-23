from __future__ import absolute_import, division, print_function

import pathlib

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# tutorial from https://www.tensorflow.org/tutorials/keras/basic_regression

dataset_path = '../dataset/test/unicauca100.csv'

# import dataset using pandas

raw_dataset = pd.read_csv(
    dataset_path,
    na_values = "?",
    comment='\t',
    sep=",",
    skipinitialspace=True
)
dataset = raw_dataset.copy()

# remove colunas com valores irrelevantes: parâmetro 1 é para colunas, 0 é para linhas
dataset = dataset.drop('Flow.ID', 1)
dataset = dataset.drop('Source.IP', 1)
dataset = dataset.drop('Source.Port', 1) # infos qualitativas
dataset = dataset.drop('Destination.IP', 1) # infos qualitativas
dataset = dataset.drop('Destination.Port', 1) # infos qualitativas
dataset = dataset.drop('Protocol', 1) # infos qualitativas
dataset = dataset.drop('Timestamp', 1) # infos qualitativas
dataset = dataset.drop('Label', 1) # infos qualitativas
dataset = dataset.drop('L7Protocol', 1) # infos qualitativas
dataset = dataset.drop('ProtocolName', 1) # infos qualitativas


# drop rows that contain unknown values
dataset = dataset.dropna()


# Split dataset into a training set and a test set
train_dataset = dataset.sample(frac=0.8,random_state=0)
test_dataset = dataset.drop(train_dataset.index)

# inspect dataset - Have a quick look at the joint distribution of a few pairs of columns from the training set.
sns.pairplot(
    train_dataset[["Flow.Duration"]],
    diag_kind="kde"
)

# check overall statistics
train_stats = train_dataset.describe()
train_stats.pop("Flow.Duration")
train_stats = train_stats.transpose()
print(train_stats)



# split features from labels - Separate the target value (label) from features
train_labels = train_dataset.pop('Flow.Duration')
test_labels = test_dataset.pop('Flow.Duration')


# Normalize data
# def norm(x):
#     try:
#         value = (x - train_stats['mean']) / train_stats['std']
#     except:
#         value = x
#
#     import pdb; pdb.set_trace()
#
#     return value

# normed_train_data = norm(train_dataset)
# normed_test_data = norm(test_dataset)
normed_train_data = train_dataset
normed_test_data = test_dataset

## Building the model ##
def buildModel():
    # Add layers to the deep learning model: Adds a densely-connected layer with 64 units to the model:
    model = keras.Sequential([
        layers.Dense(64, activation=tf.nn.relu, input_shape=[len(train_dataset.keys())]),
        layers.Dense(64, activation=tf.nn.relu),
        layers.Dense(1)
    ])

    optimizer = tf.keras.optimizers.RMSprop(0.001)
    # optimizer=tf.train.AdamOptimizer(0.001)

    model.compile(
        loss='mean_squared_error',
        optimizer=optimizer,
        metrics=['mean_absolute_error', 'mean_squared_error']
    )
    return model

model = buildModel()

# Use the .summary method to print a simple description of the model
print('MODEL SUMMARY')
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
    plt.ylabel('Mean Abs Error [Flow.Duration]')
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
    plt.ylabel('Mean Square Error [$Flow.Duration^2$]')
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
model = buildModel()

# The patience parameter is the amount of epochs to check for improvement
early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=10)

history = model.fit(
    normed_train_data,
    train_labels,
    epochs=EPOCHS,
    validation_split = 0.2,
    verbose=0,
    callbacks=[early_stop, PrintDot()]
)

plotHistory(history)

loss, mae, mse = model.evaluate(normed_test_data, test_labels, verbose=0)
print("Testing set Mean Abs Error: {:5.2f} Flow.Duration".format(mae))


## Make predictions ##
test_predictions = model.predict(normed_test_data).flatten()

plt.scatter(test_labels, test_predictions)
plt.xlabel('True Values [Flow.Duration]')
plt.ylabel('Predictions [Flow.Duration]')
plt.axis('equal')
plt.axis('square')
plt.xlim([0,plt.xlim()[1]])
plt.ylim([0,plt.ylim()[1]])
_ = plt.plot([-100, 100], [-100, 100])


# Error distribution
error = test_predictions - test_labels
plt.hist(error, bins = 25)
plt.xlabel("Prediction Error [Flow.Duration]")
_ = plt.ylabel("Count")
