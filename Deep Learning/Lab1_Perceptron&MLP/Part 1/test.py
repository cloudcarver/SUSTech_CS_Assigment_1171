from data_generator import gauss_dis, pts_set
from perceptron import Perceptron
import matplotlib.pyplot as plt
import numpy as np
import pickle
import config
import argparse

def _generate_dataset(mean, sigma, size, label, train_percentage):
    g = gauss_dis.load_or_new(mean=mean, sigma=sigma, size=size)
    dataset_all = pts_set(size=size, x=g.x, y=g.y)
    train_x, test_x = pts_set.separate(dataset_all, train_percentage=train_percentage)
    train_label = np.dot(label, np.ones(int(size * train_percentage)))
    test_label = np.dot(label, np.ones(size - int(size * train_percentage)))
    return g, train_x.arr, train_label, test_x.arr, test_label 

def process_experiment(mean_1, sigma_1, mean_2, sigma_2, size, train_percentage):
    # generate or read dataset
    a, a_train_x, a_train_label, a_test_x, a_test_label = _generate_dataset(mean=mean_1, sigma=sigma_1, size=size, label=1, train_percentage=train_percentage)
    b, b_train_x, b_train_label, b_test_x, b_test_label = _generate_dataset(mean=mean_2, sigma=sigma_2, size=size, label=-1, train_percentage=train_percentage)
    train_x = a_train_x + b_train_x
    train_label = np.concatenate((a_train_label, b_train_label))
    test_x = a_test_x + b_test_x
    test_label = np.concatenate((a_test_label, b_test_label))
    
    # train a new network or load a network if exists
    try:
        network = pickle.load(open("save/perceptron_u1{}v1{}u2{}v2{}s{}p{}.pkl".format(mean_1, sigma_1, mean_2, sigma_2, size, train_percentage), 'rb'))
    except:
        network = Perceptron(2, max_epochs=config.EPOCH, learning_rate=config.LEARNING_RATE)
        network.train(train_x, train_label)
        if config.SAVE_FILE:
            network.save("save/perceptron_u1{}v1{}u2{}v2{}s{}p{}.pkl".format(mean_1, sigma_1, mean_2, sigma_2, size, train_percentage))
    
    # analysis

    cnt = 0
    test_size = len(test_x)
    for i in range(0, test_size):
        x = test_x[i]
        y_prime = network.forward(np.array(x))
        y = test_label[i]
        if config.DEBUG:
            print("input:{}, output:{}, ground truth:{}".format(x, y_prime, y))
        if y_prime == y:
            cnt = cnt + 1
    print("training parameters: {}".format(network.w))
    print("accuracy is {}%".format(100*cnt/test_size))

    # plot: scatter all data
    plt.scatter(a.x, a.y)
    plt.scatter(b.x, b.y)
    
    # plot: scatter test data
    cx = []
    cy = []
    for i in range(0, test_size):
        cx.append(test_x[i][0])
        cy.append(test_x[i][1])
    plt.scatter(cx, cy)
    
    # plot: separator
    x1, x2 = min(mean_1, mean_2) - 2 * max(sigma_1, sigma_2), max(mean_1, mean_2) + 2 * max(sigma_1, sigma_2)
    w0, w1, w2 = network.w[0], network.w[1], network.w[2]
    y1 = - (w1 * x1 + w0) / w2
    y2 = - (w1 * x2 + w0) / w2
    plt.plot([x1, x2], [y1, y2])
    plt.show()

def experiment_1():
    process_experiment(mean_1=0, sigma_1=2, mean_2=12, sigma_2=3, size=100, train_percentage=0.8)

def experiment_2():
    process_experiment(mean_1=0, sigma_1=7, mean_2=12, sigma_2=7, size=100, train_percentage=0.8)

def experiment_3():
    process_experiment(mean_1=0, sigma_1=3, mean_2=1, sigma_2=4, size=100, train_percentage=0.8)

if __name__ == "__main__":
    
    # Results are saved.
    # 1. The trained network and generated dataset are already saved in local `saves/`
    # 2. The retrains the network and regenerates the dataset, plz delete everything inside the `saves/` folder 
    #
    # Customize the training process
    # 1. Go to config.py modify the predefined hyper-parameters
    # 2. call `process_experiment` with new arguments
    #

    experiment_1()
    experiment_2()
    experiment_3()
    