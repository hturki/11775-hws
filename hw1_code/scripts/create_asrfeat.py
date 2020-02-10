#!/bin/python
import os
from sklearn.feature_extraction.text import TfidfVectorizer
import sys

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "Usage: {0} vocab_file, file_list".format(sys.argv[0])
        print "file_list -- the list of videos"
        print "asr_path -- folder containing asr files"
        exit(1)

    file_list = sys.argv[1]
    asr_path = sys.argv[2]

    vectorizer = TfidfVectorizer(input="filename")

    inputs = []
    outputs = []
    with open(file_list, "r") as f:
        for line in f.readlines():
            text_path = asr_path + line.replace('\n', '') + ".txt"
            if os.path.exists(text_path) == False:
                continue
            inputs.append(text_path)
            outputs.append("asrfeat/" + line.replace('\n', '') + ".asrfeat")

    matrix = vectorizer.fit_transform(inputs)
    for i in range(len(inputs)):
        with open(outputs[i], "w") as out:
            out.write(';'.join(map(str, matrix[i].toarray()[0])))

    print "ASR features generated successfully!"
