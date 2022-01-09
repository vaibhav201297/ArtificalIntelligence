# multilayer_perceptron.py: Machine learning implementation of a Multilayer Perceptron classifier from scratch.
#
# Submitted by: Vaibhav Vishwanath : 2000912419
#
# Based on skeleton code by CSCI-B 551 Fall 2021 Course Staff
# Code Reference : https://pabloinnsente.github.io/the-multilayer-perceptron
import warnings
import numpy as np
from numpy.lib import gradient
from utils import identity, sigmoid, tanh, relu, softmax, cross_entropy, one_hot_encoding
warnings.filterwarnings("ignore", category=RuntimeWarning)


class MultilayerPerceptron:
    """
    A class representing the machine learning implementation of a Multilayer Perceptron classifier from scratch.

    Attributes:
        n_hidden
            An integer representing the number of neurons in the one hidden layer of the neural network.

        hidden_activation
            A string representing the activation function of the hidden layer. The possible options are
            {'identity', 'sigmoid', 'tanh', 'relu'}.

        n_iterations
            An integer representing the number of gradient descent iterations performed by the fit(X, y) method.

        learning_rate
            A float representing the learning rate used when updating neural network weights during gradient descent.

        _output_activation
            An attribute representing the activation function of the output layer. This is set to the softmax function
            defined in utils.py.

        _loss_function
            An attribute representing the loss function used to compute the loss for each iteration. This is set to the
            cross_entropy function defined in utils.py.

        _loss_history
            A Python list of floats representing the history of the loss function for every 20 iterations that the
            algorithm runs for. The first index of the list is the loss function computed at iteration 0, the second
            index is the loss function computed at iteration 20, and so on and so forth. Once all the iterations are
            complete, the _loss_history list should have length n_iterations / 20.

        _X
            A numpy array of shape (n_samples, n_features) representing the input data used when fitting the model. This
            is set in the _initialize(X, y) method.

        _y
            A numpy array of shape (n_samples, n_outputs) representing the one-hot encoded target class values for the
            input data used when fitting the model.

        _h_weights
            A numpy array of shape (n_features, n_hidden) representing the weights applied between the input layer
            features and the hidden layer neurons.

        _h_bias
            A numpy array of shape (1, n_hidden) representing the weights applied between the input layer bias term
            and the hidden layer neurons.

        _o_weights
            A numpy array of shape (n_hidden, n_outputs) representing the weights applied between the hidden layer
            neurons and the output layer neurons.

        _o_bias
            A numpy array of shape (1, n_outputs) representing the weights applied between the hidden layer bias term
            neuron and the output layer neurons.

    Methods:
        _initialize(X, y)
            Function called at the beginning of fit(X, y) that performs one-hot encoding for the target class values and
            initializes the neural network weights (_h_weights, _h_bias, _o_weights, and _o_bias).

        fit(X, y)
            Fits the model to the provided data matrix X and targets y.

        predict(X)
            Predicts class target values for the given test data matrix X using the fitted classifier model.
    """

    def __init__(self, n_hidden = 16, hidden_activation = 'sigmoid', n_iterations = 1000, learning_rate = 0.01):
        # Create a dictionary linking the hidden_activation strings to the functions defined in utils.py
        activation_functions = {'identity': identity, 'sigmoid': sigmoid, 'tanh': tanh, 'relu': relu}

        # Check if the provided arguments are valid
        if not isinstance(n_hidden, int) \
                or hidden_activation not in activation_functions \
                or not isinstance(n_iterations, int) \
                or not isinstance(learning_rate, float):
            raise ValueError('The provided class parameter arguments are not recognized.')

        # Define and setup the attributes for the MultilayerPerceptron model object
        self.n_hidden = n_hidden
        self.hidden_activation = activation_functions[hidden_activation]
        self.n_iterations = n_iterations
        self.learning_rate = learning_rate
        self._output_activation = softmax
        self._loss_function = cross_entropy
        self._loss_history = []
        self._X = None
        self._y = None
        self._h_weights = None
        self._h_bias = None
        self._o_weights = None
        self._o_bias = None

    def _initialize(self, X, y):
        """
        Function called at the beginning of fit(X, y) that performs one hot encoding for the target class values and
        initializes the neural network weights (_h_weights, _h_bias, _o_weights, and _o_bias).

        Args:
            X: A numpy array of shape (n_samples, n_features) representing the input data.
            y: A numpy array of shape (n_samples,) representing the true class values for each sample in the input data.

        Returns:
            None.
        """

        self._X = X
        self._y = one_hot_encoding(y)

        np.random.seed(42)
        #print("Number of Features")
        #print(len(X[0]))
        #print("Number of Hidden Layers")
        #print(self.n_hidden)
        self._h_weights=np.random.rand(len(X[0]),self.n_hidden)
        #print()
        #print(self._h_weights)
        self._h_bias=np.ones((1,self.n_hidden))
        #print(self._h_bias)
        self._o_weights=np.random.rand(self.n_hidden,len(self._y[0]))
        self._o_bias=np.ones((1,len(self._y[0])))
        #print(self._o_weights)
        #print()
        #print(self._o_bias)
        return None
    



    def fit(self, X, y):
        """
        Fits the model to the provided data matrix X and targets y and stores the cross-entropy loss every 20
        iterations.

        Args:
            X: A numpy array of shape (n_samples, n_features) representing the input data.
            y: A numpy array of shape (n_samples,) representing the true class values for each sample in the input data.

        Returns:
            None.
        """

        self._initialize(X, y)
        #print(X.shape)
        while(self.n_iterations>0):
            self.n_iterations-=1

            #ForwarD Propogation
            z=X @ self._h_weights +self._h_bias
            op=self.hidden_activation(z,False)
            
            z2=op @ self._o_weights+self._o_bias
            
            op2=self._output_activation(z2,False)
           
            #Back Propogation

            error=(op2-self._y)
            #error=self._loss_function(self._y,op2)

            delta=error*self._output_activation(op2,True)
            op_gradient=op.T @ delta
            self._o_weights=self._o_weights-self.learning_rate*op_gradient
            #self._o_bias=self._o_bias-np.sum(delta,axis=0,keepdims=True)*self.learning_rate


            delta1=(delta @ self._o_weights.T)*self.hidden_activation(op,True)
            gradient1=X.T @ delta1
            self._h_weights=self._h_weights-gradient1*self.learning_rate
            #self._h_bias=self._h_bias-np.sum(delta1,axis=0,keepdims=True)*self.learning_rate
            if self.n_iterations % 20 ==0:
                self._loss_history.append(self._loss_function(self._y,op2))

            
            


        

    def predict(self, X):
        """
        Predicts class target values for the given test data matrix X using the fitted classifier model.

        Args:
            X: A numpy array of shape (n_samples, n_features) representing the test data.

        Returns:
            A numpy array of shape (n_samples,) representing the predicted target class values for the given test data.
        """
        z=X @ self._h_weights +self._h_bias
        op=self.hidden_activation(z,False)      
        z2=op @ self._o_weights+self._o_bias
        op2=self._output_activation(z2,False)
        predictions=[]
        for i in range(len(op2)):
            predictions.append(np.argmax(op2[i]))
        #print(predictions)
        return predictions        
            


