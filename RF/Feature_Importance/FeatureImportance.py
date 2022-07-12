#This script extracts feature importance
#Code adapted from: https://www.datacamp.com/tutorial/random-forests-classifier-python 
#and https://scikit-learn.org/stable/auto_examples/ensemble/plot_forest_importances.html

#imports
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from imblearn.under_sampling import InstanceHardnessThreshold
import numpy as np

def train(features, labels, filter_feat):
    #define features and labels
    X = features #Kmers
    y = labels #Binds or not

    #split into training and test set
    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y,test_size=0.1) # 90% training and 10% test

    #Create a Gaussian Regression
    clf=RandomForestClassifier(n_estimators=100, class_weight="balanced")

    #Train the model
    clf.fit(X_train,y_train)

    #Finding most important features
    importances = clf.feature_importances_

    #Writes the features of the model in order of importance to the important_features.txt file
    with open("Feature_Importance/important_features.txt", "w") as f:
        while importances.size > 0:
            index = np.argmax(importances)
            print(filter_feat[index], file=f)
            print(importances[index], file=f)
            importances = np.delete(importances, index)