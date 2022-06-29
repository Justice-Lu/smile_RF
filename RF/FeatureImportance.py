#This script extracts feature importance
#Code adapted from: https://www.datacamp.com/tutorial/random-forests-classifier-python 
#and https://scikit-learn.org/stable/auto_examples/ensemble/plot_forest_importances.html

#imports
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from imblearn.over_sampling import ADASYN
import numpy as np
import pandas as pd
import matplotlib as plt

def train(features, labels, filter_feat, filter_feat2, ligand_features):
    #define features and labels
    X = features #Kmers
    y = labels #Binds or not

    #split into training and test set
    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y,test_size=0.1) # 90% training and 10% test

    #Oversampling was necessary, because most ligand/receptor pairs do not bind in our dataset
    ros = ADASYN()

    X_res, y_res = ros.fit_resample(X_train, y_train)

    #Create a Gaussian Regression
    clf=RandomForestClassifier(n_estimators=100)

    #Train the model
    clf.fit(X_res,y_res)

    #Finding most important features
    filter_feat.extend(filter_feat2) #Feature names
    filter_feat.extend(ligand_features)

    importances = clf.feature_importances_

    #Picking the 10 most important features
    for i in range(0, 10):
        index = np.argmax(importances)
        importances[index] = 0
        print(filter_feat[index])