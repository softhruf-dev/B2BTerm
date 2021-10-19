# This configuration file allows to define the layers that constitute each
# of the neural network models used by our MLP, RNN and LSTM models.
# The first layer is the input layer, meaning that to it we add the input shape expected.
# Note that we can still add the number of neurons on the first layer.
# The last layer is the output layer, meaning that from it we have our prediction share price days
# therefore, we don't define units for this layer as this is defined from the terminal directly.
# There are several types of parameters available to configure your Neural Network model, and more on
# these can be found in https://www.tensorflow.org/api_docs/python/tf/keras/layers
# So far the following type of layers are allowed: Dense, SimpleRNN, LSTM, and Dropout

# This is an on-going work, hence, feel free to request support for more types of layers

# From the terminal, we are able to define:
#   - The number of inputs used by the module
#   - The number of training epochs
#   - The frequency of data training (i.e. do we use all data, or every other day - may speed up training)
#   - The preprocessing type: normalization, standardization, or none
#   - The optimizer
#   - The loss function

MultiLayer_Perceptron = [
    {"Dense": {"units": 50, "activation": "relu"}},
    {"Dense": {"units": 100, "activation": "relu"}},
    {"Dense": {"units": 80, "activation": "relu"}},
    {"Dense": {"units": 30, "activation": "relu"}},
    {"Dense": {"activation": "relu"}},
]

Recurrent_Neural_Network = [
    {"SimpleRNN": {"units": 20, "activation": "relu", "return_sequences": True}},
    {"SimpleRNN": {"units": 10, "activation": "relu", "return_sequences": True}},
    {"Dropout": {"rate": 0.1}},
    {"SimpleRNN": {"units": 5, "activation": "relu", "return_sequences": False}},
    {"Dense": {"activation": "linear"}},
]

Long_Short_Term_Memory = [
    {"LSTM": {"units": 25, "activation": "tanh", "return_sequences": True}},
    {"LSTM": {"units": 15, "activation": "tanh", "return_sequences": False}},
    {"Dense": {"activation": "relu"}},
]

Convolutional = [
    {"Conv1D": {"filters": 20, "kernel_size": 10, "activation": "relu"}},
    {"MaxPool1D": {"pool_size": 2}},
    {"Conv1D": {"filters": 10, "kernel_size": 5, "activation": "relu"}},
    {"MaxPool1D": {"pool_size": 2}},
    {"Flatten": {}},
    {"Dense": {"activation": "relu"}},
]

# Optimizers :  https://www.tensorflow.org/api_docs/python/tf/keras/optimizers
# Adam, Adagrad, Adadelta, Adamax,Ftrl, Nadam, Rmsprop, Sgd
Optimizer = "Adam"

# Add early stopping to save time training when validation is plateaued
# Can be set to large number or None to ignore
Early_Stop_Patience = 10

# Losses https://www.tensorflow.org/api_docs/python/tf/keras/losses
# mae, mape, mse, msle, poisson, logcosh, kld, hinge, squared_hinge, huber
Loss = "mae"

# Preprocessing technique to use : https://scikit-learn.org/stable/modules/preprocessing.html
# Options are:
# minmax - Adjusts data to be between 0 and 1 - Most Used for Stocks
# standardization - Standardizes data so that it has mean 0 and standard deviation = 1
# normalization - Normalizes data so that L2 norm (sum x_i^2) = 1
# none - No preprocessing
Preprocess = "minmax"
