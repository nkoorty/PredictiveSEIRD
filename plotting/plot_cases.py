import matplotlib.pyplot as plt
import json
import csv
from datetime import datetime, timedelta


def json_to_csv(json_file, csv_file, start_date):
    # Load JSON data
    with open(json_file, 'r') as f:
        data = json.load(f)

    # Extract the cases data
    cases = data['data']

    # Calculate dates
    dates = [start_date + timedelta(days=i) for i in range(len(cases))]

    # Write to CSV
    with open(csv_file, 'w', newline='') as csvfile:
        fieldnames = ['Date', 'Cases']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for date, case in zip(dates, cases):
            writer.writerow({'Date': date.strftime('%Y-%m-%d'), 'Cases': round(case)}) # noqa


def plot_cases(json_file):
    # Load JSON data
    with open(json_file, 'r') as f:
        data = json.load(f)

    # Extract the cases data
    cases = data['Cases']

    # Plot the data
    plt.plot(cases)
    plt.xlabel('Days')
    plt.ylabel('Cases')
    plt.title('COVID-19 Cases in Stockholm')
    plt.show()


def merge_data(cases_csv, deaths_json, output_csv):
    # Load cases data from CSV
    cases_data = {}
    with open(cases_csv, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cases_data[row['Date']] = int(row['Cases'])

    # Load deaths data from JSON
    with open(deaths_json, 'r') as f:
        data = json.load(f)
    deaths = data['data']
    deaths_start_date = datetime.strptime('2020-03-22', '%Y-%m-%d')
    deaths_dates = [deaths_start_date + timedelta(days=i) for i in range(len(deaths))] # noqa

    # Merge data
    merged_data = {}
    for date, cases in cases_data.items():
        merged_data[date] = {'Cases': cases, 'Deaths': 0}
    for date, deaths_count in zip(deaths_dates, deaths):
        date_str = date.strftime('%Y-%m-%d')
        if date_str in merged_data:
            merged_data[date_str]['Deaths'] = round(deaths_count)
        else:
            merged_data[date_str] = {'Cases': 0, 'Deaths': round(deaths_count)}

    # Write merged data to CSV
    with open(output_csv, 'w', newline='') as csvfile:
        fieldnames = ['Date', 'Cases', 'Deaths']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for date, counts in sorted(merged_data.items()):
            writer.writerow({'Date': date, 'Cases': counts['Cases'], 'Deaths': counts['Deaths']}) # noqa


# Usage example
start_date = datetime.strptime('2020-03-04', '%Y-%m-%d')
# json_to_csv('stockholm_cases.json', 'stockholm_cases.csv', start_date)
plot_cases('stockholm_data.csv')

# merge_data('stockholm_cases.csv', 'stockholm_deaths.json', 'stockholm_combined.csv') # noqa
