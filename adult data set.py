# -*- coding: utf-8 -*-
"""ADULT DATA SET.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1keSVhRFnrkVcSKK0J1qNDmMga-xj5AZZ

#Import modules
"""

import pandas as pd
import numpy as np
import sklearn as sk
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import pickle

import pickle
from sklearn.metrics import roc_curve, auc
from matplotlib import rcParams
from sklearn import metrics
from statsmodels.graphics.mosaicplot import mosaic
from sklearn.impute import SimpleImputer
from sklearn.neighbors import (KNeighborsClassifier, NeighborhoodComponentsAnalysis)
from sklearn.metrics import auc, confusion_matrix, plot_confusion_matrix, classification_report, roc_curve, roc_auc_score
from sklearn.preprocessing import OneHotEncoder as SklearnOneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV, KFold
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression as SklearnLinearRegression, LogisticRegression, RidgeClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.compose import ColumnTransformer

from sklearn.model_selection import train_test_split 
from sklearn.metrics import confusion_matrix
from sklearn.cluster import KMeans
from sklearn.metrics import classification_report

# Commented out IPython magic to ensure Python compatibility.
# #i hate auto-scrolling. so i disable it
# 
# %%javascript
# IPython.OutputArea.prototype._should_scroll = function(lines) {
#     return false;
# }

"""# Extract and view data"""

heading =['age', 'workclass', 'fnlwgt', 'education', 'education-num','marital-status', 'occupation', 'relationship', 'race', 'sex', 'capital-gain', 'capital-loss', 'hours-per-week', 'native-country','income']
df = pd.read_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data', header = None, names = heading)

df.head(10)

#income this is the last feature so the output has already been included okay so this makes it supervised machine learning

df.info()

# let us just see the shape of this data set so we will see the shape and we see that there are 32 561 rows and 15 columns

print(df.shape)

#that means how many i want to find out the the is null total number of zero or null entries now this is showing me that there are no null values in either of the features

df.apply(lambda x:sum(x.isnull()))

# Now i will return a scalar value which is the count of all the unique values in the Index.

df.nunique()

#Pandas describe() is used to view some basic statistical details
# .T just for visualisation

df.describe().T

"""#Value count function"""

# Now with  value_counts() function we will return object containing counts of unique values.

df['workclass'].value_counts()

df.columns

df['occupation'].value_counts()

df['native-country'].value_counts()

df['marital-status'].value_counts()

df['sex'].value_counts()

df['race'].value_counts()

df['income'].value_counts()

#Seaborn literally counts the number of observations per category for a categorical variable, and displays the results as a bar chart and countplot creating horizontal plot

sns.countplot(df['income'], palette='cool', hue='relationship', data=df);

df['education'].value_counts()

print(len(df.corr().columns))

#also i want to see something regarding correlation
#and we see that the figure that there is no as such high positive correlation

df.corr(method='pearson', min_periods=1)

df['age']



"""#Finding the outliers if any? BoxPlot"""

df.boxplot(column='age')

df.boxplot(column='fnlwgt')

df.boxplot(column='education-num')

df.boxplot(column='capital-gain')

df.boxplot(column='capital-loss')

df.boxplot(column='hours-per-week')

"""#Data Visualisation"""

px.pie(df, values='education-num', names='education', 
      color_discrete_sequence = px.colors.qualitative.T10)

from collections import Counter

#AGE HISTOGRAM

attr = 0
attribute = pd.Series(df.iloc[:,attr].values )
fig = plt.figure()
distinct = set(df.iloc[:,attr].values)
attribute.plot.hist(bins=int(len(distinct)/2), rwidth=0.9,
                   color='g')
plt.title('Attribute {}: {}'.format(attr+1, heading[attr]))
plt.xlabel('{}'.format(heading[attr]))
plt.ylabel('Count')
plt.show()

#WORKCLASS HISTOGRAM

attr = 1
freqs = Counter(df.iloc[:,attr].values)
fig = plt.figure()
xvals = range(len(freqs.values()))
plt.bar(xvals, freqs.values() , color='g')
plt.xticks(xvals, freqs.keys(),rotation='vertical')
plt.title('Attribute {}: {}'.format(attr+1, heading[attr]))
plt.xlabel('{}'.format(heading[attr]))
plt.ylabel('Count')
plt.show()

#FNLWGT HISTOGRAM

attr = 2
attribute = pd.Series(df.iloc[:,attr].values )
fig = plt.figure()
attribute.plot.hist(bins=15, rwidth=0.9,
                   color='g')
plt.xticks(rotation='vertical')
plt.title('Attribute {}: {}'.format(attr+1, heading[attr]))
plt.xlabel('{}'.format(heading[attr]))
plt.ylabel('Count')
plt.show()

#EDUCATION HISTOGRAM

attr = 3
freqs = Counter(df.iloc[:,attr].values)
sort_vals = [freqs[key] for key in sorted(freqs.keys())]
fig = plt.figure()
xvals = range(len(freqs.values()))
plt.bar(xvals, sort_vals, color='g')
plt.xticks(xvals, sorted(freqs.keys()),rotation='vertical')
plt.title('Attribute {}: {}'.format(attr+1, heading[attr]))
plt.xlabel('{}'.format(heading[attr]))
plt.ylabel('Count')
plt.show()

