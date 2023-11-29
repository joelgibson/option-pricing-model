import timeit
import numpy as np
from datetime import datetime
from v1_option_pricing_v1 import decimal_round
from v1_option_pricing_v1_cy import discrete_divs_cy

TOLERANCE = 0.05  # TOLERANCE for the difference between the actual and expected option prices

def year_fraction(start_date, end_date):
    # Function to calculate the year fraction between two dates
    days_in_year = 365.25  # considering leap years
    return (end_date - start_date).days / days_in_year


def div_days(date):
    start_of_year = datetime(date.year, 1, 1)
    day_count = (date - start_of_year).days + 1  # +1 because day count starts at 1
    return day_count / 365.25


def test_discrete_divs_cython():


    # t = year_fraction(datetime(2023, 11, 22), datetime(2024, 12, 15))
    # div_times = np.array([
    #     div_days(datetime(2023, 12, 31)),
    #     div_days(datetime(2024, 8, 15)),
    # ])
    # div_amt = np.array([
    #   0.8,
    #   0.8,
    # ])
    # actual = decimal_round(
    # discrete_divs_cy(1, -1, 25, 100, 0.05, 0.3, t, 200, div_times, div_amt, 0))
    # expected = 4.573  # Expected option price
    # print("Expected:", expected, "Actual:", actual)
    # assert abs((actual - expected) / expected) < TOLERANCE


    t = year_fraction(datetime(2023, 11, 22), datetime(2024, 2, 14))
    actual = decimal_round(
        discrete_divs_cy(1, 1, 25, 23, 0.05, 0.3, t, 200, np.array([]), np.array([]), 0.015))
    expected = 2.722  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE



    t = year_fraction(datetime(2023, 11, 22), datetime(2024, 2, 14))
    actual = decimal_round(
        discrete_divs_cy(1, -1, 25, 23, 0.05, 0.3, t, 200, np.array([]), np.array([]), 0.015))
    expected = 0.55  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE


    t = year_fraction(datetime(2023, 11, 22), datetime(2024, 2, 14))
    actual = decimal_round(
        discrete_divs_cy(1, 1, 25, 25, 0.05, 0.3, t, 200, np.array([]), np.array([]), 0.015))
    expected = 1.526  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE


    t = year_fraction(datetime(2023, 11, 22), datetime(2024, 2, 14))
    actual = decimal_round(
        discrete_divs_cy(1, -1, 25, 25, 0.05, 0.3, t, 200, np.array([]), np.array([]), 0.015))
    expected = 1.343  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE


    actual = decimal_round(
        discrete_divs_cy(1, 1, 25, 27, 0.05, 0.3, t, 200, np.array([]), np.array([]), 0.015))
    expected = 0.759  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE


    actual = decimal_round(
        discrete_divs_cy(1, -1, 25, 27, 0.05, 0.3,t, 200, np.array([]), np.array([]), 0.015))
    expected = 2.577  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE


    # Dividends 1
    t = year_fraction(datetime(2023, 11, 22), datetime(2024, 7, 15))
    div_times = np.array([
        div_days(datetime(2024, 2, 15)),
    ])
    div_amt = np.array([
      0.8,
    ])
    actual = decimal_round(
        discrete_divs_cy(1, 1, 25, 23, 0.05, 0.3, t, 200, div_times, div_amt, 0.015))
    expected = 3.273  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE


    t = year_fraction(datetime(2023, 11, 22), datetime(2024, 7, 15))
    div_times = np.array([
        div_days(datetime(2024, 2, 15)),
    ])
    div_amt = np.array([
      0.8,
    ])
    actual = decimal_round(
    discrete_divs_cy(1, -1, 25, 23, 0.05, 0.3, t, 200, div_times, div_amt, 0.015))
    expected = 1.506  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE


    t = year_fraction(datetime(2023, 11, 22), datetime(2024, 7, 15))
    div_times = np.array([
        div_days(datetime(2024, 2, 15)),
    ])
    div_amt = np.array([
      0.8,
    ])
    actual = decimal_round(
        discrete_divs_cy(1, 1, 25, 25, 0.05, 0.3, t, 200, div_times, div_amt, 0.015))
    expected = 2.241  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE


    t = year_fraction(datetime(2023, 11, 22), datetime(2024, 7, 15))
    div_times = np.array([
        div_days(datetime(2024, 2, 15)),
    ])
    div_amt = np.array([
      0.8,
    ])
    actual = decimal_round(
    discrete_divs_cy(1, -1, 25, 25, 0.05, 0.3, t, 200, div_times, div_amt, 0.015))
    expected = 2.502  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE


    t = year_fraction(datetime(2023, 11, 22), datetime(2024, 7, 15))
    div_times = np.array([
        div_days(datetime(2024, 2, 15)),
    ])
    div_amt = np.array([
      0.8,
    ])
    actual = decimal_round(
        discrete_divs_cy(1, 1, 25, 27, 0.05, 0.3, t, 200, div_times, div_amt, 0.015))
    expected = 1.490  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE


    t = year_fraction(datetime(2023, 11, 22), datetime(2024, 7, 15))
    div_times = np.array([
        div_days(datetime(2024, 2, 15)),
    ])
    div_amt = np.array([
      0.8,
    ])
    actual = decimal_round(
    discrete_divs_cy(1, -1, 25, 27, 0.05, 0.3, t, 200, div_times, div_amt, 0.015))
    expected = 3.764  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE


    # Dividends 2
    t = year_fraction(datetime(2023, 11, 22), datetime(2024, 12, 15))
    div_times = np.array([
        div_days(datetime(2024, 2, 15)),
        div_days(datetime(2024, 8, 15)),
    ])
    div_amt = np.array([
      0.8,
      0.8,
    ])
    actual = decimal_round(
    discrete_divs_cy(1, 1, 25, 23, 0.05, 0.3, t, 200, div_times, div_amt, 0.015))
    expected = 3.684  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE


    t = year_fraction(datetime(2023, 11, 22), datetime(2024, 12, 15))
    div_times = np.array([
        div_days(datetime(2024, 2, 15)),
        div_days(datetime(2024, 8, 15)),
    ])
    div_amt = np.array([
      0.8,
      0.8,
    ])
    actual = decimal_round(
    discrete_divs_cy(1, -1, 25, 23, 0.05, 0.3, t, 200, div_times, div_amt, 0.015))
    expected = 2.245  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE


    t = year_fraction(datetime(2023, 11, 22), datetime(2024, 12, 15))
    div_times = np.array([
        div_days(datetime(2024, 2, 15)),
        div_days(datetime(2024, 8, 15)),
    ])
    div_amt = np.array([
      0.8,
      0.8,
    ])
    actual = decimal_round(
    discrete_divs_cy(1, 1, 25, 25, 0.05, 0.3, t, 200, div_times, div_amt, 0.015))
    expected = 2.723  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE


    t = year_fraction(datetime(2023, 11, 22), datetime(2024, 12, 15))
    div_times = np.array([
        div_days(datetime(2024, 2, 15)),
        div_days(datetime(2024, 8, 15)),
    ])
    div_amt = np.array([
      0.8,
      0.8,
    ])
    actual = decimal_round(
    discrete_divs_cy(1, -1, 25, 25, 0.05, 0.3, t, 200, div_times, div_amt, 0.015))
    expected = 3.309  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE


    t = year_fraction(datetime(2023, 11, 22), datetime(2024, 12, 15))
    div_times = np.array([
        div_days(datetime(2024, 2, 15)),
        div_days(datetime(2024, 8, 15)),
    ])
    div_amt = np.array([
      0.8,
      0.8,
    ])
    actual = decimal_round(
    discrete_divs_cy(1, 1, 25, 27, 0.05, 0.3, t, 200, div_times, div_amt, 0.015))
    expected = 1.991  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE


    t = year_fraction(datetime(2023, 11, 22), datetime(2024, 12, 15))
    div_times = np.array([
        div_days(datetime(2024, 2, 15)),
        div_days(datetime(2024, 8, 15)),
    ])
    div_amt = np.array([
      0.8,
      0.8,
    ])
    actual = decimal_round(
    discrete_divs_cy(1, -1, 25, 27, 0.05, 0.3, t, 200, div_times, div_amt, 0.015))
    expected = 4.573  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE

print(timeit.timeit('test_discrete_divs_cython()', setup="from __main__ import test_discrete_divs_cython", number=1))
