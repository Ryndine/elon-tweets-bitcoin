# elon-tweets-bitcoin
Project 1 UCSD Extension Data Analytics Bootcamp

# Correlation Between Elon Musk's Twitter and Bitcoin Values
What this dataset is looking for is to see when Elon Musk tweets about bitcoin, if it influences the value of the coin when he does.

## Tools & Databases Used:
- Python / Jupyter
- Textblob
- Klines Binance Data Collection
- Twint

## What this data will be collecting:
- All Elon Musk tweets from 2021 to 2019 using Twint.
- All Bitcoin values and trades from 2021 to 2019 using Klines Binance Data.
- All Dogecoin values and trades from 2021 to 2019 using Klines Binance Data.

## Our methods and observation directions:
- Work on ETL for project.
- With Textblob, we will analyze all of Elon Musk's tweets to extract all noun phrases and store them into a new dataframe.
- Use the new DataFrame, we can find a ponit in time when Elon Musk says mentions "Telsa", "Bitcoin", and "Dogecoin", then check what the value of Bitcoin and Dogecoin were around that time.
- Using 5 & 30 minute periods we can calcuate and plot percent change which can be uased to verify correlation between Elon Musk's Tweets and Coin Values.
- The inclusion of Dogecoin data is so we have another currency to test the collected data against.
- Telsa is being analyzed as well because we can see values before Telsa accepted bitcoin vs after it started accepting it.

## Known Issues:
- The data is collected manually, therefore the accuracy of the results is directly influenced by our ability to correctly sort through all of Elon Musk's tweets.
- Due to time constraints we have to use common terms, and anything that's immediately identifiable.
