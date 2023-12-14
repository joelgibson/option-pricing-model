import yfinance as yf
import pandas as pd
import datetime
import numpy as np


# Load the list of Australian stocks from a text file called 'au_stocks_list.txt'
with open("v1_stocks_list.txt") as f:
    tickers = f.read().splitlines()

# Set up date ranges
end = datetime.datetime.now()
start = end - datetime.timedelta(days=365*2)


import pdb; pdb.set_trace()


# Get the ticker data for each stock
data = []
for ticker in tickers:
    print("Fetching data for: ", ticker)
    stock = yf.Ticker(ticker)
    df = stock.history(start=start, end=end)
    df["Ticker"] = ticker
    data.append(df)

# Combine data into a single pandas dataframe
df = pd.concat(data)

temp = []
# Iterate over each stock ticker in the dataframe
for ticker in df["Ticker"].unique():
    # Retrieve all data for this stock ticker
    stock_data = df[df["Ticker"] == ticker]

    # Add the moving averages to the new dataframe
    temp.append(
        pd.DataFrame({
        "Ticker": [ticker] * len(stock_data),
        "Date": stock_data.index,
        "Close": stock_data["Close"],
        })
    )

# Print the new dataframe
df = pd.concat(temp)

# 3M Realiased Vol
df["LogReturn"] = np.log(df["Close"] / df["Close"].shift(1))
df["Realised3MVol"] = df["LogReturn"].rolling(window=63).std() * np.sqrt(252)


# Get me the last rows of the df for each ticker
df_vol = df.groupby("Ticker").tail(1)
df_vol.to_csv("docs/volatility.csv")
df_vol