above_50 = df.loc[df["income"].values == " >50K"]
freqs = Counter(above_50.iloc[:,attr].values)
sort_vals = [freqs[key] for key in sorted(freqs.keys())]
fig = plt.figure()
xvals = range(len(freqs.values()))
plt.bar(xvals, sort_vals, color='g')
plt.xticks(xvals,sorted(freqs.keys()),rotation='vertical')
plt.title('Attribute {}: {} Above 50K'.format(attr+1, heading[attr]))
plt.xlabel('{}'.format(heading[attr]))
plt.ylabel('Count')
plt.show()

below_50 = df.loc[df["income"].values == " <=50K"]
freqs = Counter(below_50.iloc[:,attr].values)
sort_vals = [freqs[key] for key in sorted(freqs.keys())]
fig = plt.figure()
xvals = range(len(freqs.values()))
plt.bar(xvals, sort_vals, color='g')
plt.xticks(xvals, sorted(freqs.keys()),rotation='vertical')
plt.title('Attribute {}: {} Below 50K'.format(attr+1, heading[attr]))
plt.xlabel('{}'.format(heading[attr]))
plt.ylabel('Count')
plt.show()

#EDUCATION-NUM HISTOGRAM

attr = 4
attribute = pd.Series(df.iloc[:,attr].values )
fig = plt.figure()
distinct = set(df.iloc[:,attr].values)
attribute.plot.hist(bins=len(distinct), rwidth=0.9,
                   color='g')
#plt.xticks(rotation='vertical')
plt.title('Attribute {}: {}'.format(attr+1, heading[attr]))
plt.xlabel('{}'.format(heading[attr]))
plt.ylabel('Count')
plt.show()

#MARITAL-STATUS HISTOGRAM

attr = 5
freqs = Counter(df.iloc[:,attr].values)
fig = plt.figure()
xvals = range(len(freqs.values()))
plt.bar(xvals, freqs.values() , color='g')
plt.xticks(xvals, freqs.keys(),rotation='vertical')
plt.title('Attribute {}: {}'.format(attr+1, heading[attr]))
plt.xlabel('{}'.format(heading[attr]))
plt.ylabel('Count')
plt.show()

#OCCUPATION HISTOGRAM

attr = 6
freqs = Counter(df.iloc[:,attr].values)
fig = plt.figure()
xvals = range(len(freqs.values()))
plt.bar(xvals, freqs.values() , color='g')
plt.xticks(xvals, freqs.keys(),rotation='vertical')
plt.title('Attribute {}: {}'.format(attr+1, heading[attr]))
plt.xlabel('{}'.format(heading[attr]))
plt.ylabel('Count')
plt.show()

#RELATIONSHIP HISTOGRAM

attr = 7
freqs = Counter(df.iloc[:,attr].values)
sort_vals = [freqs[key] for key in sorted(freqs.keys())]
fig = plt.figure()
xvals = range(len(freqs.values()))
plt.bar(xvals, sort_vals , color='g')
plt.xticks(xvals, sorted(freqs.keys()),rotation='vertical')
plt.title('Attribute {}: {}'.format(attr+1, heading[attr]))
plt.xlabel('{}'.format(heading[attr]))
plt.ylabel('Count')
plt.show()


above_50 = df.loc[df["income"].values == " >50K"]
freqs = Counter(above_50.iloc[:,attr].values)
sort_vals = [freqs[key] for key in sorted(freqs.keys())]
fig = plt.figure()
xvals = range(len(freqs.values()))
plt.bar(xvals, sort_vals, color='g')
plt.xticks(xvals,sorted(freqs.keys()),rotation='vertical')
plt.title('Attribute {}: {} Above 50K'.format(attr+1, heading[attr]))
plt.xlabel('{}'.format(heading[attr]))
plt.ylabel('Count')
plt.show()


below_50 = df.loc[df["income"].values == " <=50K"]
freqs = Counter(below_50.iloc[:,attr].values)
sort_vals = [freqs[key] for key in sorted(freqs.keys())]
fig = plt.figure()
xvals = range(len(freqs.values()))
plt.bar(xvals, sort_vals, color='g')
plt.xticks(xvals, sorted(freqs.keys()),rotation='vertical')
plt.title('Attribute {}: {} Below 50K'.format(attr+1, heading[attr]))
plt.xlabel('{}'.format(heading[attr]))
plt.ylabel('Count')
plt.show()

#RACE HISTOGRAM
attr = 8
freqs = Counter(df.iloc[:,attr].values)
fig = plt.figure()
xvals = range(len(freqs.values()))
plt.bar(xvals, freqs.values() , color='g')
plt.xticks(xvals, freqs.keys(),rotation='vertical')
plt.title('Attribute {}: {}'.format(attr+1, heading[attr]))
plt.xlabel('{}'.format(heading[attr]))
plt.ylabel('Count')
plt.show()

#SEX HISTOGRAM

attr = 9
freqs = Counter(df.iloc[:,attr].values)
sort_vals = [freqs[key] for key in sorted(freqs.keys())]
fig = plt.figure()
xvals = range(len(freqs.values()))
plt.bar(xvals, sort_vals , color='g')
plt.xticks(xvals, sorted(freqs.keys()),rotation='vertical')
plt.title('Attribute {}: {}'.format(attr+1, heading[attr]))
plt.xlabel('{}'.format(heading[attr]))
plt.ylabel('Count')
plt.show()

