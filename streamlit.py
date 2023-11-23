import streamlit as st
import numpy as np
from datetime import datetime

from v1_american_option_pricing_v1_cy import discrete_divs_cy


def year_fraction(start_date, end_date):
    # Function to calculate the year fraction between two dates
    days_in_year = 365.25  # considering leap years
    return (end_date - start_date).days / days_in_year


def div_days(date):
    start_of_year = datetime(date.year, 1, 1)
    day_count = (date - start_of_year).days + 1  # +1 because day count starts at 1
    return day_count / 365.25


# Create a sidebar for user inputs
st.header("American Style Discrete Dividend Option")

flag = st.selectbox("Option Type", options=[1, -1], format_func=lambda x: "Call" if x == 1 else "Put")
s = st.number_input("Initial Stock Price", min_value=0.0, value=25.0)
k = st.number_input("Strike Price", min_value=0.0, value=23.0)
r = st.number_input("Risk-Free Interest Rate", min_value=0.0, value=0.05)
sigma = st.number_input("Volatility", min_value=0.0, value=0.3)
valuation_date = st.text_input("Valuation Date", value="datetime(2023, 11, 22)")
expiration_date = st.text_input("Expiration Date", value="datetime(2024, 7, 15)")
steps = st.number_input("Steps in Binomial Model", min_value=1, value=100)
dividend_dates = st.text_input("Dividends Dates", value="[datetime(2024, 2, 15)]")
dividend_amounts = st.text_input("Dividends Dates", value="[0.8]")


# Calculate the option price
option_price = discrete_divs_cy(
    flag,
    s,
    k,
    r,
    sigma,
    year_fraction(eval(valuation_date), eval(expiration_date)),
    steps,
    np.array([div_days(date) for date in eval(dividend_dates)]),
    np.array(eval(dividend_amounts)),
)

# Display the result
st.header("Option Price")
st.markdown(f"# {option_price}")
