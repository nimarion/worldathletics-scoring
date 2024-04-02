#!/bin/bash

if [ "$#" -ne 4 ]; then
    echo "Usage: $0 input_pdf output_csv gender environment"
    exit 1
fi

input_pdf="$1"
output_csv="$2"
gender=$3
environment=$4

python3 convert_pdf.py --input "$input_pdf" --output "$output_csv"
python3 convert_csv.py --input "$output_csv" --output "$output_csv" --gender "$gender" --environment "$environment"
