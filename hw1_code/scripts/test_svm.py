#!/bin/python 

import numpy
import os
from sklearn.svm.classes import SVC
import cPickle
import sys

# Apply the SVM model to the testing videos; Output the score for each video

def write_predictions(list, output_file, suffix):
    global f, output, line, split, feature_file
    with open(list, "r") as f:
        with open(output_file, "w") as output:
            for line in f.readlines():
                split = line.split(" ")
                feature_file = feat_dir + split[0].strip() + "." + suffix
                if os.path.exists(feature_file):
                    prediction = cv.predict_proba([numpy.genfromtxt(feature_file, delimiter=";")])[0][1]
                else:
                    prediction = 0
                output.write(str(prediction) + "\n")


if __name__ == '__main__':
    if len(sys.argv) != 6:
        print "Usage: {0} model_file feat_dir feat_dim output_file".format(sys.argv[0])
        print "model_file -- path of the trained svm file"
        print "feat_dir -- dir of feature files"
        print "val_output_file -- path to save the prediction score for validation entries"
        print "output_file -- path to save the prediction score for test entries"
        print "suffix -- suffix of feature files"
        exit(1)

    model_file = sys.argv[1]
    feat_dir = sys.argv[2]
    val_output_file = sys.argv[3]
    output_file = sys.argv[4]
    suffix = sys.argv[5]

    cv = cPickle.load(open(model_file, "rb"))
    write_predictions("list/val", val_output_file, suffix)
    write_predictions("../all_test_fake.lst", output_file, suffix)

