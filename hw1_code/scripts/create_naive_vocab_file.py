#!/bin/python
import os
import sys
# Generate k-means features for videos; each video is represented by a single vector

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print "Usage: {0} file_list asr_path output_file".format(sys.argv[0])
        print "file_list -- the list of videos"
        print "asr_path -- folder containing asr files"
        print "output_file -- where to write the vocab file"
        exit(1)

    file_list = sys.argv[1]
    asr_path = sys.argv[2]
    output_file = sys.argv[3]

    words = set()
    with open(file_list, "r") as f:
        for line in f.readlines():
            text_path = asr_path + line.replace('\n', '') + ".txt"
            if os.path.exists(text_path) == False:
                continue
            with open(text_path, "r") as cur_file:
                for sentence in cur_file.readlines():
                    for word in sentence.split(" "):
                        word = word.strip()
                        if len(word) == 0:
                            continue
                        if word.endswith("."):
                            word = word[:-1]
                        words.add(word.lower())

    with open(output_file, "w") as f:
        for word in sorted(words):
            f.write(word + "\n")

    print "Generated vocabulary with %d words" % len(words)
