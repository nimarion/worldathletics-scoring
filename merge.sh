#!/bin/bash

merge_csv() {
    tail -n +2 "$2" >> "$3"
}

if [ $# -lt 2 ]; then
    echo "Usage: $0 file1.csv file2.csv [file3.csv ...] output.csv"
    exit 1
fi

# Extract the output file
output_file="${@: -1}"
# Remove the output file from the arguments list
input_files=${@:1:$#-1}

for file in $input_files; do
    merge_csv "$output_file" "$file" "$output_file"
done

head -n 1 "$1" > temp_first_line.txt
tail -n +2 "$output_file" >> temp_first_line.txt
mv temp_first_line.txt "$output_file"