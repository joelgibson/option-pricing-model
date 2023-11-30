import timeit
import numpy as np
from datetime import datetime
from v1_option_pricing import decimal_round, discrete_divs
from v1_option_pricing_cy import discrete_divs_cy

RISK_FREE = 0.05
VOL = 0.3
STEPS = 170
DIV_YIELD = 0.015
TOLERANCE = 0.1


def test_discrete_divs_cython():

    print("====================================")
    print("Mega Long Dated Options")
    print("====================================")

    start_date = datetime(2023, 11, 30)
    end_date = datetime(2027, 11, 30)
    t = (end_date - start_date).days / 365

    div_times = np.array([
        (datetime(2023, 12, 15) - start_date).days / 365,
        (datetime(2024, 12, 15) - start_date).days / 365,
        (datetime(2025, 12, 15) - start_date).days / 365,
        # (datetime(2026, 12, 15) - start_date).days / 365,
    ])
    div_amt = np.array([
        8.0,
        8.0,
        8.0,
        # 8.0,
    ])
    actual = decimal_round(
        discrete_divs_cy(1, 1, 100, 100, 0.05, 0.4, t, 100, div_times, div_amt, 0.0))
    expected = 32.366 # Expected option price
    print("Expected:", expected, "Actual:", actual)

    actual = decimal_round(
        discrete_divs_cy(1, -1, 100, 100, 0.05, 0.4, t, 100, div_times, div_amt, 0.0))
    expected = 32.366 # Expected option price
    print("Expected:", expected, "Actual:", actual)

    print("====================================")
    print("V2 Comparison")
    print("====================================")

    t = np.float64(5/12)
    div_times = np.array([
        2.0/12,
    ], dtype=np.double)
    div_amt = np.array([
        2.0
    ], dtype=np.double)
    #(50,50,0.05,5/12,0.4,[2],[2/12],1000)
    actual = decimal_round(
        discrete_divs_cy(1, 1, 50, 50, 0.05, 0.4, t, 1000, div_times, div_amt, 0))
    expected = 4.481 # Expected option price
    print("Expected:", expected, "Actual:", actual)

    print("====================================")
    print("Weird Dividend Test")
    print("====================================")

    start_date = datetime(2023, 11, 22)
    end_date = datetime(2024, 12, 15)
    t = (end_date - start_date).days / 365


    div_times = np.array([
        (datetime(2023, 12, 15) - start_date).days / 365,
        (datetime(2024, 8, 15) - start_date).days / 365,
    ])
    div_amt = np.array([
        0.8,
        0.8,
    ])
    actual = decimal_round(
        discrete_divs_cy(1, 1, 100, 25, 0.05, 0.3, t, STEPS, div_times, div_amt, DIV_YIELD))
    expected = 75 # Expected option price
    print("Expected:", expected, "Actual:", actual)

    actual = decimal_round(
        discrete_divs_cy(1, -1, 25, 100, RISK_FREE, VOL, t, STEPS, div_times, div_amt, DIV_YIELD))
    expected = 75  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE

    # Tests against Deans calcs from Excel spreadsheet
    print("====================================")
    print("No Dividends")
    print("====================================")

    start_date = datetime(2023, 11, 22)
    end_date = datetime(2024, 2, 14)
    t = (end_date - start_date).days / 365

    # 25/23
    actual = decimal_round(
        discrete_divs_cy(1, 1, 25, 23, RISK_FREE, VOL, t, STEPS, np.array([]), np.array([]), DIV_YIELD))
    expected = 2.722  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE

    actual = decimal_round(
        discrete_divs_cy(1, -1, 25, 23, RISK_FREE, VOL, t, STEPS, np.array([]), np.array([]), DIV_YIELD))
    expected = 0.55  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE

    # 25/25
    actual = decimal_round(
        discrete_divs_cy(1, 1, 25, 25, RISK_FREE, VOL, t, STEPS, np.array([]), np.array([]), DIV_YIELD))
    expected = 1.526  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE

    actual = decimal_round(
        discrete_divs_cy(1, -1, 25, 25, RISK_FREE, VOL, t, STEPS, np.array([]), np.array([]), DIV_YIELD))
    expected = 1.343  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE

    # 25/27
    actual = decimal_round(
        discrete_divs_cy(1, 1, 25, 27, RISK_FREE, VOL, t, STEPS, np.array([]), np.array([]), DIV_YIELD))
    expected = 0.759  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE

    actual = decimal_round(
        discrete_divs_cy(1, -1, 25, 27, 0.05, 0.3,t, 200, np.array([]), np.array([]), DIV_YIELD))
    expected = 2.577  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE


    # Dividends 1
    print("====================================")
    print("One Dividend")
    print("====================================")

    start_date = datetime(2023, 11, 22)
    end_date = datetime(2024, 7, 15)
    t = (end_date - start_date).days / 365

    div_times = np.array([
        (datetime(2024, 2, 15) - start_date).days / 365,
    ])
    div_amt = np.array([
        0.8,
    ])

    # 25/23
    actual = decimal_round(
        discrete_divs_cy(1, 1, 25, 23, RISK_FREE, VOL, t, STEPS, div_times, div_amt, DIV_YIELD))
    expected = 3.273  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE

    actual = decimal_round(
        discrete_divs_cy(1, -1, 25, 23, RISK_FREE, VOL, t, STEPS, div_times, div_amt, DIV_YIELD))
    expected = 1.506  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE

    # 25/25
    actual = decimal_round(
        discrete_divs_cy(1, 1, 25, 25, RISK_FREE, VOL, t, STEPS, div_times, div_amt, DIV_YIELD))
    expected = 2.241  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE

    actual = decimal_round(
        discrete_divs_cy(1, -1, 25, 25, RISK_FREE, VOL, t, STEPS, div_times, div_amt, DIV_YIELD))
    expected = 2.502  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE

    # 25/27
    actual = decimal_round(
        discrete_divs_cy(1, 1, 25, 27, RISK_FREE, VOL, t, STEPS, div_times, div_amt, DIV_YIELD))
    expected = 1.490  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE

    actual = decimal_round(
        discrete_divs_cy(1, -1, 25, 27, RISK_FREE, VOL, t, STEPS, div_times, div_amt, DIV_YIELD))
    expected = 3.764  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE

    # Dividends 2
    print("====================================")
    print("Two Dividends")
    print("====================================")

    start_date = datetime(2023, 11, 22)
    end_date = datetime(2024, 12, 15)
    t = (end_date - start_date).days / 365

    div_times = np.array([
        (datetime(2024, 2, 15) - start_date).days / 365,
        (datetime(2024, 8, 15) - start_date).days / 365,
    ])
    div_amt = np.array([
        0.8,
        0.8,
    ])

    # 25/23
    actual = decimal_round(
        discrete_divs_cy(1, 1, 25, 23, RISK_FREE, VOL, t, STEPS, div_times, div_amt, DIV_YIELD))
    expected = 3.684  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE

    actual = decimal_round(
        discrete_divs_cy(1, -1, 25, 23, RISK_FREE, VOL, t, STEPS, div_times, div_amt, DIV_YIELD))
    expected = 2.245  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE

    # 25/25
    actual = decimal_round(
        discrete_divs_cy(1, 1, 25, 25, RISK_FREE, VOL, t, STEPS, div_times, div_amt, DIV_YIELD))
    expected = 2.723  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE

    actual = decimal_round(
        discrete_divs_cy(1, -1, 25, 25, RISK_FREE, VOL, t, STEPS, div_times, div_amt, DIV_YIELD))
    expected = 3.309  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE

    # 25/27
    actual = decimal_round(
        discrete_divs_cy(1, 1, 25, 27, RISK_FREE, VOL, t, STEPS, div_times, div_amt, DIV_YIELD))
    expected = 1.991  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE

    actual = decimal_round(
        discrete_divs_cy(1, -1, 25, 27, RISK_FREE, VOL, t, STEPS, div_times, div_amt, DIV_YIELD))
    expected = 4.573  # Expected option price
    print("Expected:", expected, "Actual:", actual)
    assert abs((actual - expected) / expected) < TOLERANCE

print(timeit.timeit('test_discrete_divs_cython()', setup="from __main__ import test_discrete_divs_cython", number=1))
