import timeit
import numpy as np
from datetime import datetime
from v1_option_pricing import decimal_round
import v1_option_pricing_cy
import optprice

TOLERANCE = 0.05  # TOLERANCE for the difference between the actual and expected option prices

def year_fraction(start_date, end_date):
    # Function to calculate the year fraction between two dates
    days_in_year = 365.25  # considering leap years
    return (end_date - start_date).days / days_in_year


RISK_FREE = 0.05
VOL = 0.3
STEPS = 170
DIV_YIELD = 0.015
TOLERANCE = 0.01


def test_discrete_divs(fn):

    div_times_empty = np.array([])
    div_amt_empty = np.array([])

    print("====================")
    print("One - No Divs")
    print("====================")

    start_date = datetime(2023, 11, 22)
    end_date = datetime(2024, 2, 14)
    t = (end_date - start_date).days / 365

    print("Oracle vs Code")
    print("--------------------")
    # 25/23
    actual = decimal_round(
        fn(0, 1, 25, 23, RISK_FREE, VOL, t, STEPS, div_times_empty, div_amt_empty, DIV_YIELD))
    expected = 2.721  # Expected option price
    print(f"{expected:<7} {actual:<7} {abs((actual - expected) / expected) < TOLERANCE}")

    actual = decimal_round(
        fn(0, -1, 25, 23, RISK_FREE, VOL, t, STEPS, div_times_empty, div_amt_empty, DIV_YIELD))
    expected = 0.545  # Expected option price
    print(f"{expected:<7} {actual:<7} {abs((actual - expected) / expected) < TOLERANCE}")

    # 25/25
    actual = decimal_round(
        fn(0, 1, 25, 25, RISK_FREE, VOL, t, STEPS, div_times_empty, div_amt_empty, DIV_YIELD))
    expected = 1.526  # Expected option price
    print(f"{expected:<7} {actual:<7} {abs((actual - expected) / expected) < TOLERANCE}")

    actual = decimal_round(
        fn(0, -1, 25, 25, RISK_FREE, VOL, t, STEPS, div_times_empty, div_amt_empty, DIV_YIELD))
    expected = 1.326  # Expected option price
    print(f"{expected:<7} {actual:<7} {abs((actual - expected) / expected) < TOLERANCE}")

    # 25/27
    actual = decimal_round(
        fn(0, 1, 25, 27, RISK_FREE, VOL, t, STEPS, div_times_empty, div_amt_empty, DIV_YIELD))
    expected = 0.758  # Expected option price
    print(f"{expected:<7} {actual:<7} {abs((actual - expected) / expected) < TOLERANCE}")

    actual = decimal_round(
        fn(0, -1, 25, 27, RISK_FREE, VOL, t, STEPS, div_times_empty, div_amt_empty, DIV_YIELD))
    expected = 2.535  # Expected option price
    print(f"{expected:<7} {actual:<7} {abs((actual - expected) / expected) < TOLERANCE}")

    print("====================")
    print("Two - No Divs")
    print("====================")

    start_date = datetime(2023, 11, 22)
    end_date = datetime(2024, 7, 15)
    t = (end_date - start_date).days / 365

    print("Oracle vs Code")
    print("--------------------")
    # 25/23
    actual = decimal_round(
        fn(0, 1, 25, 23, RISK_FREE, VOL, t, STEPS, div_times_empty, div_amt_empty, DIV_YIELD))
    expected = 3.716  # Expected option price
    print(f"{expected:<7} {actual:<7} {abs((actual - expected) / expected) < TOLERANCE}")

    actual = decimal_round(
      fn(0, -1, 25, 23, RISK_FREE, VOL, t, STEPS, div_times_empty, div_amt_empty, DIV_YIELD))
    expected = 1.225  # Expected option price
    print(f"{expected:<7} {actual:<7} {abs((actual - expected) / expected) < TOLERANCE}")

    # 25/25
    actual = decimal_round(
        fn(0, 1, 25, 25, RISK_FREE, VOL, t, STEPS, div_times_empty, div_amt_empty, DIV_YIELD))
    expected = 2.638  # Expected option price
    print(f"{expected:<7} {actual:<7} {abs((actual - expected) / expected) < TOLERANCE}")

    actual = decimal_round(
      fn(0, -1, 25, 25, RISK_FREE, VOL, t, STEPS, div_times_empty, div_amt_empty, DIV_YIELD))
    expected = 2.084  # Expected option price
    print(f"{expected:<7} {actual:<7} {abs((actual - expected) / expected) < TOLERANCE}")

    # 25/27
    actual = decimal_round(
        fn(0, 1, 25, 27, RISK_FREE, VOL, t, STEPS, div_times_empty, div_amt_empty, DIV_YIELD))
    expected = 1.813  # Expected option price
    print(f"{expected:<7} {actual:<7} {abs((actual - expected) / expected) < TOLERANCE}")

    actual = decimal_round(
      fn(0, -1, 25, 27, RISK_FREE, VOL, t, STEPS, div_times_empty, div_amt_empty, DIV_YIELD))
    expected = 3.196  # Expected option price
    print(f"{expected:<7} {actual:<7} {abs((actual - expected) / expected) < TOLERANCE}")

    # Year fraction three
    print("====================")
    print("Three - No Divs")
    print("====================")

    start_date = datetime(2023, 11, 22)
    end_date = datetime(2024, 12, 15)
    t = (end_date - start_date).days / 365

    print("Oracle vs Code")
    print("--------------------")
    # 25/23
    actual = decimal_round(
      fn(0, 1, 25, 23, RISK_FREE, VOL, t, STEPS, div_times_empty, div_amt_empty, DIV_YIELD))
    expected = 4.466  # Expected option price
    print(f"{expected:<7} {actual:<7} {abs((actual - expected) / expected) < TOLERANCE}")

    actual = decimal_round(
      fn(0, -1, 25, 23, RISK_FREE, VOL, t, STEPS, div_times_empty, div_amt_empty, DIV_YIELD))
    expected = 1.669  # Expected option price
    print(f"{expected:<7} {actual:<7} {abs((actual - expected) / expected) < TOLERANCE}")

    # 25/25
    actual = decimal_round(
      fn(0, 1, 25, 25, RISK_FREE, VOL, t, STEPS, div_times_empty, div_amt_empty, DIV_YIELD))
    expected = 3.444  # Expected option price
    print(f"{expected:<7} {actual:<7} {abs((actual - expected) / expected) < TOLERANCE}")

    actual = decimal_round(
      fn(0, -1, 25, 25, RISK_FREE, VOL, t, STEPS, div_times_empty, div_amt_empty, DIV_YIELD))
    expected = 2.543  # Expected option price
    print(f"{expected:<7} {actual:<7} {abs((actual - expected) / expected) < TOLERANCE}")

    # 25/27
    actual = decimal_round(
      fn(0, 1, 25, 27, RISK_FREE, VOL, t, STEPS, div_times_empty, div_amt_empty, DIV_YIELD))
    expected = 2.616  # Expected option price
    print(f"{expected:<7} {actual:<7} {abs((actual - expected) / expected) < TOLERANCE}")

    actual = decimal_round(
      fn(0, -1, 25, 27, RISK_FREE, VOL, t, STEPS, div_times_empty, div_amt_empty, DIV_YIELD))
    expected = 3.611  # Expected option price
    print(f"{expected:<7} {actual:<7} {abs((actual - expected) / expected) < TOLERANCE}")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('algo', choices=['cy', 'optprice'])
    args = parser.parse_args()

    print(f"Using algo {args.algo}")
    if args.algo == 'cy':
        test_discrete_divs(v1_option_pricing_cy.discrete_divs_cy)
    elif args.algo == 'optprice':
        test_discrete_divs(optprice.discrete_divs_cy)