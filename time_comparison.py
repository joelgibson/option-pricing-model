import timeit
import numpy as np
from datetime import datetime
from v1_american_option_pricing_v1 import decimal_round, discrete_divs

# import v1_american_option_pricing_v1_cy as opt_pricing
# def test_discrete_divs_cython():
#     opt_pricing.discrete_divs(1, 208.38, 210., .0255, .17, 47.5/252, 50, np.array([45/365.]), np.array([1.25]))

# print(timeit.timeit('test_discrete_divs_cython()', setup="from __main__ import test_discrete_divs_cython", number=1000))


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


print(timeit.timeit("test_discrete_divs()", "from __main__ import test_discrete_divs", number=1))

