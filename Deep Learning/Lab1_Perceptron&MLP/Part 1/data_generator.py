import random
import pickle
import numpy as np
import config
import matplotlib.pyplot as plt

class pts_set():

    def __init__(self, data=None, size=0, x=None, y=None):
        if data == None:
            self.arr = []
            self.size = size
            for i in range(0, size):
                self.arr.append(np.array([x[i], y[i]]))
        else:
            self.arr = data
            self.size = len(data)

    def save(self, file_path):
        f = open(file_path, 'wb')
        pickle.dump(self, f)
        f.close()

    def __str__(self):
        return self.arr

    @staticmethod
    def separate(pts_set_instance, train_percentage):
        total_size = pts_set_instance.size
        train_size = int(total_size * train_percentage)
        train_data = pts_set_instance.arr[0 : train_size]
        test_data  = pts_set_instance.arr[train_size : total_size]
        return pts_set(data=train_data), pts_set(data=test_data)

    @staticmethod
    def load(file_path):
        f = open(file_path, 'rb')
        rtn = pickle.load(f)
        f.close()
        return rtn

class gauss_dis():
    
    def __init__(self, mean, sigma, size):
        self.mean = mean
        self.sigma = sigma
        self.size = size

        self.k = 1 / (np.sqrt(2 * np.pi) * sigma)
        self.n = 2 * sigma * sigma

        self.x = np.random.default_rng().normal(mean, sigma, size)
        # self.y = self._f(self.x)
        self.y = np.random.default_rng().normal(mean, sigma, size)

    def _f(self, x):
        return self.k * (np.e** ((-(x - self.mean)*(x - self.mean))/self.n))
    
    def draw(self):
        plt.scatter(self.x, self.y)
        plt.show()

    def save(self, dirpath=''):
        f = open("save/mean={}_sigma={}_size={}.pkl".format(self.mean, self.sigma, self.size), 'wb')
        pickle.dump(self, f)
        f.close()
    
    @staticmethod
    def load(mean, sigma, size, dirpath=''):
        f = open("save/mean={}_sigma={}_size={}.pkl".format(mean, sigma, size), 'rb')
        rtn = pickle.load(f)
        f.close()
        return rtn

    @staticmethod
    def new(mean, sigma, size, dirpath=''):
        g = gauss_dis(mean, sigma, size)
        if config.SAVE_FILE:
            g.save(dirpath)
        return gauss_dis.load(mean, sigma, size)
    
    @staticmethod
    def load_or_new(mean, sigma, size, dirpath=''):
        try:
            return gauss_dis.load(mean, sigma, size, dirpath)
        except:    
            return gauss_dis.new(mean, sigma, size, dirpath)