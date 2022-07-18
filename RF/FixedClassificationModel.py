#This script is a Classification Random Forest Model with Undersampling
#Code adapted from: https://www.datacamp.com/tutorial/random-forests-classifier-python 

#imports
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics

def train(features, labels):
    #define features and labels
    X = features #Kmers
    y = labels #Binds or not

    #split into training and test set
    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y,test_size=0.1) # 90% training and 10% test

    #compare to random undersampling

    #Create a Gaussian Regression
    clf=RandomForestClassifier(n_estimators=100, class_weight="balanced") #add in , class_weight="balanced"
    #Train the model
    clf.fit(X_train,y_train)

    #Form predictions
    y_pred=clf.predict_proba(X_test)[:,1]
    precision, recall, thresholds = metrics.precision_recall_curve(y_test, y_pred)

    acc = metrics.roc_auc_score(y_test, y_pred)
    rec = metrics.auc(recall,precision)
    #Print accuracy of the model
    #print("Accuracy:",acc)
    #print("Recall:",rec)

    y_pred=clf.predict(X_test)

    mat = (metrics.matthews_corrcoef(y_test, y_pred))
    bac = metrics.balanced_accuracy_score(y_test, y_pred)
    #print('Balanced Accuracy Score: ' + str(bac))

    TN, FN, TP, FP = matthew_counts(y_test, y_pred)

    return acc,rec,bac,mat,TN, FN, TP, FP

def matthew_counts(y_test, y_pred):
    TN = 0
    FN = 0
    TP = 0
    FP = 0

    for i in range(len(y_test)):
        if (y_test[i] == 0) & (y_pred[i] == 0):
            TN += 1
        if (y_test[i] == 1) & (y_pred[i] == 0):
            FN += 1
        if (y_test[i] == 1) & (y_pred[i] == 1):
            TP += 1
        if (y_test[i] == 0) & (y_pred[i] == 1):
            FP += 1
    return TN, FN, TP, FP

def neutral_train(features, labels, n_features, proteins, ligands):
    X = features
    Y = labels
    X_n = n_features
    clf = RandomForestClassifier(n_estimators=100, class_weight="balanced")  # add in , class_weight="balanced"
    X_train, X_test, y_train, y_test = train_test_split(X, Y, stratify=Y, test_size=0.1)  # 90% training and 10% test
    # Train the model
    clf.fit(X_train, y_train)

    n_pred = clf.predict(X_n)

    num_proteins = len(proteins)
    num_ligands = len(ligands)

    f = open('neutral_pair_predictions.txt', "w")

    i = 0
    for p in n_pred:
        p_ind = i // num_ligands
        l_ind = i % p_ind

        f.write(proteins[p_ind] + "\t" + ligands[l_ind] + "\t" + str(p) + "\n")
        i += 1