above_50 = df.loc[df["income"].values == " >50K"]
freqs = Counter(above_50.iloc[:,attr].values)
sort_vals = [freqs[key] for key in sorted(freqs.keys())]
fig = plt.figure()
xvals = range(len(freqs.values()))
plt.bar(xvals, sort_vals, color='g')
plt.xticks(xvals,sorted(freqs.keys()),rotation='vertical')
plt.title('Attribute {}: {} Above 50K'.format(attr+1, heading[attr]))
plt.xlabel('{}'.format(heading[attr]))
plt.ylabel('Count')
plt.show()


below_50 = df.loc[df["income"].values == " <=50K"]
freqs = Counter(below_50.iloc[:,attr].values)
sort_vals = [freqs[key] for key in sorted(freqs.keys())]
fig = plt.figure()
xvals = range(len(freqs.values()))
plt.bar(xvals, sort_vals, color='g')
plt.xticks(xvals, sorted(freqs.keys()),rotation='vertical')
plt.title('Attribute {}: {} Below 50K'.format(attr+1, heading[attr]))
plt.xlabel('{}'.format(heading[attr]))
plt.ylabel('Count')
plt.show()

#CAPITAL-GAIN HISTOGRAM

attr = 10
attribute = pd.Series(df.iloc[:,attr].values )
fig = plt.figure()
attribute.plot.hist(bins=25, rwidth=0.9,
                   color='g')
plt.xticks(rotation='vertical')
plt.title('Attribute {}: {}'.format(attr+1, heading[attr]))
plt.xlabel('{}'.format(heading[attr]))
plt.ylabel('Count')
plt.show()

#CAPTIAL-LOSS HISTOGRAM

attr = 11
attribute = pd.Series(df.iloc[:,attr].values )
fig = plt.figure()
attribute.plot.hist(bins=25, rwidth=0.9,
                   color='g')
plt.xticks(rotation='vertical')
plt.title('Attribute {}: {}'.format(attr+1, heading[attr]))
plt.xlabel('{}'.format(heading[attr]))
plt.ylabel('Count')
plt.show()

#HOURS-PER-WEEK HISTOGRAM

attr = 12
attribute = pd.Series(df.iloc[:,attr].values )
fig = plt.figure()
attribute.plot.hist(bins=20, rwidth=0.9,
                   color='g')

plt.xticks(rotation='vertical')
plt.title('Attribute {}: {}'.format(attr+1, heading[attr]))
plt.xlabel('{}'.format(heading[attr]))
plt.ylabel('Count')
plt.show()

#NATIVE-COUNTRY HISTOGRAM

attr = 13
freqs = Counter(df.iloc[:,attr].values)
xvals = range(len(freqs.values()))
fig = plt.figure(figsize=(18, 5))
plt.bar(xvals, freqs.values(), color='g')
plt.xticks(xvals, freqs.keys(),rotation='vertical')
plt.title('Attribute {}: {}'.format(attr+1, heading[attr]))
plt.xlabel('{}'.format(heading[attr]))
plt.ylabel('Count')
plt.show()

"""# Data Pre-processing

0 when INCOME <=50K

1 when INCOME >50
"""

heading =['age', 'workclass', 'fnlwgt', 'education', 'education-num','marital-status', 'occupation', 'relationship', 'race', 'sex', 'capital-gain', 'capital-loss', 'hours-per-week', 'native-country','income']
df = pd.read_csv("https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data", header=None, names = heading, na_values="?", skipinitialspace = True)

df['target'] = df['income']
df['target'] = np.where(df['income'].isin(['>50K']), 1, 0)

#Correlation matrix to identify their relation with income.

plt.subplots(figsize=(10, 10))
sns.heatmap(df.corr(), vmax=.9, square=True, annot=True, fmt='.1f', center=0)
plt.show()

#I will drop FNLWGT beacuse has 0 corelation to target value

df = df.drop(['fnlwgt'], axis=1)

#I will drop education, beacuse Education and Education Number are the same

df.drop(['education'], axis = 1, inplace = True)

target = 'target'
num_features = ['age', 'capital-gain', 'capital-loss', 'hours-per-week', 'education-num']
cat_features = ['workclass', 'marital-status', 'occupation', 'relationship', 'race', 'sex', 'native-country']
features = df.columns.tolist()
features.remove(target)
X = df[features]
y = df[target]

def drawRocCurve(classifier, nameClassifier, X_test, y_test):
    # generate a no skill prediction (majority class)
    ns_probs = [0 for _ in range(len(y_test))]
    # predict probabilities
    lr_probs = classifier.predict_proba(X_test)
    # keep probabilities for the positive outcome only
    lr_probs = lr_probs[:, 1]
    # calculate scores
    ns_auc = roc_auc_score(y_test, ns_probs)
    lr_auc = roc_auc_score(y_test, lr_probs)
    # summarize scores
    print('Random model: ROC AUC=%.3f' % (ns_auc))
    print(f'{nameClassifier}: ROC AUC=%.3f' % (lr_auc))
    # calculate roc curves
    ns_fpr, ns_tpr, _ = roc_curve(y_test, ns_probs)
    lr_fpr, lr_tpr, _ = roc_curve(y_test, lr_probs)
    # plot the roc curve for the model
    plt.plot(ns_fpr, ns_tpr, linestyle='--', label='Random model')
    plt.plot(lr_fpr, lr_tpr, marker='.', label=nameClassifier)
    # axis labels
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    # show the legend
    plt.legend()
    # show the plot
    plt.show()
    return lr_auc, lr_fpr, lr_tpr

