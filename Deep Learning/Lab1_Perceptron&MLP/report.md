# Assignment 1

name: 王炜皓

sid: 11710403

last edited: 2020/4/2



# Part I - the Perceptron

Task 1 : Using `random` module in python to generate data, see `data_generator.py`

Task 2 : Implement perceptron, see `perceptron.py`

Task 3 : Train and analyze the perceptron with different dataset, see `test.py`

Task 4 : Three different experiments.

Others

1. The generated data and trained network can be saved in local machine to save time, see `save/`

2. plot the classifier

   ​	The input is 2-D and the output is 1-D, they constructs a 3-D space, thus the classifier is actually a 2-D panel. The expression is

$$
\tilde{y} = w_1x_1+w_2x_2+b
$$

​			The figure is shown in y = 0, thus let $\tilde{y} = 0$, we have $x_2 = - \frac{w_1x_1+b}{w_2}$, a line in 2-D figure.




#### Experiment 1: well separated distribution 

<img src="C:\Users\ASUS\AppData\Roaming\Typora\typora-user-images\image-20200319172658183.png" alt="image-20200319172658183" style="zoom: 50%;" />

​                                                                   *Figure 1. well separated distribution*



##### Dataset

First sample 100 points (blue points in the figure) from Gaussian distribution $A$( $\mu = 0,  $$\sigma = 2$), then sample another 100 points (orange points in the figure) from Gaussian distribution $B(\mu = 12, \sigma = 3)$.

##### Hyperparameters

epoch: $10^{4}$

learning rate: $10^{-2}$

##### Results

Points used to do testing are shown in the figure (green points)

$w^{\mathrm{T}} = [ 0.22,-0.0402492,-0.01550595]$, the blue line shown in the figure

accuracy: 100.0%



#### Experiment 2: high variance

<img src="C:\Users\ASUS\AppData\Roaming\Typora\typora-user-images\image-20200319172800765.png" alt="image-20200319172800765" style="zoom: 50%;" />

​                                                                                 *Figure 2. high variance*



##### Dataset

First sample 100 points (blue points in the figure) from Gaussian distribution $A$( $\mu = 0,  $$\sigma = 7$), then sample another 100 points (orange points in the figure) from Gaussian distribution $B(\mu = 12, \sigma = 7)$.

##### Hyperparameters

epoch: $10^{4}$

learning rate: $10^{-2}$

##### Results

Points used to do testing are shown in the figure (green points)

$w^{\mathrm{T}} = [ 2.15,       -0.22855528, -0.12826092]$, the blue line shown in the figure

accuracy: 90%



#### Experiment 3: Close distribution

<img src="C:\Users\ASUS\AppData\Roaming\Typora\typora-user-images\image-20200319172849778.png" alt="image-20200319172849778" style="zoom: 50%;" />

​                                                                              *Figure 3. close distribution*



##### Dataset

First sample 100 points (blue points in the figure) from Gaussian distribution $A$( $\mu = 0,  $$\sigma = 3$), then sample another 100 points (orange points in the figure) from Gaussian distribution $B(\mu = 1, \sigma = 4)$.

##### Hyperparameters

epoch: $10^{4}$

learning rate: $10^{-2}$

##### Results

Points used to do testing are shown in the figure (green points)

$w^{\mathrm{T}} = [ 0.02,       -0.01164701,  0.0355244 ]$, the blue line shown in the figure

accuracy: 47.5%



## Analysis of Perceptron

If the means of the two Gaussian distribution are too close or if their variances are too high, the accuracy of the prediction can be terribly bad. The reason is that **the perceptron is a linear classifier**. If the means are close or variances are high, these two distributions are "mixed", as shown in the figure. There is no line can separate them perfectly in this case (not considering kernel methods). If the means are not close and variances are relatively small, according to the **three-sigma rule**, almost all the points of these two distributions can be separated by a single line.











# Part II - the multi-layer perceptron

#### Task 1.1 Implement modules

The computation formulas are from some references. Reference: `Lecture_4_part_2.pdf`

Other individual works:

1) Initialization: Since the activation function is `ReLU`, the initial values of weight are sample from:
$$
W_{ij} \sim N(0, \sqrt{\frac{2}{m}})
$$
, where $m$ is the number of inputs. The bias are all zeros at the beginning.



2) SoftMax
$$
z_i = \frac{e^{x_i}}{\sum_k e^{x_k}}
$$
, where $z_i$ is $i$-th element of the output.

To compute the Jacobian matrix, $\frac{\part z_j}{\part x_i}$ should be known.

