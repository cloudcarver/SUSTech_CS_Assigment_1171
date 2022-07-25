import numpy as np
import random
import pickle
import config

class Perceptron(object):

    def __init__(self, n_inputs, max_epochs=1e4, learning_rate=1e-2):
        """
        Initializes perceptron object.
        Args:
            n_inputs: number of inputs.
            max_epochs: maximum number of training cycles.
            learning_rate: magnitude of weight changes at each training cycle
        """
        # fields
        self.n_inputs = n_inputs
        self.max_epochs = max_epochs
        self.learning_rate = learning_rate
        self.w = np.zeros(n_inputs + 1)

        
    def forward(self, input):
        """
        Predict label from input 
        Args:
            input: numpy array of dimension equal to n_inputs. e.g. np.array([11.9183227, 0.13293148])
            output: label, 1 or -1
        """
        input_vector = np.concatenate((np.array([1]), input))
        np.dot(input_vector, self.w)
        label = self.sgn(np.dot(input_vector, self.w))
        return label
    
    def sgn(self, weighted_sum):
        return 1 if weighted_sum > 0 else -1
        
    def train(self, training_inputs, labels):
        """
        Train the perceptron
        Args:
            training_inputs: list of numpy arrays of training points.
            labels: arrays of expected output value for the corresponding point in training_inputs.
        """
        # init
        data_set = []
        size = len(training_inputs)
        for i in range(0, size):
            data_set.append((np.concatenate((np.array([1]), training_inputs[i])), training_inputs[i], labels[i]))
        
        # train
        for i in range(0, int(self.max_epochs)):
            random.shuffle(data_set)
            if config.VERBOSE:
                print("process: {}% traning weight:{}".format(100*i/self.max_epochs, self.w))
            for i in range(0, size):
                xin = data_set[i][1]
                x = data_set[i][0]
                y = data_set[i][2]
                y_prime = self.forward(xin)
                if y != y_prime:
                    # w = w + nyx
                    self.w = self.w + self.learning_rate * y * x
    
    def save(self, filepath):
        f = open(filepath, 'wb')
        pickle.dump(self, f)
        f.close()