def GridSearch(param, estimator, X=X, y=y):
    '''GridSearch function split the data for training and test sets; fit data 
    for a given model and choose the best paramethers using GridSearchCV from sklearn.
    At the end this function return score raport for the prediction'''
    # split into a training and testing set
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

    grid_rf = GridSearchCV(estimator, param, refit = True, verbose = 3, n_jobs=-1) 

    # fitting the model for grid search 
    grid_rf.fit(X_train, y_train) 

    # print best parameter after tuning 
    print(grid_rf.best_params_) 
    grid_rf_predictions = grid_rf.predict(X_test) 

    # print classification report 
    return classification_report(y_test, grid_rf_predictions)

def ConfusionMatrix(classifier, X=X, y=y, confusionMatrix = True, plotConfusionMatrix = True):
        '''ConfusionMatrix function split data, fit data to model and give 
        a prediction for a given model and data. After that draw Confusion Matrix or 
        Plot Confusion Matrix to show the score'''
        #computing the confusion matrix with each row corresponding to the true class
        if(confusionMatrix):
            print(confusion_matrix(y_test, y_pred))

        #drawing Plot Confusion Matrix
        if(plotConfusionMatrix):
            plot_confusion_matrix(classifier, X_test, y_test)  
            plt.show()

def featuresToOther(column, dataframe = df, percent=0.05, name_for_other="Other"):
    
    '''This function change features under given threshold to one group. 
    The group is called by name_for_other, default- Other'''
    
    frame = dataframe[column].value_counts().to_frame()
    values =  dataframe[column].value_counts().index.tolist()
    sum_of_count = 0
    for n in range(len(frame.index)): 
        sum_of_count += frame.iloc[n]
    threshold = sum_of_count.iloc[0]*percent
    list_values_to_change= []
    for i in range(len(frame.index)):
        num = frame.iloc[i, 0]
        if(num < threshold):
            list_values_to_change.append(values[i])
    dataframe[column].replace(list_values_to_change, name_for_other, inplace = True)

insignificant_values = ['workclass', 'occupation', 'race', 'native-country']
for value in insignificant_values:
    featuresToOther(column=value, dataframe=df, percent=0.04)

target = 'target'
num_features = ['age', 'capital-gain', 'capital-loss', 'hours-per-week', 'education-num']
cat_features = ['workclass', 'marital-status', 'occupation', 'relationship', 'race', 'sex', 'native-country']
features = df.columns.tolist()
features.remove(target)
X = df[features]
y = df[target]

numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='Other')),
    ('onehot', SklearnOneHotEncoder())])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, num_features),
        ('cat', categorical_transformer, cat_features)])

"""#Classification

##Decision Tree Classifier
"""

clf = Pipeline(steps=[('preprocessor', preprocessor),
                      ('classifier',  DecisionTreeClassifier())])
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

clf.fit(X_train, y_train)
print("model score: %.3f" % clf.score(X_test, y_test))

ConfusionMatrix(classifier=clf, confusionMatrix=False)

lr_auc_tree, lr_fpr_tree, lr_tpr_tree = drawRocCurve(clf, "Decision Tree Classifier", X_test, y_test)

"""##Random Forest Classifier"""

clf = Pipeline(steps=[('preprocessor', preprocessor),
                      ('classifier',  RandomForestClassifier())])
param = {'classifier__max_depth': [2, 20],
         'classifier__n_estimators': [100, 500],
         'classifier__max_features': [10 , 20]}
gs = GridSearchCV(clf, param)
gs.fit(X_train, y_train)
best_params = gs.best_params_
print(best_params)
ConfusionMatrix(classifier=gs, confusionMatrix=False)

clf = Pipeline(steps=[('preprocessor', preprocessor),
                      ('classifier',  RandomForestClassifier())])
param = {'classifier__max_depth': [20, 50],
         'classifier__max_features': [10, 30],
         'classifier__min_samples_split': [10, 30]}
gs = GridSearchCV(clf, param)
gs.fit(X_train, y_train)
best_params = gs.best_params_
print(best_params)
ConfusionMatrix(classifier=gs, confusionMatrix=False)

clf = Pipeline(steps=[('preprocessor', preprocessor),
                      ('classifier',  RandomForestClassifier(max_depth =  20,max_features =  10,
                                                             min_samples_split =  30,
                                                             n_estimators =  500))])
clf.fit(X_train, y_train)
clf.predict(X_test)
ConfusionMatrix(classifier=clf, confusionMatrix=False)

lr_auc_rf, lr_fpr_rf, lr_tpr_rf = drawRocCurve(clf, "Random Forest Classifier", X_test, y_test)

"""##Linear Regression Classifier"""

clf = Pipeline(steps=[('preprocessor', preprocessor),
                      ('classifier',  RidgeClassifier())])
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

