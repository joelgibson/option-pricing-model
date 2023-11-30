#
#  https://github.com/Meraki6/Binomial-Tree-Methods-of-Pricing-American-Put-Options-with-Discrete-Dividends/blob/main/escrowed%20adj%202%20CRR%20tree.m
#
import numpy as np
from typing import List
from datetime import datetime

def binomial_tree_crr_discrete(s0: float, k: float, r: float, t: float, sigma: float, divs: List[float], divt: List[float], n: int) -> float:
    """
    Binomial Tree Model of CRR with discrete dividends.

    Parameters:
    s0 (float): Initial stock price
    k (float): Strike price
    r (float): Risk-free rate
    t (float): Time to maturity
    sigma (float): Volatility of the underlying asset
    divs (List[float]): Dividends
    divt (List[float]): Dividend times
    n (int): Number of time steps

    Returns:
    float: Option price
    """
    dt = t / n
    s0d = s0
    if divs:
        s0d -= np.sum(np.array(divs) * np.exp(-r * np.array(divt)))
    ddiv = []
    if divt:
        ddiv = np.ceil(np.array(divt) * n / t) + 1
    divn = len(divt) - 1 if divt else 0
    sigman = sigma
    if divs and divt:
        sigman = 0
        for i in range(1, divn + 1):
            before = divt[i-2] if i > 1 else 0
            sigman += (s0 * sigma / (s0 - np.sum(np.array(divs) * np.exp(-r * np.array(divt)) * (i <= ddiv))))**2 * (divt[i-1] - before)
        sigman = np.sqrt((sigman + sigma**2 * (t - divt[divn])) / t)
    u = np.exp(sigman * np.sqrt(dt))
    d = 1 / u
    p = (np.exp(r * dt) - d) / (u - d)
    discount = np.exp(-r * dt)
    s_vals = []
    for i in range(1, n + 2):
        svals = np.zeros(i)
        for j in range(1, i + 1):
            svals[j - 1] = s0d * u**(i - 1) * (d/u)**(j - 1)
            if divs and divt:
                svals[j - 1] += np.sum(np.array(divs) * np.exp(-r * dt * (ddiv - i)) * (i < ddiv))
        s_vals.append(svals)
    p_vals = [np.maximum(k - s_vals[n], 0)]
    for i in range(n, 0, -1):
        pvals = np.zeros(i)
        for j in range(1, i + 1):
            early = discount * (p * p_vals[0][j - 1] + (1 - p) * p_vals[0][j])
            internal = np.maximum(k - s_vals[i - 1][j - 1], 0)
            pvals[j - 1] = np.maximum(early, internal)
        p_vals.insert(0, pvals)
    return p_vals[0][0]


price = binomial_tree_crr_discrete(spot=50,strike=50,risk_free=0.05,time_to_exp=5/12,0.4,[2],[2/12],1000)
print(price)
