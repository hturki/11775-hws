#!/bin/python 

import numpy
import os
from sklearn.svm.classes import SVC
import cPickle
import sys


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print "Usage: {0} event_name list_file output_file".format(sys.argv[0])
        print "event_name -- event name"
        print "list_file -- file containing validation labels"
        print "output_file -- path to save the label file"
        exit(1)

    event_name = sys.argv[1]
    list_file = sys.argv[2]
    output_file = sys.argv[3]

    with open(list_file, "r") as f:
        with open(output_file, "w") as out:
            for line in f.readlines():
                split = line.split(" ")
                if split[1].strip() == event_name:
                    out.write('1\n')
                else:
                    out.write('0\n')
