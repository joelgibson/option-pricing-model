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

    # Year fraction one
    t = year_fraction(datetime(2023, 11, 22), datetime(2024, 2, 14))

    actual = decimal_round(
        discrete_divs_cy(0, 1, 25, 23, 0.05, 0.3, t, 200, np.array([]), np.array([]), 0.015))
    expected = 2.721  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE


    actual = decimal_round(
        discrete_divs_cy(0, -1, 25, 23, 0.05, 0.3, t, 200, np.array([]), np.array([]), 0.015))
    expected = 0.545  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE


    actual = decimal_round(
        discrete_divs_cy(0, 1, 25, 25, 0.05, 0.3, t, 200, np.array([]), np.array([]), 0.015))
    expected = 1.526  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE


    actual = decimal_round(
        discrete_divs_cy(0, -1, 25, 25, 0.05, 0.3, t, 200, np.array([]), np.array([]), 0.015))
    expected = 1.326  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE


    actual = decimal_round(
        discrete_divs_cy(0, 1, 25, 27, 0.05, 0.3, t, 200, np.array([]), np.array([]), 0.015))
    expected = 0.758  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE


    actual = decimal_round(
        discrete_divs_cy(0, -1, 25, 27, 0.05, 0.3, t, 200, np.array([]), np.array([]), 0.015))
    expected = 2.535  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE

    # Year fraction two
    t = year_fraction(datetime(2023, 11, 22), datetime(2024, 7, 15))

    actual = decimal_round(
        discrete_divs_cy(0, 1, 25, 23, 0.05, 0.3, t, 200, np.array([]), np.array([]), 0.015))
    expected = 3.716  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE


    actual = decimal_round(
      discrete_divs_cy(0, -1, 25, 23, 0.05, 0.3, t, 200, np.array([]), np.array([]), 0.015))
    expected = 1.225  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE


    actual = decimal_round(
        discrete_divs_cy(0, 1, 25, 25, 0.05, 0.3, t, 200, np.array([]), np.array([]), 0.015))
    expected = 2.638  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE


    actual = decimal_round(
      discrete_divs_cy(0, -1, 25, 25, 0.05, 0.3, t, 200, np.array([]), np.array([]), 0.015))
    expected = 2.084  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE


    actual = decimal_round(
        discrete_divs_cy(0, 1, 25, 27, 0.05, 0.3, t, 200, np.array([]), np.array([]), 0.015))
    expected = 1.813  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE


    actual = decimal_round(
      discrete_divs_cy(0, -1, 25, 27, 0.05, 0.3, t, 200, np.array([]), np.array([]), 0.015))
    expected = 3.196  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE


    # Year fraction three

    t = year_fraction(datetime(2023, 11, 22), datetime(2024, 12, 15))

    actual = decimal_round(
      discrete_divs_cy(0, 1, 25, 23, 0.05, 0.3, t, 200, np.array([]), np.array([]), 0.015))
    expected = 4.466  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE


    actual = decimal_round(
      discrete_divs_cy(0, -1, 25, 23, 0.05, 0.3, t, 200, np.array([]), np.array([]), 0.015))
    expected = 1.669  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE


    actual = decimal_round(
      discrete_divs_cy(0, 1, 25, 25, 0.05, 0.3, t, 200, np.array([]), np.array([]), 0.015))
    expected = 3.444  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE


    actual = decimal_round(
      discrete_divs_cy(0, -1, 25, 25, 0.05, 0.3, t, 200, np.array([]), np.array([]), 0.015))
    expected = 2.543  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE


    actual = decimal_round(
      discrete_divs_cy(0, 1, 25, 27, 0.05, 0.3, t, 200, np.array([]), np.array([]), 0.015))
    expected = 2.616  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE


    actual = decimal_round(
      discrete_divs_cy(0, -1, 25, 27, 0.05, 0.3, t, 200, np.array([]), np.array([]), 0.015))
    expected = 3.611  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE

print(timeit.timeit('test_discrete_divs_cython()', setup="from __main__ import test_discrete_divs_cython", number=1))
