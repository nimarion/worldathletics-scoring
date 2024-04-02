import tabula
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, help='PDF file to convert', required=True)
    parser.add_argument('--output', type=str, help='Output csv file name', required=True)
    args = parser.parse_args()

    input_file = args.input
    output_file = args.output

    tabula.convert_into(input_file, output_file, output_format="csv", pages='all')