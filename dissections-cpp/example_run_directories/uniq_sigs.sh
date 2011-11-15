#!/bin/bash

FILENAME=$1

echo "unique_sigs.sh: $FILENAME"

TMP_FILE_1=`mktemp --tmpdir="$PWD"`
TMP_FILE_2=`mktemp --tmpdir="$PWD"`

sort $FILENAME > $TMP_FILE_1

if [ "$?" -ne 0 ]; then
    rm -f $TMP_FILE_1
    rm -f $TMP_FILE_2
    exit 1
fi 

uniq $TMP_FILE_1 > $TMP_FILE_2

if [ "$?" -ne 0 ]; then
    rm -f $TMP_FILE_1
    rm -f $TMP_FILE_2
    exit 1
fi 

mv $TMP_FILE_2 $FILENAME

rm $TMP_FILE_1
