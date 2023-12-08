#!/bin/bash

INPUT=credit_card_transactions-ibm_v2.csv
OUTPUT_DIR=split
OUTPUT_NAME=part

split -l 2440000 $INPUT $OUTPUT_NAME --numeric-suffixes=0

for i in {00..09}
do 
    mv $OUTPUT_NAME$i $OUTPUT_DIR/$OUTPUT_NAME$i.csv
done

echo "Done csv splitting: MANUALLY DELETE HEADER FROM part00.csv!"