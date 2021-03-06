#!/bin/python
import numpy
import os
import cPickle
from sklearn.cluster.k_means_ import KMeans
import sys
# Generate k-means features for videos; each video is represented by a single vector

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print "Usage: {0} kmeans_model, cluster_num, file_list".format(sys.argv[0])
        print "kmeans_model -- path to the kmeans model"
        print "cluster_num -- number of cluster"
        print "file_list -- the list of videos"
        exit(1)

    kmeans_model = sys.argv[1]
    file_list = sys.argv[3]
    cluster_num = int(sys.argv[2])

    # load the kmeans model
    kmeans = cPickle.load(open(kmeans_model, "rb"))
    with open(file_list, "r") as f:
        for line in f.readlines():
            mfcc_path = "mfcc/" + line.replace('\n', '') + ".mfcc.csv"
            if os.path.exists(mfcc_path) == False:
                continue
            array = numpy.genfromtxt(mfcc_path, delimiter=";")
            kmeans_vector = numpy.zeros(cluster_num)
            for cluster in kmeans.predict(array):
                kmeans_vector[cluster] += 1
            with open("kmeans/" + line.replace('\n', '') + ".kmeans", "w") as out:
                out.write(';'.join(map(lambda x: str(int(x)), kmeans_vector)))

    print "K-means features generated successfully!"