clf.fit(X_train, y_train)
print("model score: %.3f" % clf.score(X_test, y_test))
ConfusionMatrix(classifier=clf, confusionMatrix=False)

nameClassifier = "Linear Regression Classifier"
# generate a no skill prediction (majority class)
ns_probs = [0 for _ in range(len(y_test))]
# predict probabilities
lr_probs = clf.predict(X_test)
# keep probabilities for the positive outcome only
lr_probs = lr_probs
# calculate scores
ns_auc = roc_auc_score(y_test, ns_probs)
lr_auc = roc_auc_score(y_test, lr_probs)
# summarize scores
print('Random model: ROC AUC=%.3f' % (ns_auc))
print(f'{nameClassifier}: ROC AUC=%.3f' % (lr_auc))
# calculate roc curves
ns_fpr, ns_tpr, _ = roc_curve(y_test, ns_probs)
lr_fpr, lr_tpr, _ = roc_curve(y_test, lr_probs)
# plot the roc curve for the model
plt.plot(ns_fpr, ns_tpr, linestyle='--', label='Random model')
plt.plot(lr_fpr, lr_tpr, marker='.', label=nameClassifier)
# axis labels
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
# show the legend
plt.legend()
# show the plot
plt.show()
lr_auc_rc, lr_fpr_rc, lr_tpr_rc = lr_auc, lr_fpr, lr_tpr

"""##Logistic Regerssion Classifier"""

clf = Pipeline(steps=[('preprocessor', preprocessor),
                      ('classifier',  LogisticRegression())])
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

clf.fit(X_train, y_train)
print("model score: %.3f" % clf.score(X_test, y_test))
ConfusionMatrix(classifier=clf, confusionMatrix=False)

lr_auc_logr, lr_fpr_logr, lr_tpr_logr = drawRocCurve(clf, "Logistic Regression", X_test, y_test)

"""##k-Nearest Neighbours Classifier"""

clf = Pipeline(steps=[('preprocessor', preprocessor),
                      ('knn',  KNeighborsClassifier())])
param = {'knn__n_neighbors': [10, 100],
         'knn__weights': ['uniform', 'distance'],
         'knn__p': [1, 2]}
gs = GridSearchCV(clf, param)
gs.fit(X_train, y_train)
best_params = gs.best_params_
print(best_params)
ConfusionMatrix(classifier=gs, confusionMatrix=False)

clf = Pipeline(steps=[('preprocessor', preprocessor),
                      ('knn',  KNeighborsClassifier())])
param = {'knn__n_neighbors': [100, 500],
         'knn__weights': ['uniform'],
         'knn__p': [1]}
gs = GridSearchCV(clf, param)
gs.fit(X_train, y_train)
best_params = gs.best_params_
print(best_params)
ConfusionMatrix(classifier=gs, confusionMatrix=False)

clf = Pipeline(steps=[('preprocessor', preprocessor),
                      ('knn',  KNeighborsClassifier(n_neighbors=10, p=1, weights='uniform'))])
clf.fit(X_train, y_train)
clf.predict(X_test)
ConfusionMatrix(classifier=clf, confusionMatrix=False)

lr_auc_knn, lr_fpr_knn, lr_tpr_knn = drawRocCurve(clf, "K-Neighbors Classifier", X_test, y_test)

clf = Pipeline(steps=[('preprocessor', preprocessor),
                      ('svc',  SVC())])
param = {'svc__C': [1, 10],
         'svc__kernel': ['linear', 'poly']}
gs = GridSearchCV(clf, param)
gs.fit(X_train, y_train)
best_params = gs.best_params_
print(best_params)
ConfusionMatrix(classifier=gs, confusionMatrix=False)

clf = Pipeline(steps=[('preprocessor', preprocessor),
                      ('svc',  SVC())])
param = {'svc__kernel': ['poly', 'rbf'],
         'svc__gamma': ['scale', 'auto']
        }
gs = GridSearchCV(clf, param)
gs.fit(X_train, y_train)
best_params = gs.best_params_
print(best_params)
ConfusionMatrix(classifier=gs, confusionMatrix=False)

clf = Pipeline(steps=[('preprocessor', preprocessor),
                      ('svc',  SVC(C = 1, kernel = "rbf", gamma = "scale", probability=True))])
clf.fit(X_train, y_train)
clf.predict(X_test)
ConfusionMatrix(classifier=clf, confusionMatrix=False)

lr_auc_svm, lr_fpr_svm, lr_tpr_svm = drawRocCurve(clf, "SVC", X_test, y_test)

"""## Compare Classifiers"""

# Determining the size of the drawing
fig, ax = plt.subplots(figsize=(10,10))
ax.set_facecolor((0,0,0.10))

#about Random model
ns_probs = [0 for _ in range(len(y_test))]
ns_auc = roc_auc_score(y_test, ns_probs)
ns_fpr, ns_tpr, _ = roc_curve(y_test, ns_probs)

