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
 
**Collecting Data**

To answer whether or not Elon Musk influences bitcoin values, I needed to have a dataset that I could view values exactly when a tweet happens. I decided that I needed to include enough data to show trends before Elon Musk start tweeting out about bitcoin as well as before tesla started accepting bitcoins in order to increase accuracy of the analysis. Also, since bitcoin values are rapidly changing I had to make sure that the data had enough timestamps in it to accurately declare whether tweets would show causation.

Knowing this I decided to look at tweets and bitcoin values per minute. Due to the data being per minute it ended up quite large so I had to reduce the range I look at to 2019 and 2021. This still gave me enough data to view any possible correlations.

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
**Final Dataframe**

No that I have two cleaned csv files, I'm able to pair coin values to a moment in time when a tweet happened. The next step was understanding how to analyze the data. The conclusion was to be able to see when a tweet happens and view coin values before and after the tweet. Because values rapidly change, anything beyond 30 minutes was considered to have too many possible causations. Since 30 minutes itself was a long period of time, I also decided to include 5 minutes to see more immediate effects.

To accomplish this I first had to make minor adjustments to the dataframe. Since I needed to read the noun-phrases for key phrases I created a function would would convert the string into a list of strings.
```
# Function to change subject string into a list of strings
def is_subject(subject_field, subject_set):
    subjects = set([i.lower().replace("'", '') for i in subject_field.strip('[]').split(', ')])
    check_subject = list(subject_set & subjects) != []
    if check_subject:
        return 1
    else:
        return 0
```
After that I'm setting up variables that hold what keywords I'm looking for. This process is done manually by reading Elon's Tweets and finding words he uses.
```
# For Function: Noun phrases I want to find in database
tesla_fields = set(['tesla', 'autopilot'])
btc_fields = set(['btc', 'bitcoin'])
eth_fields = set(['ethereum', 'eth'])
doge_fields = set(['dogecoin', 'doge', 'egod'])
crypto_fields = {*btc_fields, *eth_fields, *doge_fields, *['crypto', 'moon', 'currency']}
```
Next I create new columns of 1's and 0's to show whether a tweet contains the field values I'm looking for.
```
# For Function: Creating column to store values from the function.
elon_df['is_tesla'] = elon_df['noun_phrases'].apply(func=is_subject, subject_set=tesla_fields)
elon_df['is_doge'] = elon_df['noun_phrases'].apply(func=is_subject, subject_set=doge_fields)
elon_df['is_btc'] = elon_df['noun_phrases'].apply(func=is_subject, subject_set=btc_fields)
elon_df['is_crypto'] = elon_df['noun_phrases'].apply(func=is_subject, subject_set=crypto_fields)
```
Now that Elon's dataframe is ready for analysis, I need to setup the coin dataframes. First was just a little more cleanup.
```
# Setting up bitcoin dataframe
bitcoin = R'bitcoin_database\Cleaned\BTCUSDT.csv'
bitcoin_df = pd.read_csv(bitcoin)
for col in ['Open Time', 'Close Time']:
    bitcoin_df[col] = pd.to_datetime(bitcoin_df[col], unit='ms')
bitcoin_df = bitcoin_df.drop(columns=['Close', 'Close Time'])

# Setting up dogecoin dataframe
dogecoin = R'dogecoin_database\Cleaned\DOGEUSDT.csv'
dogecoin_df = pd.read_csv(dogecoin)
for col in ['Open Time', 'Close Time']:
    dogecoin_df[col] = pd.to_datetime(dogecoin_df[col], unit='ms')
dogecoin_df = dogecoin_df.drop(columns=['Close', 'Close Time'])
```
After I worked on the function that would find the intervals for each tweet and the coin values for that interval.
```
# Function that will return new dataframe
def find_intervals(df_row, target_coin: DataFrame, interval: str = '5 minutes', plusminus='after'):
    td = pd.Timedelta(interval)
    timestamp = df_row['created_at']
    #  For current tweet (row) pull target coin data for specified interval before or after tweets timestamp
    if plusminus == 'after':
        coin_df = target_coin.where(target_coin['Open Time'].between(timestamp, timestamp+td)).dropna()
    elif plusminus == 'before':
        coin_df = target_coin.where(target_coin['Open Time'].between(timestamp, timestamp-td)).dropna()
    # Find values I want and populate columns for them
    try:
        dfmin = coin_df['Open'].iloc[0]
        dfmax = coin_df['Open'].iloc[-1]

        change = (dfmax - dfmin) / dfmin

        df_row[interval + ' beginning value'] = dfmin
        df_row[interval + ' end value'] = dfmax
        df_row[interval + ' change pct'] = change

        return df_row

    except Exception as e:
        return df_row.apply(lambda x: None)
```
Last part was to simply create my variables, new dataframes, and a loop to apply the new function.
```
# Defining the intervals I want for the 
intervals = ['5 minutes', '30 minutes']
intervals_plusminus = [('5 minutes', 'after'), ('30 minutes', 'after')]

# Loop will apply function to every row
crypto_btcval_tweets = crypto_tweets
crypto_dogeval_tweets = crypto_tweets
for interval, plusminus in intervals_plusminus:
    crypto_btcval_tweets = crypto_btcval_tweets.apply(find_intervals, axis=1, target_coin=bitcoin_df, interval=interval, plusminus=plusminus)
    crypto_dogeval_tweets = crypto_dogeval_tweets.apply(find_intervals, axis=1, target_coin=dogecoin_df, interval=interval, plusminus=plusminus)

crypto_btcval_tweets = crypto_btcval_tweets.dropna()
crypto_dogeval_tweets = crypto_dogeval_tweets.dropna()
```
Since I'm plotting all the data I ran a little more cleanup on headers, and made csv files for the final dataset.
```
# Not sure why columns got messed up, but fixing it here
crypto_btcval_tweets = crypto_btcval_tweets[['id', 'created_at', 'tweet', 'noun_phrases', 'polarity', 'subjectivity', 'is_btc', 'is_doge', 'is_crypto', 'is_tesla', '5 minutes beginning value', '5 minutes end value', '5 minutes change pct', '30 minutes beginning value', '30 minutes end value', '30 minutes change pct']]
crypto_dogeval_tweets = crypto_dogeval_tweets[['id', 'created_at', 'tweet', 'noun_phrases', 'polarity', 'subjectivity', 'is_btc', 'is_doge', 'is_crypto', 'is_tesla', '5 minutes beginning value', '5 minutes end value', '5 minutes change pct', '30 minutes beginning value', '30 minutes end value', '30 minutes change pct']]

crypto_btcval_tweets.to_csv('crypto_btcval_tweets.csv', index=False)
crypto_dogeval_tweets.to_csv('crypto_dogeval_tweets.csv', index=False)
```

**Analysis**




## Limitations:
- The data is collected manually, therefore the accuracy of the results is directly influenced by our ability to correctly sort through all of Elon Musk's tweets.
- Due to time constraints we have to use common terms, and anything that's immediately identifiable.
