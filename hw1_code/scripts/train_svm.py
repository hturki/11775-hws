#!/bin/python 

import numpy
import os
from sklearn.svm.classes import SVC
import cPickle
import sys
from sklearn.model_selection import GridSearchCV

# Performs K-means clustering and save the model to a local file

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print "Usage: {0} event_name feat_dir output_file".format(sys.argv[0])
        print "event_name -- name of the event (P001, P002 or P003 in Homework 1)"
        print "feat_dir -- dir of feature files"
        print "output_file -- path to save the svm model"
        print "suffix -- suffix of feature files"
        exit(1)

    event_name = sys.argv[1]
    feat_dir = sys.argv[2]
    output_file = sys.argv[3]
    suffix = sys.argv[4]

    positives = []
    negatives = []
    with open("list/train", "r") as f:
        for line in f.readlines():
            split = line.split(" ")
            feature_file = feat_dir + split[0].strip() + "." + suffix
            if not os.path.exists(feature_file):
                continue
            if split[1].strip() == event_name:
                positives.append(numpy.genfromtxt(feature_file, delimiter=";"))
            else:
                negatives.append(numpy.genfromtxt(feature_file, delimiter=";"))

    num_per_label = min(len(positives), len(negatives))


    Cs = [0.001, 0.01, 0.1, 1, 10, 100, 1000]
    gammas = [0.001, 0.01, 0.1, 1, 10, 100, 1000]

    param_grid = [
        {'C': Cs, 'kernel': ['linear']},
        {'C': Cs, 'gamma': gammas, 'kernel': ['rbf']},
        {'kernel': ['sigmoid']}
    ]

    grid_search = GridSearchCV(SVC(probability=True), param_grid, n_jobs=-1, verbose=10)
    grid_search.fit(positives[:num_per_label] + negatives[:num_per_label], [1] * num_per_label + [0] * num_per_label)
    print "Best params: %s" % grid_search.best_params_

    with open(output_file, "wb") as f:
        cPickle.dump(grid_search.best_estimator_, f)

    print 'SVM trained successfully for event %s!' % (event_name)
