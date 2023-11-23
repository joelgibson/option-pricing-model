# https://github.com/TRBD/option_pricing_cython/tree/master

from datetime import datetime, timedelta
import numpy as np
from typing import List, Tuple


N_DECIMAL = 10

def decimal_round(num: float) -> float:
    """
    Round a number to N_DECIMAL decimal places.

    Parameters:
    num: The number to be rounded

    Returns:
    The rounded number
    """
    return round(num, N_DECIMAL)


def option_binomial(
    flag: int,
    s: float,
    k: float,
    r: float,
    sigma: float,
    valuation_date: datetime,
    expiration_date: datetime,
    steps: int
) -> float:
    """
    Calculate the price of an American option using a binomial model.

    Parameters:
    flag: The type of option (1 for call, -1 for put)
    s: The initial stock price
    k: The strike price
    r: The risk-free interest rate
    sigma: The volatility of the underlying asset
    valuation_date: The date when the option is valued
    expiration_date: The date when the option expires
    steps: The number of time steps in the binomial model

    Returns:
    The price of the option
    """
    t = (expiration_date - valuation_date).days / 365.0  # Time to maturity in years
    R = decimal_round(np.exp(r * (t / steps)))  # Discount factor
    r_inv = decimal_round(1. / R)  # Inverse of the discount factor
    u = decimal_round(np.exp(sigma * np.sqrt(t / steps)))  # Upward movement factor
    uu = decimal_round(u * u)  # Square of the upward movement factor
    d = decimal_round(1. / u)  # Downward movement factor
    p_up = decimal_round((R - d) / (u - d))  # Probability of an upward movement
    p_down = decimal_round(1.0 - p_up)  # Probability of a downward movement
    prices = np.empty(steps + 1)  # Array to store the stock prices
    option_values = np.empty(steps + 1)  # Array to store the option values
    prices[0] = decimal_round(s * (d**steps))  # Initial stock price
    for i in range(1, steps + 1):
        prices[i] = decimal_round(uu * prices[i-1])  # Calculate the stock price
    for i in range(steps+1):
        option_values[i] = decimal_round(np.max([0.0, flag*(prices[i] - k)]))  # Calculate the option value
    for step in range(steps-1, -1, -1):
        for i in range(step+1):
            option_values[i] = decimal_round((p_up * option_values[i+1] + p_down * option_values[i]) * r_inv)  # Update the option value
            prices[i] = decimal_round(d * prices[i+1])  # Update the stock price
            option_values[i] = decimal_round(np.max([option_values[i], flag*(prices[i] - k)]))  # Update the option value
    return decimal_round(option_values[0])  # Return the option price


