import numpy as np

class NumberClassifier:

    def __init__(self, weights_file='weights/weights.txt'):
        self.weights = []

        dims = None
        with open(weights_file, 'r') as file:
            for line in file:
                if ';' in line:
                    dims = tuple([int(dim.strip()) for dim in line.split(';')])

                else:
                    values = np.asarray([[float(val.strip()) for val in line.split(',')]])
                    self.weights.append(values.reshape(dims))

        self.weights = np.asarray(self.weights)

    # returns the number corresponding to the largest output activation, but -1 if no output is greater than 0.5
    def classify(self, input_vec):
        def sigmoid(z):
            return 1 / (1 + np.exp(-z))

        activations = np.asarray([input_vec]).T
        for wt in self.weights:
            # add on the bias unit to the vector
            activations = np.concatenate(([[1]], activations))

            # calculate the activations of the next layer
            activations = sigmoid(np.dot(wt, activations))

        outputs = activations.T[0]
        if np.max(outputs) < 0.5:
            return -1

        return np.argmax(outputs)
