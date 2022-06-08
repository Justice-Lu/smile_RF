#Code adapted from: https://www.datacamp.com/tutorial/random-forests-classifier-python 

#imports
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn import metrics

def train(features, labels):
    #define features and labels
    X = features #Globals.features (kmers)
    y = labels #logFC

    #split into training and test set
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3) # 70% training and 30% test

    #Create a Gaussian Regression
    clf=RandomForestRegressor(n_estimators=100)

    #Train the model
    clf.fit(X_train,y_train)

    #Form predictions
    y_pred=clf.predict(X_test)
    print(y_pred)
    print(y_test)

    #Print accuracy of the model
    print("Accuracy:",metrics.r2_score(y_test, y_pred))

dummyX = [[2,2,2,2],[3,3,3,3],[4,4,4,4],[5,5,5,5],[6,6,6,6],[7,7,7,7],[8,8,8,8],[9,9,9,9],[10,10,10,10],[1,1,1,1]]
dummyY = [2,3,4,5,6,7,8,9,10,1]
train(dummyX, dummyY)