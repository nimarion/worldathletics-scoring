import pandas as pd
import argparse 

def isTechnical(discipline):
    if any(char.isdigit() for char in discipline):
        return False
    return True

def performance_to_float(performance):
    performance = performance.strip().replace(",", ".")
    if ":" in performance:
        # Running disciplines with format "1:23.45" or "1:23" or "2:29:08"
        parts = performance.split(":")
        if len(parts) < 2:
            print(f"Invalid performance: {performance}")
            return 0
        if "." in parts[1]:
            sub_parts = parts[1].split(".")
            minutes = int(parts[0])
            seconds = int(sub_parts[0])
            milliseconds = int(sub_parts[1])
            return (minutes * 60 + seconds) * 1000 + milliseconds
        if (len(parts) == 3):
            hours = int(parts[0])
            minutes = int(parts[1])
            if ("." in parts[2]):
                sub_parts = parts[2].split(".")
                seconds = int(sub_parts[0])
                milliseconds = int(sub_parts[1])
                return (hours * 3600 + minutes * 60 + seconds) * 1000 + milliseconds
            seconds = int(parts[2])
            return hours * 3600 + minutes * 60 + seconds
        return int(parts[0]) * 60 + int(parts[1])
    else:
        # Technical disciplines and sprint disciplines with format "10.23", "1.70"
        try:
            converted_performance = float(performance)
        except ValueError:
            print(f"Invalid performance: {performance}")
            return 0
        return int(converted_performance * 1000)
    

def calculate_points(sex, environment, discipline, result):
    isTechnicalDiscipline = isTechnical(discipline)
    disciplinePerformance = performance_to_float(result)

    print(disciplinePerformance)

    df = pd.read_csv("data/merged.csv")
    df = df.drop_duplicates()

    df = df[(df['Discipline'] == discipline) & (df['Environment'] == environment) & (df["Gender"] == sex)]
    df['Performance'] = df['Result'].apply(performance_to_float)

    if not isTechnicalDiscipline:
        df = df[df['Performance'] >= disciplinePerformance]
        closest_performance = df.iloc[(df['Performance'] - disciplinePerformance).abs().argsort()[:1]]
    else:
        df = df[df['Performance'] <= disciplinePerformance]
        closest_performance = df.iloc[(df['Performance'] - disciplinePerformance).abs().argsort()[:1]]

    points = 0

    if not closest_performance.empty:
        points = closest_performance['Points'].values[0]

    return points


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calculate scoring points')
    parser.add_argument('--sex', choices=["M", "W"], required=True)
    parser.add_argument('--environment', choices=["Outdoor", "Indoor"], required=True, type=str)
    parser.add_argument('--discipline', required=True, type=str)
    parser.add_argument('--result', required=True, type=str)
    args = parser.parse_args()

    points = calculate_points(args.sex, args.environment, args.discipline, args.result)
    print(points)