if $i \neq j$: 
$$
\frac{\part z_j}{\part x_i} = \frac{-e^{x_i}e^{x_j}}{(\sum_k e^{x_k})^2} = -\frac{e^{x_i}}{\sum_k e^{x_k}}\frac{e^{x_j}}{\sum_k e^{x_k}} = -z_iz_j
$$
if $i = j$:
$$
\frac{\part z_j}{\part x_i} = \frac{e^{x_j}\sum_ke^{x_k} - e^{x_j}e^{x_i}}{(\sum_k e^{x_k})^2} = \frac{e_{x_j}}{\sum_k e^{x_k}}(1 -\frac{e^{x_i}}{\sum_k e^{x_k}}) = z_i(1-z_j)
$$
Thus, $d_{x}$ can be computed by:
$$
{d_x}_i = z_i(d_i - z^{\mathrm{T}}d_{out})
$$
Then the backward function of SoftMax can be easily realized by:

```python
def backward(self, dout):
    return  self.z * (dout - np.dot(dout, self.z.T))
```



#### Task 1.2 Implement Multiple-Layer Perceptron

The MLP is implemented by `OrderedDict` in python module `collections`. 



#### Task 2.1 Implement the training program for MLP

There are several method in `train_mlp_numpy.py`, the call hierarchy of these methods is:

![image-20200402144152120](C:\Users\ASUS\AppData\Roaming\Typora\typora-user-images\image-20200402144152120.png)

​                                                                              *Figure 4. Call hierarchy*



The training process is described as follows:

1. Data preprocessing: 1) zero-centered 2) normalization

<img src="C:\Users\ASUS\AppData\Roaming\Typora\typora-user-images\image-20200402144720870.png" alt="image-20200402144720870" style="zoom:50%;" />

​                                                                              *Figure 5. data preprocessing*



The blue points are data before preprocessing, the orange points are data after preprocessing.

2. Initialization: Instantiate a MLP, select an optimizer and initial some hyperparameters according to the use input.

3. Train: Repeatedly call `optimizer.train_step()` to train the MLP and evaluate the MLP in every predefined time interval. 



#### Task 2.2 Implement Optimizer for training MLP

The `train_step()` is realized as the follow description:

​	1) Shuffle the dataset, and then split it into many mini-batches according to the batch size. Then finish these mini-batch in one epoch. 

​	2) For every mini-batch, do forward and backward for every piece of data and then accumulate the gradients after every backward operation. After finishing one mini-batch, Divide every accumulated gradients by batch size and then use them to update the corresponding parameters in MLP. The python code to describe this process is like:

```python
# update
for i in range(1, self.mlp.layer_cnt + 1):
 dw = accumulate_grad['weight_{}'.format(i)] / batch_size
 db = accumulate_grad['bias_{}'.format(i)]   / batch_size
 self.mlp.layers['layer_{}_Affine'.format(i)].params['weight'] -= self.learning_rate*dw
 self.mlp.layers['layer_{}_Affine'.format(i)].params['bias'] -= self.learning_rate*db
```

Though this is the implementation of Stochastic Gradient Descent, it can also perform Batch Gradient Descent. Just simply set the batch-size to the number of data in the training dataset.

**Adam** is also implemented in `optimizer.py`. And **Adam** dramatically change the convergence rate of the batch gradient descent:



#### Task 3 Show the accuracy curves for both training data and test data

The jupyter notebook is written in `part2.ipynb`

Batch Gradient Descent: `lr = 0.01`

![image-20200402152356040](C:\Users\ASUS\AppData\Roaming\Typora\typora-user-images\image-20200402152356040.png)

​                                                                              *Figure 6b. BGD(lr=0.01)*                                                                



Batch Gradient Descent with **Adam**: `lr = 0.01`

![image-20200402152819004](C:\Users\ASUS\AppData\Roaming\Typora\typora-user-images\image-20200402152819004.png)

​                                                                       *Figure 6. BGD with Adam(lr=0.01)*                             



#### Other works

Visualization of the classifier

Case 1 : epoch : 1490. train accuracy: 95.00% test accuracy: 95.50%. train loss: 0.14033. test loss: 0.13550

<img src="C:\Users\ASUS\AppData\Roaming\Typora\typora-user-images\image-20200403104545097.png" alt="image-20200403104545097" style="zoom:50%;" />

​                                                                              *Figure 8. BGD (lr=0.01)*

Case 2 :  epoch: 90. train accuracy: 100.00% test accuracy: 100.00%. train loss: 0.00135. test loss: 0.00092

