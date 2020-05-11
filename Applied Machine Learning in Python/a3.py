'''
In this assignment you will train several models and evaluate how effectively they predict instances of fraud using data based on this dataset from Kaggle.

Each row in fraud_data.csv corresponds to a credit card transaction. Features include confidential variables V1 through V28 as well as Amount which is the amount of the transaction.

The target is stored in the class column, where a value of 1 corresponds to an instance of fraud and 0 corresponds to an instance of not fraud.
'''
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys, os
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.dummy import DummyClassifier
from sklearn.metrics import recall_score, precision_score, confusion_matrix,\
                            precision_recall_curve, roc_curve
from sklearn.svm import SVC



sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))



__author__ = 'Chris Hilldrup'



'''
Import the data from fraud_data.csv. What percentage of the observations in the dataset are instances of fraud?

This function should return a float between 0 and 1. 
'''
def answer_one():
    df = pd.read_csv(sys.path[-1] + '/Data/fraud_data.csv')
    fraud = len(df[(df['Class'] == 1)])
    
    return fraud/len(df)



# NOTE: Following provided by Coursera
df = pd.read_csv(sys.path[-1] + '/Data/fraud_data.csv')
X = df.iloc[:,:-1]
y = df.iloc[:,-1]

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)



'''
Using X_train, X_test, y_train, and y_test (as defined above), train a dummy classifier that classifies everything as the majority class of the training data. What is the accuracy of this classifier? What is the recall?

This function should a return a tuple with two floats, i.e. (accuracy score, recall score).
'''
def answer_two():
    dc = DummyClassifier(strategy='most_frequent').fit(X_train, y_train)
    accuracy = dc.score(X_test, y_test)
    recall = recall_score(y_test, dc.predict(X_test))
    
    return accuracy, recall



'''
Using X_train, X_test, y_train, y_test (as defined above), train a SVC classifer using the default parameters. What is the accuracy, recall, and precision of this classifier?

This function should a return a tuple with three floats, i.e. (accuracy score, recall score, precision score).
'''
def answer_three():
    svc = SVC().fit(X_train, y_train)
    accuracy = svc.score(X_test, y_test)
    y_pred = svc.predict(X_test)
    recall = recall_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    
    return accuracy, recall, precision



'''
Using the SVC classifier with parameters {'C': 1e9, 'gamma': 1e-07}, what is the confusion matrix when using a threshold of -220 on the decision function. Use X_test and y_test.

This function should return a confusion matrix, a 2x2 numpy array with 4 integers.
'''
def answer_four():
    svc = SVC(C=1e9, gamma=1e-07).fit(X_train, y_train)
    y_pred = svc.decision_function(X_test) > -220
    confusion = confusion_matrix(y_test, y_pred)
    
    return confusion



'''
Train a logisitic regression classifier with default parameters using X_train and y_train.

For the logisitic regression classifier, create a precision recall curve and a roc curve using y_test and the probability estimates for X_test (probability it is fraud).

Looking at the precision recall curve, what is the recall when the precision is 0.75?

Looking at the roc curve, what is the true positive rate when the false positive rate is 0.16?

This function should return a tuple with two floats, i.e. (recall, true positive rate).
'''
def answer_five():
    log_reg = LogisticRegression(solver='liblinear').fit(X_train, y_train)
    y_prob_pred = log_reg.predict_proba(X_test)
    
    prc = precision_recall_curve(y_test, y_prob_pred[:,1])
    roc = roc_curve(y_test, y_prob_pred[:,1])
    
    fig, (ax1, ax2) = plt.subplots(1,2)
    
    # Precision_recall_curve
    ax1.plot(prc[0], prc[1])
    ax1.set_xlabel('Precision')
    ax1.set_ylabel('Recall')
    ax1.set_title('Precision Recall Curve')
    ax1.vlines(0.75, ymin=0, ymax=1)
    
    # ROC_curve
    ax2.plot(roc[0], roc[1])
    ax2.set_xlabel('False Positive Rate')
    ax2.set_ylabel('True Positive Rate')
    ax2.set_title('ROC Curve')
    ax2.vlines(.16, ymin=0, ymax=1)
    
    plt.show()
    
    recall = 0.8
    tpr = 0.9
    
    return recall, tpr
answer_five()


'''
Perform a grid search over the parameters listed below for a Logisitic Regression classifier, using recall for scoring and the default 3-fold cross validation.

'penalty': ['l1', 'l2']

'C':[0.01, 0.1, 1, 10, 100]

From .cv_results_, create an array of the mean test scores of each parameter combination. i.e.

     l1  l2
0.01  ?  ?
0.1   ?  ?
1     ?  ?
10    ?  ?
100   ?  ?


This function should return a 5 by 2 numpy array with 10 floats.

Note: do not return a DataFrame, just the values denoted by '?' above in a numpy array. You might need to reshape your raw result to meet the format we are looking for.
'''
def answer_six():
    params = {'penalty':['l1','l2'],
              'C':[0.01, 0.1, 1.0, 10, 100]}
    
    grid = GridSearchCV(LogisticRegression(solver = 'liblinear'),
                        param_grid = params,
                        scoring = 'recall',
                        cv = 3)
    
    grid.fit(X_train, y_train)
    result = np.array(grid.cv_results_['mean_test_score'])
    
    return result.reshape(5,2)
