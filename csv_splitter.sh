#!/bin/bash
find "~/some_folder" -name "*.csv" | while read fname; do
    ls $fname;
    python csv_splitter.py --file-name $fname --maximum-lines-per-file 500000
done;
