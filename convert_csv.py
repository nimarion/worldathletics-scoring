import pandas as pd 
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, help='File csv file to convert', required=True)
    parser.add_argument('--environment', type=str, help='Environment of the competition', choices=['Indoor', 'Outdoor'], required=True)
    parser.add_argument('--gender', type=str, help='Gender of scoring file', choices=['M', 'W', 'X'], required=True)
    parser.add_argument('--output', type=str, help='Output csv file name', required=True)
    args = parser.parse_args()

    f = open(args.input, "r")

    gender = args.gender
    environment = args.environment

    lines = []

    switchPointColumn = False

    # read every line in the file
    for line in f:
        line = line.replace("\n", "")
        if 'Points' in line:
            if line.endswith('Points'):
                switchPointColumn = True
            else:
                switchPointColumn = False
        if switchPointColumn:
            line = line.split(',')
            line = line[-1] + ',' + ','.join(line[:-1])
        
        lines.append(line)

    headers = []

    dict = []

    for line in lines:
        if 'Points' in line:
            headers = line.split(',')
            continue

        line = line.split(',')

        points = line[0]

        for i in range(1, len(line)):
            discipline = headers[i]
            performance = line[i]
            if performance == "-":
                continue
            dict.append({
                "Points": points,
                "Discipline": discipline,
                "Result": performance,
                "Gender": gender,
                "Environment": environment
            })

    df = pd.DataFrame(dict)
    df['Points'] = df['Points'].fillna(0)
    df['Points'] = df['Points'].replace('', 0)
    df = df[df['Points'] != 0]
    df['Points'] = df['Points'].astype(int)
    df = df.sort_values(by=['Discipline', 'Points'])
    df.to_csv(args.output, index=False)