<img src="C:\Users\ASUS\AppData\Roaming\Typora\typora-user-images\image-20200403104847736.png" alt="image-20200403104847736" style="zoom: 50%;" />

​                                                                    *Figure 9. SGD (lr=0.01 batch-size=1)*



# Part III Stochastic Gradient Descent

#### Task 1 Modify the train method to accept a parameter

The train method is defined by:

```python
def train(dataset=None, dataset_test=None, mlp=None, use_optimizer=OPTIMIZER_DEFAULT,
    learning_rate=LEARNING_RATE_DEFAULT, max_steps=MAX_EPOCHS_DEFAULT, eval_freq=EVAL_FREQ_DEFAULT, batch_size=BATCH_SIZE_DEFAULT)
```

To use **batch gradient descent**, user can simply call `train(batch_size=<Size of training dataset>)` . For example, if the training dataset has 800 data in total, then `train(batch_size=800)` is called.

To use **stochastic gradient descent**, user can simply call `train(batch_size=<Size of mini-batch)`. For example, if the user want to use SGD with mini-batch size of 1, then `train(bath_size=1)` is called.



#### Task 2 Show the accuracy curves

The jupyter notebook is written in `part2.ipynb`

Since the accuracy is converged really quickly, `max_steps` is set to 100 and `eval_freq` is set to 1.

Stochastic Gradient Descent: `lr = 0.01, batch size = 1`

![image-20200402162027942](C:\Users\ASUS\AppData\Roaming\Typora\typora-user-images\image-20200402162027942.png)

​                                                                  *Figure 10. SGD (lr=0.01 batch-size=1)*                   



Stochastic Gradient Descent: `lr = 0.01, batch size = 16`

![image-20200402162110521](C:\Users\ASUS\AppData\Roaming\Typora\typora-user-images\image-20200402162110521.png)

​                                                                  *Figure 11. SGD (lr=0.01 batch-size=16)*                     



Stochastic  Gradient Descent with **Adam**: `lr = 0.01, batch size = 16`

![image-20200402162210653](C:\Users\ASUS\AppData\Roaming\Typora\typora-user-images\image-20200402162210653.png)

​                                                            *Figure 12. SGD with Adam (lr=0.01 batch-size=16)*               



## Results and Analysis of MLP

#### BGD and SGD 

​    Since the dataset is perfect and with no noise at all. MLP with one layer which contains only 20 neurons should be able to be trained to perfectly classify the data. Figure 8. shows that SGD achieve 100% accuracy in 5 epochs. However Figure 6. shows that BGD cannot achieve 100% accuracy within 1500 epochs. This is because SGD update parameters multiple times within one epochs where BGD only update parameters once. To verify this statement, a training experiment with longer epochs is done:

![image-20200402180427695](C:\Users\ASUS\AppData\Roaming\Typora\typora-user-images\image-20200402180427695.png)

​                                                                       *Figure 13. BGD (lr=0.01)*       



![image-20200402180549497](C:\Users\ASUS\AppData\Roaming\Typora\typora-user-images\image-20200402180549497.png)

​                                                          *Figure 14. training result in process. BGD (lr=0.01)*       



In this experiment, the BGD achieved 100% accuracy within 4,000 epochs. This means BGD updates its parameters about 4,000 times to achieved this accuracy. In SGD, it only use 5 epochs to achieve this accuracy. This is because SGD updates the parameters 800 times in every epochs. 5 epochs means 4,000 updates are operated. This experiment also shows that SGD outperforms BGD. The data is too perfect distributed might be the reason why SGD can achieve the same accuracy in same number of epochs as the BGD since BGD nearly use the actual gradients to update the parameters.



#### Using Optimizer Adam to train

​    BGD takes relatively long time to train a good model. To reduce the training epochs to train a good model, Adam is implemented and another experiment using Adam to train is done:

![image-20200402182746252](C:\Users\ASUS\AppData\Roaming\Typora\typora-user-images\image-20200402182746252.png)

​                                                                      *Figure 15. BGD with Adam (lr=0.01)*       



In this experiment, the accuracy achieve 100% within 250 epochs which is much smaller than 4,000 epochs. To show that Adam works in every circumstance with this dataset. One more experiment using SGD and Adam is done:

![image-20200402183230756](C:\Users\ASUS\AppData\Roaming\Typora\typora-user-images\image-20200402183230756.png)

​                                                              *Figure 16. SGD with Adam (lr=0.01 batch-size=1)*       



The curves shows that the model achieve 100% accuracy within 3 epochs. This experiment shows that Adam can also work well in SGD.