# plot the roc curve for the model
plt.plot(ns_fpr, ns_tpr, linestyle='--')
plt.plot(lr_fpr_tree, lr_tpr_tree, label="Decision Tree, %.3f" % (lr_auc_tree))
plt.plot(lr_fpr_rf, lr_tpr_rf,  label="Random Forest, %.3f" % (lr_auc_rf))
plt.plot(lr_fpr_rc, lr_tpr_rc,  label="Ridge Classifier, %.3f" % (lr_auc_rc))
plt.plot(lr_fpr_logr, lr_tpr_logr, label="Logistic Regression, %.3f" % (lr_auc_logr))
plt.plot(lr_fpr_knn, lr_tpr_knn, label="K-Nearest Neighbours, %.3f" % (lr_auc_knn))
plt.plot(lr_fpr_svm, lr_tpr_svm,  label="Support Vector Machine, %.3f" % (lr_auc_svm))

plt.plot([0, 1], [0, 1], linestyle='--', lw=2)
# axis labels
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
# show the legend
plt.legend()
# show the plot
plt.show()

# Best score has Random Forest - 0,916



"""#Clustering

##K-Means Clustering
"""

heading =['age', 'workclass', 'fnlwgt', 'education', 'education-num','marital-status', 'occupation', 'relationship', 'race', 'sex', 'capital-gain', 'capital-loss', 'hours-per-week', 'native-country','income']
df = pd.read_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data', header = None, names = heading)

#Determine “k” value from the elbow method

# iterate over all the attributes(columns) from the dataset
for attribute in df.columns:
    # check if the datatype of the attribute is an object
    if df.dtypes[attribute] == np.object:
        # use factorize function to represent string values as numeric values
        df[attribute], _ = pd.factorize(df[attribute])
        
# min max normalization
df = (df-df.min())/(df.max()-df.min())

# variable X contains all the attributes except 'Class'
X = df.iloc[:,0:14]   

# variable Y contains the target 'Class'
Y = df.iloc[:,14:15]

# create empty list to store the sum of squared error 
sse = []

# iterate from 1 to 10 clusters
for k in range(1, 11):
    # set kmeans for the kth number of clusters
    model = KMeans(n_clusters = k)
    # pass the data to the kmeans model
    model.fit(X)
    # store the sum of squared error in sse
    sse.append(model.inertia_)
    
print('\nAccording to the graph, we can see that the elbow starts at 2. Therefore, 2 is the optimal number of clusters.')
    
# plot the graph
plt.plot(range(1, 11), sse)
plt.xlabel('Number of clusters')
plt.ylabel('Sum of squared errors (SSE)')
plt.title('The Elbow Method');

#Visualization for K-Means Clustering

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.3, random_state = 0)

# Import PCA
from sklearn.decomposition import PCA

# set to 2 dimensions
pca = PCA(n_components = 2)

# Create the KMeans model

# set 2 clusters for kmeans model
model = KMeans(n_clusters = 2)

# pass the training data to the kmeans model
model.fit(X_train)

# Compute cluster centers and predict cluster index for each sample 

# compute cluster centers
print('Cluster Centers:')
print(model.cluster_centers_)

# predict training data
train_pred = model.predict(X_train)

# Model and fit the data to the PCA model
X_train_pca = pca.fit_transform(X_train)

# Visualize the predicted training labels vs actual training labels. 
x = X_train_pca[:, 0]
y = X_train_pca[:, 1]

plt.figure(figsize=(10, 10))

# scatter plot for actual training labels
plt.subplot(211)
plt.title('Actual Training Labels')
sns.scatterplot(x = x, y = y, hue = Y_train.income)

# scatter plot for predicted training labels
plt.subplot(212)
plt.title('Predicted Training Labels')
sns.scatterplot(x = x, y = y, hue = train_pred);

#Visualizing the predicted testing labels versus actual testing labels. Use the trained model in previous step.

# predict cluster index for each sample 

# predict testing data
test_pred = model.predict(X_test)

# Model and fit the data to the PCA model
X_test_pca = pca.fit_transform(X_test)

# Visualize the predicted testing labels vs actual testing labels. 
x = X_test_pca[:, 0]
y = X_test_pca[:, 1]

plt.figure(figsize=(10, 10))

# scatter plot for actual testing labels
plt.subplot(211)
plt.title('Actual Testing Labels')
sns.scatterplot(x = x, y = y, hue = Y_test.income)

# scatter plot for predicted testing labels
plt.subplot(212)
plt.title('Predicted Testing Labels')
sns.scatterplot(x = x, y = y, hue = test_pred);

#Evaluation of your clustering model and printing confusion matrix.

# print the confusion matrix for predicted training labels and actual training labels
print('confusion matrix (training dataset):')
print(confusion_matrix(Y_train, train_pred))

# print the confusion matrix for predicted testing labels and actual testing labels
print('\nconfusion matrix (testing dataset):')
print(confusion_matrix(Y_test, test_pred))

"""##Hierarchical Agglomerative Clustering"""

#Find the best Hierarchical Agglomerative Clustering Model

# Import AgglomerativeClustering
from sklearn.cluster import AgglomerativeClustering
# Import pairwise_distances for calculating pairwise distance matrix
from sklearn.metrics.pairwise import pairwise_distances
# Import f1_score
from sklearn.metrics import f1_score

## Calculate pairwise distance matrix for X_train
# https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise_distances.html
pdm_train = pairwise_distances(X_train, metric='euclidean')
print('Pairwise Distance Matrix:')
#np.set_printoptions(threshold=np.inf)
print(np.matrix(pdm_train))

