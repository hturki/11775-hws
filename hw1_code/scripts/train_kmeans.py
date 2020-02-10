#!/bin/python 

import numpy
import os
from sklearn.cluster.k_means_ import KMeans
import cPickle
import sys
from joblib import parallel_backend

# Performs K-means clustering and save the model to a local file

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print "Usage: {0} input_file cluster_num output_file".format(sys.argv[0])
        print "input_file -- path to the mfcc file"
        print "cluster_num -- number of cluster"
        print "output_file -- path to save the k-means model"
        exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[3]
    cluster_num = int(sys.argv[2])

    if input_file.endswith(".csv"):
        array = numpy.genfromtxt(input_file, delimiter=";")
    else:
        array = None
        with open(input_file, "r") as f:
            for line in f.readlines():
                mfcc_path = "mfcc/" + line.replace('\n', '') + ".mfcc.csv"
                if os.path.exists(mfcc_path) == False:
                    continue
                file_values = numpy.genfromtxt(mfcc_path, delimiter=";")
                if array is None:
                    array = file_values
                else:
                    array = numpy.concatenate((array, file_values))
    with parallel_backend('threading', n_jobs=-1):
        k_means = KMeans(n_clusters=cluster_num, verbose=1).fit(array)

    with open(output_file, "wb") as f:
        cPickle.dump(k_means, f)

    print "K-means trained successfully!"
