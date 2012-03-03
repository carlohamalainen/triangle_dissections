#!/bin/bash

# Sort and keep only the unique lines of a file. For paranoia we do this in 
# multiple steps instead of using the simpler expression "cat $FILENAME | sort | uniq > blah".

set -o nounset

FILENAME=$1

echo "unique_sigs.sh: $FILENAME"

TMP_FILE_1=`mktemp --tmpdir="$PWD"`
TMP_FILE_2=`mktemp --tmpdir="$PWD"`

# Sort the input file and store in the first temporary file:
sort $FILENAME > $TMP_FILE_1

if [ "$?" -ne 0 ]; then
    rm -f $TMP_FILE_1
    rm -f $TMP_FILE_2
    exit 1
fi 

# Find the unique lines of this file, storing in the second temporary file:
uniq $TMP_FILE_1 > $TMP_FILE_2

if [ "$?" -ne 0 ]; then
    rm -f $TMP_FILE_1
    rm -f $TMP_FILE_2
    exit 1
fi 

# If all went well, remove temporary files, delete the original file, and
# move the sorted and unique file back to the original filename.
mv $TMP_FILE_2 $FILENAME
rm $TMP_FILE_1
