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

# Do some calcs
df["Vol"] = df.groupby("Ticker")["Close"].transform(lambda x: x.pct_change().rolling(250).std() * np.sqrt(252))
df["VolStd"] = df.groupby("Ticker")["Vol"].transform(np.std)
df["Vol1m"] = df.groupby("Ticker")["Close"].transform(lambda x: x.pct_change().rolling(21).std() * np.sqrt(252))

# df.to_csv("~/Downloads/df.csv")

# Get me the last rows of the df for each ticker
df_vol = df.groupby("Ticker").tail(1)

# Get me vol is above or below 2 std
N = 2
df_vol["VolDiff"] = df_vol["Vol"] - df_vol["Vol1m"]
df_vol["VolDiffAboveNStd"] = df_vol["VolDiff"] > N * df_vol["VolStd"]
df_vol["VolDiffBelowNStd"] = df_vol["VolDiff"] < -N * df_vol["VolStd"]
filt = (df_vol["VolDiffAboveNStd"] == True) | (df_vol["VolDiffBelowNStd"] == True)
df_vol = df_vol[filt]

# Output to CSV
df_vol.to_csv("~/Downloads/volatility.csv")

df_vol