## Model and fit the training data to the AgglomerativeClustering model
# https://scikit-learn.org/stable/modules/generated/sklearn.cluster.AgglomerativeClustering.html
## complete linkage + cosine
complete_cos = AgglomerativeClustering(n_clusters=2, affinity='cosine', linkage='complete')
complete_cos_pred = complete_cos.fit_predict(X_train)
complete_cos_f1 = f1_score(Y_train, complete_cos_pred, average='macro')
print("Confusion Matrix for complete linkage + cosine:")
print(confusion_matrix(Y_train,complete_cos_pred))

## Model and fit the training data to the AgglomerativeClustering model
## complete linkage + euclidean
complete_euc = AgglomerativeClustering(n_clusters=2, affinity='euclidean', linkage='complete').fit(X)
complete_euc_pred = complete_euc.fit_predict(X_train)
complete_euc_f1 = f1_score(Y_train, complete_euc_pred, average='macro')
print("Confusion Matrix for complete linkage + euclidean:")
print(confusion_matrix(Y_train,complete_euc_pred))

## Model and fit the training data to the AgglomerativeClustering model
## complete linkage + manhattan
complete_man = AgglomerativeClustering(n_clusters=2, affinity='manhattan', linkage='complete').fit(X)
complete_man_pred = complete_man.fit_predict(X_train)
complete_man_f1 = f1_score(Y_train, complete_man_pred, average='macro')
print("Confusion Matrix for complete linkage + manhattan:")
print(confusion_matrix(Y_train,complete_man_pred))

## Model and fit the training data to the AgglomerativeClustering model
## average linkage + cosine
average_cos = AgglomerativeClustering(n_clusters=2, affinity='cosine', linkage='average').fit(X)
average_cos_pred = average_cos.fit_predict(X_train)
average_cos_f1 = f1_score(Y_train, average_cos_pred, average='macro')
print("Confusion Matrix for average linkage + cosine:")
print(confusion_matrix(Y_train,average_cos_pred))

## Model and fit the training data to the AgglomerativeClustering model
## average linkage + euclidean
average_euc = AgglomerativeClustering(n_clusters=2, affinity='euclidean', linkage='average').fit(X)
average_euc_pred = average_euc.fit_predict(X_train)
average_euc_f1 = f1_score(Y_train, average_euc_pred, average='macro')
print("Confusion Matrix for average linkage + euclidean:")
print(confusion_matrix(Y_train,average_euc_pred))

## Model and fit the training data to the AgglomerativeClustering model
## average linkage + manhattan
average_man = AgglomerativeClustering(n_clusters=2, affinity='manhattan', linkage='average').fit(X)
average_man_pred = average_man.fit_predict(X_train)
average_man_f1 = f1_score(Y_train, average_man_pred, average='macro')
print("Confusion Matrix for average linkage + manhattan:")
print(confusion_matrix(Y_train,average_man_pred))

print("F1-score for complete linkage + cosine", complete_cos_f1)
print("F1-score for complete linkage + euclidean", complete_euc_f1)
print("F1-score for complete linkage + manhattan", complete_man_f1)
print("F1-score for average linkage + cosine", average_cos_f1)
print("F1-score for average linkage + euclidean", average_euc_f1)
print("F1-score for average linkage + manhattan", average_man_f1)

#Visualization for Hierarchical Agglomerative Clustering

from sklearn.decomposition import PCA

# Visualize the predicted training labels versus actual training labels. 
# The best performed model was average linkage + euclidean which is the one with highest f1-score which
# is  0.4310104676325485.

# Reducing the acttributes to 2 using Principa Component Analysis
pca = PCA(n_components = 2) 
X_pca = pca.fit_transform(X_train)
X_pca = pd.DataFrame(data = X_pca, columns = ['pc1', 'pc2'])

x = X_pca.iloc[:, 0]
y = X_pca.iloc[:, 1]
plt.figure(figsize=(12, 11))
# scatter plot for actual testing labels
plt.subplot(211)
plt.title('Agglomerative: Actual training Labels')
sns.scatterplot(x = x, y = y, hue = Y_train.income)

# scatter plot for predicted testing labels
plt.subplot(212)
plt.title('Agglomerative: Predicted training Labels')
sns.scatterplot(x = x, y = y, hue = average_euc_pred);

"""##Compare K-Means Clustering and Hierarchical Agglomerative Clustering"""

#Visualize Clusters

# Model and fit the data to the Kmeans (use fit_predict : Performs clustering on X and returns cluster labels.)
Model = KMeans(n_clusters = 2)
label_kmean = Model.fit_predict(X)

### Agglomerative Clustering
# Calculate pairwise distance matrix for X
pdm_train = pairwise_distances(X, metric='euclidean')
print('Pairwise Distance Matrix for X:')
print(np.matrix(pdm_train))

# Model and fit the data to the Agglomerative (use fit_predict : Performs clustering on X and returns cluster labels.)
average_euc = AgglomerativeClustering(n_clusters=2, affinity='euclidean', linkage='average').fit(X)
avg_euc_pred_X = average_euc.fit_predict(X)

# Visualize Clusters
#  Model and fit the data to the PCA model
X_pca = pca.fit_transform(X)

# Visualize the predicted Kmeans labels versus  the predicted Agglomerative labels versus Actual labels. 

