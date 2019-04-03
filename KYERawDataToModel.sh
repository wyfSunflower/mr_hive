#!/usr/bin/env bash

if [ ! -d "KYEIndoorLocation" ]; then
    mkdir KYEIndoorLocation
fi
if [ -z "$1" ]; then
    echo "please input a valid raw data file path!"
    exit -1
fi
cat $1 | python KYEExtractRSSIFeature.py $1 > ./KYEIndoorLocation/raw_sample

sort -u ./KYEIndoorLocation/raw_sample > ./KYEIndoorLocation/raw_sample_unique
shuf ./KYEIndoorLocation/raw_sample_unique > ./KYEIndoorLocation/raw_sample_unique_shuf
TOTAL_RAW="./KYEIndoorLocation/raw_sample_unique_shuf"
total_sample_count=`cat $TOTAL_RAW | wc -l`

train_test_split_ratio=0.8
float_train_count=`echo "$total_sample_count * $train_test_split_ratio" | bc`

train_sample_count=`printf "%.0f\n" $float_train_count`

test_sample_count=`echo "$total_sample_count - $train_sample_count" | bc`

head -$train_sample_count $TOTAL_RAW > ./KYEIndoorLocation/train_sample_set
tail -$test_sample_count $TOTAL_RAW > ./KYEIndoorLocation/test_sample_set
python KYELearn.py > ./KYEIndoorLocation/auc_result