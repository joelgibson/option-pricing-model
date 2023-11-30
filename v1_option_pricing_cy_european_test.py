import timeit
import numpy as np
from datetime import datetime
from v1_option_pricing import decimal_round
from v1_option_pricing_cy import discrete_divs_cy

TOLERANCE = 0.05  # TOLERANCE for the difference between the actual and expected option prices

def year_fraction(start_date, end_date):
    # Function to calculate the year fraction between two dates
    days_in_year = 365.25  # considering leap years
    return (end_date - start_date).days / days_in_year


RISK_FREE = 0.05
VOL = 0.3
STEPS = 170
DIV_YIELD = 0.015
TOLERANCE = 0.05


def test_discrete_divs_cython():
    div_times_empty = np.array([])
    div_amt_empty = np.array([])

    print("====================================")
    print("Groupe One - No Dividends")
    print("====================================")

    start_date = datetime(2023, 11, 22)
    end_date = datetime(2024, 2, 14)
    t = (end_date - start_date).days / 365

    actual = decimal_round(
        discrete_divs_cy(0, 1, 25, 23, RISK_FREE, VOL, t, STEPS, div_times_empty, div_amt_empty, DIV_YIELD))
    expected = 2.721  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE


    actual = decimal_round(
        discrete_divs_cy(0, -1, 25, 23, RISK_FREE, VOL, t, STEPS, div_times_empty, div_amt_empty, DIV_YIELD))
    expected = 0.545  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE


    actual = decimal_round(
        discrete_divs_cy(0, 1, 25, 25, RISK_FREE, VOL, t, STEPS, div_times_empty, div_amt_empty, DIV_YIELD))
    expected = 1.526  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE


    actual = decimal_round(
        discrete_divs_cy(0, -1, 25, 25, RISK_FREE, VOL, t, STEPS, div_times_empty, div_amt_empty, DIV_YIELD))
    expected = 1.326  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE


    actual = decimal_round(
        discrete_divs_cy(0, 1, 25, 27, RISK_FREE, VOL, t, STEPS, div_times_empty, div_amt_empty, DIV_YIELD))
    expected = 0.758  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE


    actual = decimal_round(
        discrete_divs_cy(0, -1, 25, 27, RISK_FREE, VOL, t, STEPS, div_times_empty, div_amt_empty, DIV_YIELD))
    expected = 2.535  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE


    print("====================================")
    print("Groupe Two - No Dividends")
    print("====================================")

    start_date = datetime(2023, 11, 22)
    end_date = datetime(2024, 7, 15)
    t = (end_date - start_date).days / 365


    actual = decimal_round(
        discrete_divs_cy(0, 1, 25, 23, RISK_FREE, VOL, t, STEPS, div_times_empty, div_amt_empty, DIV_YIELD))
    expected = 3.716  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE


    actual = decimal_round(
      discrete_divs_cy(0, -1, 25, 23, RISK_FREE, VOL, t, STEPS, div_times_empty, div_amt_empty, DIV_YIELD))
    expected = 1.225  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE


    actual = decimal_round(
        discrete_divs_cy(0, 1, 25, 25, RISK_FREE, VOL, t, STEPS, div_times_empty, div_amt_empty, DIV_YIELD))
    expected = 2.638  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE


    actual = decimal_round(
      discrete_divs_cy(0, -1, 25, 25, RISK_FREE, VOL, t, STEPS, div_times_empty, div_amt_empty, DIV_YIELD))
    expected = 2.084  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE


    actual = decimal_round(
        discrete_divs_cy(0, 1, 25, 27, RISK_FREE, VOL, t, STEPS, div_times_empty, div_amt_empty, DIV_YIELD))
    expected = 1.813  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE


    actual = decimal_round(
      discrete_divs_cy(0, -1, 25, 27, RISK_FREE, VOL, t, STEPS, div_times_empty, div_amt_empty, DIV_YIELD))
    expected = 3.196  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE


    # Year fraction three
    print("====================================")
    print("Groupe Three - No Dividends")
    print("====================================")

    start_date = datetime(2023, 11, 22)
    end_date = datetime(2024, 12, 15)
    t = (end_date - start_date).days / 365

    actual = decimal_round(
      discrete_divs_cy(0, 1, 25, 23, RISK_FREE, VOL, t, STEPS, div_times_empty, div_amt_empty, DIV_YIELD))
    expected = 4.466  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE


    actual = decimal_round(
      discrete_divs_cy(0, -1, 25, 23, RISK_FREE, VOL, t, STEPS, div_times_empty, div_amt_empty, DIV_YIELD))
    expected = 1.669  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE


    actual = decimal_round(
      discrete_divs_cy(0, 1, 25, 25, RISK_FREE, VOL, t, STEPS, div_times_empty, div_amt_empty, DIV_YIELD))
    expected = 3.444  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE


    actual = decimal_round(
      discrete_divs_cy(0, -1, 25, 25, RISK_FREE, VOL, t, STEPS, div_times_empty, div_amt_empty, DIV_YIELD))
    expected = 2.543  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE


    actual = decimal_round(
      discrete_divs_cy(0, 1, 25, 27, RISK_FREE, VOL, t, STEPS, div_times_empty, div_amt_empty, DIV_YIELD))
    expected = 2.616  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE


    actual = decimal_round(
      discrete_divs_cy(0, -1, 25, 27, RISK_FREE, VOL, t, STEPS, div_times_empty, div_amt_empty, DIV_YIELD))
    expected = 3.611  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE

print(timeit.timeit('test_discrete_divs_cython()', setup="from __main__ import test_discrete_divs_cython", number=1))
