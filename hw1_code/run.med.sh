#!/bin/bash

# An example script for multimedia event detection (MED) of Homework 1
# Before running this script, you are supposed to have the features by running run.feature.sh 

# Note that this script gives you the very basic setup. Its configuration is by no means the optimal. 
# This is NOT the only solution by which you approach the problem. We highly encourage you to create
# your own setups. 

# Paths to different tools; 
map_path=/home/ubuntu/tools/mAP
export PATH=$map_path:$PATH

#echo "Creating validation label files"
#mkdir -p val_labels
#for event in P001 P002 P003; do
#  echo "=========  Event $event  ========="
#  python scripts/create_label_file.py $event list/val val_labels/${event}_label || exit 1;
#done

echo "#####################################"
echo "#       MED with MFCC Features      #"
echo "#####################################"
mkdir -p mfcc_pred
# iterate over the events
for event in P001 P002 P003; do
  echo "=========  Event $event  ========="
  # now train a svm model
  python scripts/train_svm.py $event "kmeans/" mfcc_pred/svm.$event.model kmeans || exit 1;
  # apply the svm model to *ALL* the testing videos;
  # output the score of each testing video to a file ${event}_pred
  python scripts/test_svm.py mfcc_pred/svm.$event.model "kmeans/" mfcc_pred/${event}_val_mfcc.lst mfcc_pred/${event}_mfcc.lst kmeans || exit 1;
  # compute the average precision by calling the mAP package
  ap val_labels/${event}_label mfcc_pred/${event}_val_mfcc.lst
done

echo ""
echo "#####################################"
echo "#       MED with ASR Features       #"
echo "#####################################"
mkdir -p asr_pred
# iterate over the events
for event in P001 P002 P003; do
  echo "=========  Event $event  ========="
  # now train a svm model
  python scripts/train_svm.py $event "asrfeat/" asr_pred/svm.$event.model asrfeat || exit 1;
  # apply the svm model to *ALL* the testing videos;
  # output the score of each testing video to a file ${event}_pred 
  python scripts/test_svm.py asr_pred/svm.$event.model "asrfeat/" asr_pred/${event}_val_asr.lst asr_pred/${event}_asr.lst asrfeat || exit 1;
  # compute the average precision by calling the mAP package
  ap val_labels/${event}_label asr_pred/${event}_val_asr.lst
done