# Visualize the predicted testing labels vs actual testing labels. 
### scatter(x, y, your_data)
x = X_pca[:, 0]
y = X_pca[:, 1]

plt.figure(figsize=(10, 10))

plt.subplot(211)
plt.title('Actual Labels')
sns.scatterplot(x = x, y = y, hue = Y.income)

plt.subplot(212)
plt.title('Predicted Kmeans Labels')
sns.scatterplot(x = x, y = y, hue = label_kmean)

plt.figure(figsize=(10, 10))
plt.subplot(211)
plt.title('Predicted Agglomerative Labels')
sns.scatterplot(x = x, y = y, hue = avg_euc_pred_X);

#Compare K-Means Clustering & Hierarchical Agglomerative Clustering

print("Agglomerative: Confusion Matrix for average linkage + euclidean:")
print(confusion_matrix(Y,avg_euc_pred_X))
print("K-Means: Confusion Matrix for 2 clusters:")
print(confusion_matrix(Y,label_kmean))

print('')
print('Agglomerative Classification Report:')
print(classification_report(Y, avg_euc_pred_X))
print('K-Means Classification Report:')
print(classification_report(Y, label_kmean))

"""#Apriori Frequent Pattern Mining (improved using Sampling)"""

# Importing required libraries
from itertools import combinations
import time

heading =['age', 'workclass', 'fnlwgt', 'education', 'education-num','marital-status', 'occupation', 'relationship', 'race', 'sex', 'capital-gain', 'capital-loss', 'hours-per-week', 'native-country','income']
df = pd.read_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data', names = heading)

df.head()

# Removing irrelevant columns

df.drop(['fnlwgt', 'education-num'], axis = 1, inplace = True)
df.head()

# Size of original data

df.shape

# Removing missing values from data
df.replace(' ?', np.NaN, inplace = True)
df.dropna(axis = 0, inplace = True)

# Size of data after removing missing values
df.shape

# Converting numeric data to categorical data
df['age'] = pd.cut(df['age'], [0, 25, 40, np.inf], labels=["young", "middle_aged", "old"])
df['capital-gain'] = pd.cut(df['capital-gain'], [-1, 1, np.inf], labels=["No_Gain", "Gain"])
df['capital-loss'] = pd.cut(df['capital-loss'], [-1, 1, np.inf], labels=["No_Loss", "Loss"])
df['hours-per-week'] = pd.cut(df['hours-per-week'], [-1, 5, 20, 60, np.inf], labels=["Less", "Medium", "Reasonable", "High"])
df.head()

# Generate a sampled dataset from the input data
def sampling(df, samplingFactor):
    sampledData = df.sample(frac = samplingFactor)
    return sampledData

# Generating Candidate 1
def C1(data):
    candidates = {} # empty dictionary to store each item as key and its count as value
    for i in data.index:
        for j in data.loc[i]:
            if (j in candidates): 
                candidates[j] += 1
            else: 
                candidates[j] = 1
    print("\nC1: \n", candidates)
    return candidates

# Generating L1
def L1(c, support):
    l1 = {} # dictionary to store all the items having support more than or equal to minimum support
    l1 = dict((k,v) for k, v in c.items() if v >= support)
    print("\n\nL1: \n", l1)
    return l1

# Function to check if candidate itemset contains infrequent subset
def has_infrequent_subset(candidate, freq, prevL):
    for i in list(combinations(candidate,freq-1)):
        if i not in prevL:
            return True
        return False

# Generating Candidate k
def Ck(k, prevL, df):
    
    # Join
    # For C2:
    if k == 2:
        c = list()
        for key,v in prevL.items():
            if key not in c:
                c.append(key)
            
    # When k is greater than 2, L (k-1) contains list of tuples
    if k > 2:
        c = list()
        for key,v in prevL.items():
            for item in key:
                if item not in c:
                    c.append(item)
                    
    candidates = {} # To store all the candidate items along with its count
    cand = list(combinations(c, k))
    
    # Prune
    for cd in cand:
        if (has_infrequent_subset(cd, k, prevL) == True):
            cand.remove(cd)
            
    for i in cand:
        candidates[i] = 0
    for ind in df.index:
        for i in candidates:
            if set(i).issubset(df.loc[ind]):
                candidates[i] +=1
                
    print("\n\nC", k, ":\n", candidates)
    return candidates

# Generating Lk
def Lk(k, ck, support):
    lk = {}
    # lk contains all the values having support more than minimum support threshold
    lk = dict((key,v) for key, v in ck.items() if v >= support)
    print("\n\nL", k, ":\n", lk)
    return lk

# Function for Apriori Algorithm
def apriori(data, support, samplingFactor):
    
    s = int((support/100)*0.9*len(data))
    df = sampling(data, samplingFactor)
    t1 = time.time()
    
    print("Minimum support = ", s)
    
    lk = {}
    candidateK = {}
    candidateK = C1(df)
    lk = L1(candidateK, s)
    
    k = 2
    while lk != {}:
        candidateK = Ck(k, lk, data)
        lk = Lk(k, candidateK, s)
        k += 1
    t2 = time.time()
    
    exec_time = t2 - t1
    
    print("\nTotal execution time = ", exec_time)

    return

apriori(df, 50, 0.6)

#Thank you!