def discrete_divs(flag: int,
        s: float,
        k: float,
        r: float,
        sigma: float,
        valuation_date: datetime,
        expiration_date: datetime,
        steps: int,
        dividend_info: List[Tuple[datetime, float]]) -> float:
    """
    Calculate the price of an American option with discrete dividends using a binomial model.

    Parameters:
    flag: The type of option (1 for call, -1 for put)
    s: The initial stock price
    k: The strike price
    r: The risk-free interest rate
    sigma: The volatility of the underlying asset
    valuation_date: The date when the option is valued
    expiration_date: The date when the option expires
    steps: The number of time steps in the binomial model
    dividend_info: A list of tuples, each containing a dividend payment date and amount

    Returns:
    The price of the option
    """
    t = (expiration_date - valuation_date).days / 365.0  # Time to maturity in years
    div_times = np.array([((d[0] - valuation_date).days / 365.0) for d in dividend_info])  # Times at which dividends are paid
    div_amounts = np.array([d[1] for d in dividend_info])  # Amounts of the dividends
    no_dividends = len(div_times)  # Number of dividends
    if no_dividends == 0:
        return option_binomial(flag, s, k, r, sigma, valuation_date, expiration_date, steps)  # If no dividends, use the binomial model

    steps_before_dividend = decimal_round(int((div_times[0] / t) * steps))  # Number of steps before the first dividend
    R = decimal_round(np.exp(r * (t / steps)))  # Discount factor
    r_inv = decimal_round(1. / R)  # Inverse of the discount factor
    u = decimal_round(np.exp(sigma * np.sqrt(t/ steps)))  # Upward movement factor
    d = decimal_round(1. / u)  # Downward movement factor
    p_up = decimal_round((R-d)/(u-d))  # Probability of an upward movement
    p_down = decimal_round(1.0 - p_up)  # Probability of a downward movement
    dividend_amount = decimal_round(div_amounts[0])  # Amount of the first dividend
    tmp_dividend_times = np.empty(no_dividends - 1)  # Array to store the times of the remaining dividends
    tmp_dividend_amounts = np.empty(no_dividends - 1)  # Array to store the amounts of the remaining dividends
    for i in range(no_dividends - 1):
        tmp_dividend_times[i] = decimal_round(div_times[i+1])  # Store the time of the next dividend
        tmp_dividend_amounts[i] = decimal_round(div_amounts[i+1])  # Store the amount of the next dividend
    prices = np.empty(steps_before_dividend + 1)  # Array to store the stock prices
    option_values = np.empty(steps_before_dividend + 1)  # Array to store the option values
    prices[0] = decimal_round(s * d ** (steps_before_dividend))  # Initial stock price
    for i in range(1, steps_before_dividend + 1):
        prices[i] = decimal_round(u * u * prices[i-1])  # Calculate the stock price
    for i in range(steps_before_dividend+1):
        value_alive = decimal_round(
            discrete_divs(
                flag,
                prices[i] - dividend_amount,
                k,
                r,
                sigma,
                valuation_date + timedelta(days=int(div_times[0]*365)),
                expiration_date,
                steps - steps_before_dividend,
                [(d[0], d[1]) for d in dividend_info[1:]])
            )  # Calculate the option value if the option is not exercised
        option_values[i] = decimal_round(np.max([value_alive, flag*(prices[i] - k)]))  # Calculate the option value
    for step in range(steps_before_dividend - 1, -1, -1):
        for i in range(step+1):
            prices[i] = decimal_round(d * prices[i+1])  # Update the stock price
            option_values[i] = decimal_round((p_down * option_values[i] + p_up * option_values[i+1]) * r_inv)  # Update the option value
            option_values[i] = decimal_round(np.max([option_values[i], flag*(prices[i] - k)]))  # Update the option value

    return decimal_round(option_values[0])  # Return the option price


