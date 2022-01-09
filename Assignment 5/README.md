<h2> Elements of Artifiial Intelligence Assignment 4 </h3>
<h3> Vaibhav Vishwanath : vavish : 2000912419 </h4>

In this assignment, we try to implement K nearest neigbours and Multi-Layer Perceptron from scratch.

<h4> K Nearest Neighbors </h4>
In this implementation of KNN based on the skeleton code by Prof. Crandall, we implement the utility functions : euclidean_distance, manhattan_distance to find the distances between the test data and the train data. Since KNN is a non parametric method, there is no training required. <br/>
During testing, we compute the distances to all train data and choose the nearest neigbours based on parameter.<br/>
To decide the label of the test_data: we have used 2 methods:
<ul><li> Uniform : Each neighbour will get uniform votes </li>
<li> Distance : Each neighbour gets a vote inversely proportional to the distance </li></ul>

<h4> Multi Layer Perceptron </h4>
In this implementaion of Multi-Layer Perceptron based on the skeleton code by Prof. Crandall, we implement the utility functions : identity, sigmoid,tanh,relu, cross-entropy and one_hot_encoding functions. <br/>
We start with the forward propogation in which we predict the output values based on random initialization of hidden layer weights and output layer weights.<br/>
We initialize the biases to 1.<br/>
Then, using the activation functions : identity, ReLu, tanh, sigmoid , we compute which neurons get activated and update the weights accordingly.<br/>
We use Back Propogation to update the weights. We compute the error of the predicted labels and the ground truth and then using Gradient Descent, we update the output layer weights and then, using the output layer weights, we update the hidden layer weights on the basis of multiple learning rates.
<h5> Problems Faced </h5>
The problem faced during training and weight updation is when the values reach NaN due to which the weight updation begins to break. 

<h5> References</h5>
https://pabloinnsente.github.io/the-multilayer-perceptron


