import streamlit as st
from v1_american_option_pricing_v1 import discrete_divs

# Create a sidebar for user inputs
st.header("American Style Discrete Dividend Option")

flag = st.selectbox("Option Type", options=[1, -1], format_func=lambda x: "Call" if x == 1 else "Put")
s = st.number_input("Initial Stock Price", min_value=0.0, value=25.0)
k = st.number_input("Strike Price", min_value=0.0, value=23.0)
r = st.number_input("Risk-Free Interest Rate", min_value=0.0, value=0.05)
sigma = st.number_input("Volatility", min_value=0.0, value=0.3)
valuation_date = st.text_input("Valuation Date", value="datetime(2023, 11, 22)")
expiration_date = st.text_input("Expiration Date", value="datetime(2024, 7, 15)")
dividends = st.text_input("Dividends", value="[(datetime(2024, 2, 15), 0.8)]")
steps = st.number_input("Steps in Binomial Model", min_value=1, value=100)


# Calculate the option price
option_price = discrete_divs(
    flag,
    s,
    k,
    r,
    sigma,
    eval(valuation_date),
    eval(expiration_date),
    steps,
    eval(dividends),
  )

# Display the result
st.header("Option Price")
st.markdown(f"# {option_price}")
