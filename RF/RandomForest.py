#Code adapted from: https://www.datacamp.com/tutorial/random-forests-classifier-python 

#imports
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics

def train(features, labels):
    #define features and labels
    X = features #Globals.features (kmers)
    y = labels #logFC

    #split into training and test set
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3) # 70% training and 30% test

    #Create a Gaussian Classifier
    clf=RandomForestClassifier(n_estimators=100)

    #Train the model
    clf.fit(X_train,y_train)

    #Form predictions
    y_pred=clf.predict(X_test)

    #Print accuracy of the model
    print("Accuracy:",metrics.accuracy_score(y_test, y_pred))
