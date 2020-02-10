#!/bin/python
import numpy
import os
from sklearn.preprocessing import normalize
import sys

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print "Usage: {0} vocab_file, file_list".format(sys.argv[0])
        print "vocab_file -- path to the vocabulary file"
        print "file_list -- the list of videos"
        print "asr_path -- folder containing asr files"
        exit(1)

    vocab_file = sys.argv[1]
    file_list = sys.argv[2]
    asr_path = sys.argv[3]

    with open(vocab_file, "r") as f:
        word_indices = {k: v for v, k in enumerate(map(lambda x: x.replace('\n', ''), f.readlines()))}

    with open(file_list, "r") as f:
        for line in f.readlines():
            text_path = asr_path + line.replace('\n', '') + ".txt"
            if os.path.exists(text_path) == False:
                continue

            asrfeat_vector = numpy.zeros(len(word_indices))
            with open(text_path, "r") as cur_file:
                for sentence in cur_file.readlines():
                    for word in sentence.split(" "):
                        word = word.strip()
                        if len(word) == 0:
                            continue
                        if word.endswith("."):
                            word = word[:-1]
                        asrfeat_vector[word_indices[word.lower()]] += 1

            with open("asrfeat/" + line.replace('\n', '') + ".asrfeat", "w") as out:
                out.write(';'.join(map(str, normalize([asrfeat_vector])[0])))

    print "ASR features generated successfully!"
