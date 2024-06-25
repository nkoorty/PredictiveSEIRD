import pandas as pd


# Function to filter the CSV data
def filter_csv(input_file, output_file):
    # Read the CSV file
    df = pd.read_csv(input_file)
    # Filter the DataFrame to include only the desired columns
    filtered_df = df[['date', 'cumulative_confirmed', 'cumulative_deceased']]
    filtered_df = filtered_df.fillna(0)
    # Save the filtered DataFrame to a new CSV file
    filtered_df.to_csv(output_file, index=False)


# File paths (replace 'input.csv' and 'output.csv' with your file names)
input_file = '../data/Stockholm_COVID.csv'
output_file = '../data/stockholm_filtered.csv'

# Call the function to filter the CSV data
filter_csv(input_file, output_file)

print("Filtered data saved to", output_file)
