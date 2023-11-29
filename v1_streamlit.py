import streamlit as st
import numpy as np
from datetime import datetime

from v1_option_pricing_v1_cy import discrete_divs_cy


def year_fraction(start_date, end_date):
    # Function to calculate the year fraction between two dates
    days_in_year = 365.25  # considering leap years
    return (end_date - start_date).days / days_in_year


def div_days(date):
    start_of_year = datetime(date.year, 1, 1)
    day_count = (date - start_of_year).days + 1  # +1 because day count starts at 1
    return day_count / 365.25


# Create a sidebar for user inputs
st.header("Options Pricing Discrete Dividend")

col1, col2 = st.columns(2)  # This will create two columns of equal width

with col1:
    model = st.selectbox("Model", options=[1, 0], format_func=lambda x: "American" if x == 1 else "European")
    flag = st.selectbox("Option Type", options=[1, -1], format_func=lambda x: "Call" if x == 1 else "Put")
    s = st.number_input("Initial Stock Price", min_value=0.0, value=25.0)
    k = st.number_input("Strike Price", min_value=0.0, value=23.0)
    r = st.number_input("Risk-Free Interest Rate", min_value=0.0, value=0.05, format="%.3f")
    sigma = st.number_input("Volatility", min_value=0.0, value=0.3, format="%.3f")

with col2:
    steps = st.number_input("Steps in Binomial Model", min_value=1, value=200)
    valuation_date = st.text_input("Valuation Date", value="datetime(2023, 11, 22)")
    expiration_date = st.text_input("Expiration Date", value="datetime(2024, 12, 15)")
    dividend_dates = st.text_input("Dividends Dates", value="[datetime(2024, 2, 15), datetime(2024, 8, 15)]", help="Format is [datetime(2024, 2, 15), datetime(2024, 8, 15)]")
    dividend_amounts = st.text_input("Dividends Amounts", value="[0.8, 0.8]", help="Format is [0.8, 0.8]")
    dividend_yield = st.number_input("Dividend Yield", min_value=0.0, value=0.015, format="%.3f")

# Calculate the option price
option_price = discrete_divs_cy(
    model,
    flag,
    s,
    k,
    r,
    sigma,
    year_fraction(eval(valuation_date), eval(expiration_date)),
    steps,
    np.array([div_days(date) for date in eval(dividend_dates)]),
    np.array(eval(dividend_amounts)),
    dividend_yield,
)

# Display the result
st.markdown(f"## {round(option_price, 3)}")
