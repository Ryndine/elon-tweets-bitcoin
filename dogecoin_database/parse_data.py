import os
import pandas as pd

# Column names for the database
coin_header = [
    'Open Time',
    'Open',
    'High',
    'Low',
    'Close',
    'What',
    'Close Time',
    'Quote asset volume',
    'Trades',
    'Taker buy base asset volume',
    'Taker buy quote asset volume',
    'Ignore'
]
# Select which columns I want to pull
clean_columns = [0, 1, 4, 6, 8]
# Specify where the source csv files are
src_folder = 'Source'
# Specify where the cleaned files are to go
clean_folder = 'Cleaned'

# This function with run through all 23 files, retreive data we want, then output a csv to a new folder for further cleaning.
def clean_coin(coin):
    #Function that returns the columns we want form the csv files
    def csv_subset(path):
        return pd.read_csv(coin_path, names=coin_header, index_col=False).iloc[:, clean_columns]
    # Variable for the source folder
    coin_source = os.path.join(coin, src_folder)
    # Variable for the clean folder
    coin_cleaned = os.path.join(coin, clean_folder)
    # If statement that will generate the clean folder if it does not exist
    if not os.path.exists(coin_cleaned):
        os.mkdir(coin_cleaned)
    # Loop that goes through every source csv, reads it, then saves the columns I want to a new CSV.
    for file in os.listdir(coin_source):
        coin_path = os.path.join(coin_source, file)
        coin_dest = os.path.join(coin_cleaned, file)
        coin_df = csv_subset(coin_source)
        coin_df.to_csv(coin_dest, index=False)
    # Later added: This loop will merge all csv files into a single csv file
    df = None
    for f in os.listdir(coin_source):
        src_path = os.path.join(coin_source, f)
        # If statement to give dataframe a path to the source csv files if it doesn't have one
        if df is None:
            df = csv_subset(src_path)
        # Read each csv and append the dataframe
        else:
            df = df.append(csv_subset(src_path))
    # Creating the file name: 
    # Take the file name, split it from a string to a list a strings. 
    # Then take the first index (the main name of the files), add .csv to end.
    group_name = f.split('-')[0] + '.csv'
    # Give the new dataframe the name and path, then output it.
    dest_path = os.path.join(coin_dest, group_name)
    df.to_csv(dest_path, index=False)
# Activate the function by declaring the folder that holds the Source folder.
clean_coin('dogecoin_database')