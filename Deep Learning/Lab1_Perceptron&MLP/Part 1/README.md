# Part 1: perceptron

#### run directly [important]

```bash
python test.py
```

The program will load the trained network and generated data directly. Thus, it should be fast.

#### start a new experiment [optional]

To start an experiment, you need to open `test.py` and call `process_experiment` with specified parameters. For example,

```python
process_experiment(mean_1=0, sigma_1=2, mean_2=3, sigma_2=2, size=100, train_percentage=0.8)
```

Then it will generate two distribution, one with mean value 0, variance 2 and another with mean value 3 and variance 2. The total size is 200 and 80% of the points will be used for training.

#### Modify hyperparameters and other settings [optional]

Open `config.py` and you can change some predefined settings

```python
DEBUG = True
VERBOSE = True
SAVE_FILE = True
EPOCH = 1e4
LEARNING_RATE = 1e-2
```

`DEBUG` and `VERBOSE` are used to determine whether to print some information on the screen during the program is running.

`SAVE_FILE` is used to determine whether to save the trained network and generated data to local machine.

`EPOCH` and `LEARNING_RATE` are hyperparameters of the perceptron.

