# project-grizzly
Project 1 UCSD Extension Data Analytics Bootcamp

# Correlation Between Elon Musk's Twitter and Bitcoin Values
What this dataset is looking for is to see when Elon Musk tweets about bitcoin, if it influences the value of the coin when he does.

Tools & Databases Used:
- Python / Jupyter
- Textblob
- Klines Binance Data Collection
- Twint

What this data will be collecting:
- All Elon Musk tweets from 2021 to 2019 using Twint.
- All Bitcoin values and trades from 2021 to 2019 using Klines Binance Data.
- All Dogecoin values and trades from 2021 to 2019 using Klines Binance Data.

Our methods and observation directions:
- First we'll be using Textblob to create a function that can read all the tweets and identify when selected words are being used. Is this case we'll be looking for "Telsa", "Bitcoin", "Dogecoin, and all other phrases within those categories that we identify.
- Using that new DataFrame we will be able to compare those specific tweets in time to the value of the bitcoin that matches that date & time. In order to improve accuracy we'll be looking between 5 and 30 minute intervals and calculating the percent change between them.
- Using percent change we can create a scatter plot to see overall if his tweets have had a positive or negative influence over bitcoin value.
- Lastly we can find out if there is any correlation between how many times he tweets in a day vs the amount of trades that happened in a day.
- We're bringing in Dogecoin data as well so that we can test this against another coin.
- Telsa is being analyzed as well because we can see values before Telsa accepted bitcoin vs after it started accepting it.
