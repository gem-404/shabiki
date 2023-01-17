#!/bin/bash

for file in *.txt; do

    sed -i '/duckduckgo/d' $file
    sed -i '/javascript/d' $file
    sed -i '/spreadprivacy/d' $file

    cat $file | sort -u | uniq | tee $file > /dev/null

done