def test_discrete_divs():

    TOLERANCE = 0.05  # TOLERANCE for the difference between the actual and expected option prices

    # These are from docs/American option pricing examples.xlsx
    actual = decimal_round(
        discrete_divs(1, 25, 23, 0.05, 0.3, datetime(2023, 11, 22), datetime(2024, 2, 14), 100, []))
    expected = 2.788  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE


    actual = decimal_round(
        discrete_divs(-1, 25, 23, 0.05, 0.3, datetime(2023, 11, 22), datetime(2024, 2, 14), 100, []))
    expected = 0.532  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE


    actual = decimal_round(
        discrete_divs(1, 25, 25, 0.05, 0.3, datetime(2023, 11, 22), datetime(2024, 2, 14), 100, []))
    expected = 1.573  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE


    actual = decimal_round(
        discrete_divs(-1, 25, 25, 0.05, 0.3, datetime(2023, 11, 22), datetime(2024, 2, 14), 100, []))
    expected = 1.311  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE


    actual = decimal_round(
        discrete_divs(1, 25, 27, 0.05, 0.3, datetime(2023, 11, 22), datetime(2024, 2, 14), 100, []))
    expected = 0.788  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE


    actual = decimal_round(
        discrete_divs(-1, 25, 27, 0.05, 0.3, datetime(2023, 11, 22), datetime(2024, 2, 14), 100, []))
    expected = 2.538  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE


    # Divends 1
    actual = decimal_round(
        discrete_divs(1, 25, 23, 0.05, 0.3, datetime(2023, 11, 22), datetime(2024, 7, 15), 100, [(datetime(2024, 2, 15), 0.8)]))
    expected = 3.394  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE


    actual = decimal_round(
    discrete_divs(-1, 25, 23, 0.05, 0.3, datetime(2023, 11, 22), datetime(2024, 7, 15), 100, [(datetime(2024, 2, 15), 0.8)]))
    expected = 1.442  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE


    actual = decimal_round(
        discrete_divs(1, 25, 25, 0.05, 0.3, datetime(2023, 11, 22), datetime(2024, 7, 15), 100, [(datetime(2024, 2, 15), 0.8)]))
    expected = 2.35  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE


    actual = decimal_round(
    discrete_divs(-1, 25, 25, 0.05, 0.3, datetime(2023, 11, 22), datetime(2024, 7, 15), 100, [(datetime(2024, 2, 15), 0.8)]))
    expected = 2.419  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE


    actual = decimal_round(
        discrete_divs(1, 25, 27, 0.05, 0.3, datetime(2023, 11, 22), datetime(2024, 7, 15), 100, [(datetime(2024, 2, 15), 0.8)]))
    expected = 1.581  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE


    actual = decimal_round(
    discrete_divs(-1, 25, 27, 0.05, 0.3, datetime(2023, 11, 22), datetime(2024, 7, 15), 100, [(datetime(2024, 2, 15), 0.8)]))
    expected = 3.668  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE

    # Divends 2
    actual = decimal_round(
    discrete_divs(1, 25, 23, 0.05, 0.3, datetime(2023, 11, 22), datetime(2024, 12, 15), 100, [(datetime(2024, 2, 15), 0.8), (datetime(2024, 8, 15), 0.8)]))
    expected = 3.862  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE


    actual = decimal_round(
    discrete_divs(-1, 25, 23, 0.05, 0.3, datetime(2023, 11, 22), datetime(2024, 12, 15), 100, [(datetime(2024, 2, 15), 0.8), (datetime(2024, 8, 15), 0.8)]))
    expected = 2.129  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE


    actual = decimal_round(
    discrete_divs(1, 25, 25, 0.05, 0.3, datetime(2023, 11, 22), datetime(2024, 12, 15), 100, [(datetime(2024, 2, 15), 0.8), (datetime(2024, 8, 15), 0.8)]))
    expected = 2.889  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE


    actual = decimal_round(
    discrete_divs(-1, 25, 25, 0.05, 0.3, datetime(2023, 11, 22), datetime(2024, 12, 15), 100, [(datetime(2024, 2, 15), 0.8), (datetime(2024, 8, 15), 0.8)]))
    expected = 3.164  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE

    actual = decimal_round(
    discrete_divs(1, 25, 27, 0.05, 0.3, datetime(2023, 11, 22), datetime(2024, 12, 15), 100, [(datetime(2024, 2, 15), 0.8), (datetime(2024, 8, 15), 0.8)]))
    expected = 2.135  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE


    actual = decimal_round(
    discrete_divs(-1, 25, 27, 0.05, 0.3, datetime(2023, 11, 22), datetime(2024, 12, 15), 100, [(datetime(2024, 2, 15), 0.8), (datetime(2024, 8, 15), 0.8)]))
    expected = 4.402  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE


    # THESE ARE FROM THE PDF - docs/Vol Adjustment for Dividend-Paying Stocks (Haug, Haug, Lewis 2003)
    # actual = decimal_round(
    #     discrete_divs(1, 100, 130, 0.06, 0.3, datetime(2023, 1, 1), datetime(2024, 1, 1), 100, [(datetime(2023, 7, 2), 30)]))
    # expected = 3.45  # Expected option price
    # print("Expected:", expected, "Actual:", actual)
    # assert abs((actual - expected) / expected) < TOLERANCE


    # # THESE ARE FROM THE PAPER - Vol Adjustment for Dividend-Paying Stocks (Haug, Haug, Lewis 2003)
    # actual = decimal_round(
    #     discrete_divs(1, 100, 100, 0.06, 0.3, datetime(2023, 1, 1), datetime(2024, 1, 1), 100, [(datetime(2023, 7, 2), 7)]))
    # expected = 11.6545  # Expected option price
    # print("Expected:", expected, "Actual:", actual)
    # assert abs((actual - expected) / expected) < TOLERANCE


    # actual = decimal_round(
    #     discrete_divs(1, 100, 130, 0.06, 0.3, datetime(2023, 1, 1), datetime(2024, 1, 1), 100, [(datetime(2023, 7, 2), 7)]))
    # expected = 3.4595  # Expected option price
    # print("Expected:", expected, "Actual:", actual)
    # assert abs((actual - expected) / expected) < TOLERANCE


    # actual = decimal_round(
    #     discrete_divs(1, 100, 70, 0.06, 0.3, datetime(2023, 1, 1), datetime(2024, 1, 1), 100, [(datetime(2023, 7, 2), 7)]))
    # expected = 32.4608  # Expected option price
    # print("Expected:", expected, "Actual:", actual)
    # assert abs((actual - expected) / expected) < TOLERANCE


    # actual = decimal_round(
    #     discrete_divs(1, 100, 100, 0.06, 0.3, datetime(2023, 1, 1), datetime(2024, 1, 1), 100, [(datetime(2023, 7, 2), 30)]))
    # expected = 9.99283  # Expected option price
    # print("Expected:", expected, "Actual:", actual)
    # assert abs((actual - expected) / expected) < TOLERANCE


    # actual = decimal_round(
    #     discrete_divs(1, 100, 130, 0.06, 0.3, datetime(2023, 1, 1), datetime(2024, 1, 1), 100, [(datetime(2023, 7, 2), 30)]))
    # expected = 1.7855  # Expected option price
    # print("Expected:", expected, "Actual:", actual)
    # assert abs((actual - expected) / expected) < TOLERANCE


    # actual = decimal_round(
    #     discrete_divs(1, 100, 70, 0.06, 0.3, datetime(2023, 1, 1), datetime(2024, 1, 1), 100, [(datetime(2023, 7, 2), 30)]))
    # expected = 32.3037  # Expected option price
    # print("Expected:", expected, "Actual:", actual)
    # assert abs((actual - expected) / expected) < TOLERANCE


    # actual = decimal_round(
    #     discrete_divs(1, 100, 100, 0.06, 0.3, datetime(2023, 1, 1), datetime(2024, 1, 1), 100, [(datetime(2023, 7, 2), 50)]))
    # expected = 9.8828  # Expected option price
    # print("Expected:", expected, "Actual:", actual)
    # assert abs((actual - expected) / expected) < TOLERANCE


    # actual = decimal_round(
    #     discrete_divs(1, 100, 130, 0.06, 0.3, datetime(2023, 1, 1), datetime(2024, 1, 1), 100, [(datetime(2023, 7, 2), 50)]))
    # expected = 1.6492  # Expected option price
    # print("Expected:", expected, "Actual:", actual)
    # assert abs((actual - expected) / expected) < TOLERANCE


    # actual = decimal_round(
    #     discrete_divs(1, 100, 70, 0.06, 0.3, datetime(2023, 1, 1), datetime(2024, 1, 1), 100, [(datetime(2023, 7, 2), 50)]))
    # expected = 32.3034  # Expected option price
    # print("Expected:", expected, "Actual:", actual)
    # assert abs((actual - expected) / expected) < TOLERANCE

# test_discrete_divs()