# -*- coding: utf-8 -*- 
"""learn_iris.py
    Messing around with basic machine learning and data analysis tools using
    the UCI iris dataset.

    Author:
        Aaron Penne (based heavily on references)
        
    Resources:
        http://docs.python-guide.org/en/latest/scenarios/ml/
        https://machinelearningmastery.com/quick-and-dirty-data-analysis-with-pandas/
        http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html#example-google
        

"""


from sklearn.datasets import load_iris
from sklearn import tree
from sklearn.metrics import accuracy_score
import numpy as np
import pandas as pd
from pandas.plotting import scatter_matrix, andrews_curves, radviz
import matplotlib.pyplot as plt
import matplotlib
# import graphviz as gv

# %% Function definitions

def iris_fig(fig, title):
    """Prints figures using consistent parameters
    
    """
    # https://stackoverflow.com/a/16550348
    plt.savefig('Iris_'+title+'.png', bbox_inches='tight', dpi=300)  # https://stackoverflow.com/a/28293462
    plt.savefig('Iris_'+title+'.pdf', bbox_inches='tight')  # # http://www.pythonforbeginners.com/concatenation/string-concatenation-and-formatting-in-python

    

# %% Main starts

# Loads the iris toy dataset
iris = load_iris()

# Pulls out the struct into variables
x = iris.data
y = iris.target
y_names = iris.target_names


# %% Data Analysis
# https://machinelearningmastery.com/quick-and-dirty-data-analysis-with-pandas/

# Converts the iris dataset to a pandas dataframe
# https://stackoverflow.com/a/38105540
iris_pd = pd.DataFrame(data = np.c_[iris.data, iris.target], 
                       columns = ['sep_L', 'sep_W', 'pet_L', 'pet_W', 'tgt'])

# Summary statistics: count, mean, stdev, min, max
# http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.describe.html
print(iris_pd.describe())  # It's a one liner!

# Default styles are bad
matplotlib.style.use('ggplot')

title = 'Boxplot'
# https://pandas.pydata.org/pandas-docs/stable/visualization.html
fig = plt.figure()
iris_pd.boxplot()
# https://stackoverflow.com/a/24674675
iris_fig(fig, title)

title = 'Histograms_Dimensions'
# Histograms
fig = plt.figure()
iris_pd.hist()
iris_fig(fig, title)

title = 'Histograms_By_Class'
# Histograms by class
fig = plt.figure()
iris_pd.groupby('tgt').hist()
iris_fig(fig, title)

title = 'Histograms_By_Class_Single_Plot'
# Histograms by class on single plots
fig = plt.figure()
iris_pd.groupby('tgt').plot.hist(alpha=0.5)
iris_fig(fig, title)

# Histograms by class on single plots
#FIXME implement this by grouping by column and plot different colors for classes

title = 'Scatter_Matrix'
# Scatter plot matrix
# The fun one!
fig = plt.figure()
scatter_matrix(iris_pd, alpha=0.3, diagonal='kde')
iris_fig(fig, title)

title = 'Andrews_Curves'
# Very cool way to try to differentiate between classes. Some math is needed
# https://en.wikipedia.org/wiki/Andrews_plot
# http://sci-hub.cc/
fig = plt.figure()
andrews_curves(iris_pd, 'tgt')
iris_fig(fig, title)

title = 'Radviz'
# Springy area plots
fig = plt.figure()
radviz(iris_pd, 'tgt')
iris_fig(fig, title)

# %% Machine Learning - Classification Tree
# http://docs.python-guide.org/en/latest/scenarios/ml/

# Randomizes order of indices for splitting the data into train and test sets
ids = np.random.permutation(len(x))

# Gets n-10 data points for training
x_train = x[ids[:-10]]
y_train = y[ids[:-10]]

# Gets 10 data points for testing
x_test  = x[ids[-10:]]
y_test  = y[ids[-10:]]

# Initializes decision tree classifier
clf = tree.DecisionTreeClassifier(random_state=0, criterion="gini")

# Builds decision tree based on training data: fit(samples, targets)
clf.fit(x_train, y_train)

# Generates prediction based on test data, returning predicted classes
predictions = clf.predict(x_test)

# Prints results of classification
print("")
print(y_test, "<-- Truth")
print(predictions, "<-- Predictions")  # http://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html#sklearn.tree.DecisionTreeClassifier.predict


# Prints columns of truth vs. prediciton categories as strings
print("")
pad = len(max(y_names, key=len)) + 2  # https://stackoverflow.com/a/873333
print("Truth".ljust(pad), "Predictions".ljust(pad))  # https://docs.python.org/3/library/stdtypes.html#str.ljust
print("".ljust(pad, "-"), "".ljust(pad, "-"))
for ii in range(len(y_test)):
    truth = y_names[y_test[ii]]
    guess = y_names[predictions[ii]]
    print(truth.ljust(pad), guess.ljust(pad))

# Prints score of classification performance
print("")
print("Score: ", accuracy_score(predictions, y_test)*100, "%", sep='')

# Prints a pretty picture 
#FIXME need to print from within python code (install python-graphviz)
tree.export_graphviz(clf, out_file='iris_tree.dot')  # https://stackoverflow.com/a/5316277
# dot -Tpng iris_tree.dot -o iris_tree.png



