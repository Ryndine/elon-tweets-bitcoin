# Elon Musk's Twitter and Bitcoin Values
[Ryan Mangeno](https://github.com/Ryndine)

## Objective: 
The goal of this project is to collect data and identify whether Elon Musk's twitter activity has any correlation with Bitcoin values.

## Tools & databases used:
- Python / Jupyter
- Textblob
- Klines Binance Data Collection
- Twint

## What this data will be collecting:
- All Elon Musk tweets from 2019 to 2021 using Twint.
- All Bitcoin values and trades from 2019 to 2021 using Klines Binance Data.
- All Dogecoin values and trades from 2019 to 2021 using Klines Binance Data.

## Methods and observation directions:
 
**How much data?**

I decided that I needed to include enough data to show trends before Elon Musk start tweeting out about bitcoin, as well as before tesla started accepting bitcoins. Also, since bitcoin values are rapidly changing I had to make sure that our data had enough timepoints in it to accurately declare whether tweets would show causation.

Knowing this I decided to look at tweets and bitcoin values per minute. Due to the data being per minute, it ended up quite large so I had to reduce the range I look at to 2019 and 2021. This still gave me enough data to view any possible correlations.

**Cleaning Coins.**

After collecting the data I needed I ended up with 23 CSV files total for bitcoin and dogecoin. In order to combine all the csv I created a script: "parse_data.py" that would read each file in the folder and retrieve data I wanted while creating a new single file.

To do this I ended up creating a list variable that would have the column headers from the CSV files. 
```
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
```
Using another variable I could manually select which column I wanted from the CSV files.
```
# Select which columns I want to pull
clean_columns = [0, 1, 4, 6, 8]
``
Lastly was setting up some variables for folders.
``
# Specify where the source csv files are
src_folder = 'Source'
# Specify where the cleaned files are to go
clean_folder = 'Cleaned'
```
I decided to add backups of all the cleaning in case things came up later and I needed a new file. Here is the function I decided to go with for the cleaning process:
```
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
```
Then to initialize the function you just enter the folder you want to run. SOme systems prefer absolute pathing, some were okay with relative.
```
# Activate the function by declaring the folder that holds the Source folder.
clean_coin('dogecoin_database')
```
**Preparing Elon Tweets & Textblob**

The data for Elon Musk was easier. Using Twint I was able to scrap twitter for all tweets Elon Musk made between 2019 and 2021, which also had the timestamp down to the seconds. Since the twint process didn't allow for declaring a specific range, it produced a csv file larger than I needed. So the first step was to read in the CSV and trim only what I needed.
```
# CSV Files & drop the extra columns that go beyond the dataset needed
elon_df = pd.read_csv('elon.csv')
elon_df.drop(elon_df.tail(1689).index,inplace=True)
```
Next was setting up the textblob function. I recommend reading [textblob documentation](https://textblob.readthedocs.io/en/dev/) to understand it better, but in short it's going to read the tweets and create new columns with noun phrases, polarity, and subjectivity.
```
# A textblod function that will read tweets, and create a column of noun phrases, polarity, and subjectivity
def add_tb_data(df: DataFrame, attrs: List[str]) -> DataFrame:
    def get_tb_attr(tweet, _attr: str):
        tb = TextBlob(tweet)
        return tb.__getattribute__(_attr)
    
    for attr in attrs:
        df[attr] = df['tweet'].apply(get_tb_attr, _attr=attr)

    return df
```
I also needed a function for cleaning up the date.
```
# Function for removing the time zone from the created_at column
def fix_time(t: str):
    suffix_pst = ' Pacific Standard Time'
    suffix_pdt = ' Pacific Daylight Time'
    return t.replace(suffix_pdt, '').replace(suffix_pst, '')
```
The last step to creating Elon's csv file was selecting the relevant columns and running the functions.
```
# Dataframe for the columns we need
elon_df = elon_df[['id', 'tweet', 'created_at']]
# Clean the date & time by removing the time zones
elon_df['created_at'] = elon_df['created_at'].apply(lambda x: fix_time(x))
# These will be used for the textblob function
add_attrs = ['noun_phrases', 'polarity', 'subjectivity']
# Run the new function on our database, create attribute columns, then populate them with phrases and values
elon_df = add_tb_data(elon_df, add_attrs)
# Saving dataframe for later use
elon_df.to_csv('elon_sentsubj.csv', index=False)
```

- Use the new DataFrame, we can find a ponit in time when Elon Musk says mentions "Telsa", "Bitcoin", and "Dogecoin", then check what the value of Bitcoin and Dogecoin were around that time.
- Using 5 & 30 minute periods we can calcuate and plot percent change which can be uased to verify correlation between Elon Musk's Tweets and Coin Values.
- The inclusion of Dogecoin data is so we have another currency to test the collected data against.
- Telsa is being analyzed as well because we can see values before Telsa accepted bitcoin vs after it started accepting it.

## Limitations:
- The data is collected manually, therefore the accuracy of the results is directly influenced by our ability to correctly sort through all of Elon Musk's tweets.
- Due to time constraints we have to use common terms, and anything that's immediately identifiable.
