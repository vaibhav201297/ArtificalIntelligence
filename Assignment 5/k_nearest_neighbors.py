# k_nearest_neighbors.py: Machine learning implementation of a K-Nearest Neighbors classifier from scratch.
#
# Submitted by: [enter your full name here] -- [enter your IU username here]
#
# Based on skeleton code by CSCI-B 551 Fall 2021 Course Staff

from os import PRIO_PGRP
import numpy as np
from sklearn.metrics.pairwise import distance_metrics, euclidean_distances
from utils import euclidean_distance, manhattan_distance


class KNearestNeighbors:
    train_data=np.array([])
    labels=np.array([])
    """
    A class representing the machine learning implementation of a K-Nearest Neighbors classifier from scratch.

    Attributes:
        n_neighbors
            An integer representing the number of neighbors a sample is compared with when predicting target class
            values.

        weights
            A string representing the weight function used when predicting target class values. The possible options are
            {'uniform', 'distance'}.

        _X
            A numpy array of shape (n_samples, n_features) representing the input data used when fitting the model and
            predicting target class values.

        _y
            A numpy array of shape (n_samples,) representing the true class values for each sample in the input data
            used when fitting the model and predicting target class values.

        _distance
            An attribute representing which distance metric is used to calculate distances between samples. This is set
            when creating the object to either the euclidean_distance or manhattan_distance functions defined in
            utils.py based on what argument is passed into the metric parameter of the class.

    Methods:
        fit(X, y)
            Fits the model to the provided data matrix X and targets y.

        predict(X)
            Predicts class target values for the given test data matrix X using the fitted classifier model.
    """



    def __init__(self, n_neighbors = 5, weights = 'uniform', metric = 'l2'):
        # Check if the provided arguments are valid
        if weights not in ['uniform', 'distance'] or metric not in ['l1', 'l2'] or not isinstance(n_neighbors, int):
            raise ValueError('The provided class parameter arguments are not recognized.')

        # Define and setup the attributes for the KNearestNeighbors model object
        self.n_neighbors = n_neighbors
        self.weights = weights
        self._X = None
        self._y = None
        self._distance = euclidean_distance if metric == 'l2' else manhattan_distance

    def fit(self, X, y):
        """
        Fits the model to the provided data matrix X and targets y.

        Args:
            X: A numpy array of shape (n_samples, n_features) representing the input data.
            y: A numpy array of shape (n_samples,) representing the true class values for each sample in the input data.

        Returns:
            None.
        """
        if len(X)!=len(y):
            raise Exception('The length of X and Y does not match')
        self.train_data=X
        self.labels=y      

    def predict(self, X):
        """
        Predicts class target values for the given test data matrix X using the fitted classifier model.

        Args:
            X: A numpy array of shape (n_samples, n_features) representing the test data.

        Returns:
            A numpy array of shape (n_samples,) representing the predicted target class values for the given test data.
        """
        print()
        distances=[]
        for i in range(len(X)):
            dist_with_train=[]
            for j in range(len(self.train_data)):
                dist=self._distance(X[i],self.train_data[j])
                dist_with_train.append((dist,self.labels[j]))
            distances.append(dist_with_train)
        nearest_neighbours=[]
        for i in range(len(distances)):
            distances[i].sort(key=lambda tup:tup[0])
            nearest_neighbours.append(distances[i][:self.n_neighbors])
        final_clusters=[]
        for row in nearest_neighbours:
            cluster={}
            dist={}
            for x,y in row:
                if y in cluster:
                    cluster[y]+=1
                    dist[y]=dist[y]+1/x
                else:
                    cluster[y]=1
                    dist[y]=1/x
            #print(cluster)
            if self.weights=='uniform':
                temp=0
                for x in cluster:
                    if cluster[x]>temp:
                        temp=cluster[x]
                        temp2=x
                final_clusters.append(temp2)
            else:
                if len(cluster)==1:
                    final_clusters.append(list(cluster.keys())[0])
                else:
                    #print(dist)
                    keys=list(dist.keys())
                    vals=list(dist.values())
                    mx=keys[vals.index(max(vals))]
                    final_clusters.append(mx)
        #print(final_clusters)
        return final_clusters
    
    
       

