import math

import numba


def n_pdf(x: float) -> float:
    """Density function of the standard normal."""
    return (2 * math.pi)**-0.5 * math.exp(-x**2 / 2)


def n_cdf(x: float) -> float:
    """Distribution function of the standard normal."""
    return 0.5 + 0.5 * math.erf(x / 2**0.5)


def black_scholes(
    pc_flag: float,        # +1 for call, -1 for put.
    spot: float,           # Spot price of the underlying stock.
    strike: float,         # Strike price of the option.
    ivol: float,           # Implied volatility (annualised).
    tau: float,            # Time to expiry (years).
    rate: float = 0,       # Risk-free rate (annualised, continuously compounding).
    div_yield: float = 0,  # Dividend yield (annualised, continuously compounding).
) -> float:
    """
    Black-Scholes-Merton formula for valuing a European option on a stock, with
    a continuously compounding risk-free rate and dividend yield.
    """

    # First take the forward price of the stock, inflated by the risk-free rate and
    # depreciated by the dividend yield.
    fwd = spot * math.exp((rate - div_yield) * tau)

    # Now use the standard Black formula for the undiscounted value of the option
    # at maturity.
    x = math.log(fwd / strike)      # Negative log-moneyness.
    v = ivol * tau**0.5             # Time-scaled volatility.
    price_undiscounted = pc_flag * (
        fwd * n_cdf(pc_flag * (x / v + v / 2))
        - strike * n_cdf(pc_flag * (x / v - v / 2))
    )

    # Finally, discount the value at maturity by the risk-free rate.
    return math.exp(-rate * tau) * price_undiscounted


def binomial_tree(
    model: str,            # 'A' for American, 'E' for European.
    pc_flag: float,        # +1 for call, -1 for put.
    spot: float,           # Spot price of the underlying stock.
    strike: float,         # Strike price of the option.
    ivol: float,           # Implied volatility (annualised).
    tau: float,            # Time to expiry (years).
    rate: float = 0,       # Risk-free rate (annualised, continuously compounding).
    div_yield: float = 0,  # Dividend yield (annualised, continuously compounding).
    steps: int = 1000,     # Number of steps in the tree, eg [0, 1, ..., 100].
):
    """
    Binomial tree approximation for valuing an American or European option on a stock,
    with a continuously compounding risk-free rate and dividend yield.
    """
    assert model in 'AE'
    assert steps >= 1

    # Set up the binomial tree parameters. Here we will not build the dividend yields
    # into the risk-neutral measure, but treat them as affecting the prices of the tree.
    Δt = tau / steps              # Time step.
    u = math.exp(ivol * Δt**0.5)  # Up factor.
    d = 1 / u                     # Down factor.
    R = math.exp(rate * Δt)       # Risk-free rate on a step.
    Y = math.exp(div_yield * Δt)  # Dividend yield on a step.
    pu = (R - d) / (u - d)        # Risk-neutral up probability.
    pd = 1 - pu                   # Risk-neutral down probability.

    # Spot prices of the underlying at the maximum timestep.
    # The lowest index is the lowest price.
    sprices = [spot * u**i * d**(steps - i) / Y**steps for i in range(steps + 1)]

    # Option payoffs at the maximum timestep.
    oprices = [max(0, pc_flag * (sprice - strike)) for sprice in sprices]

    # Now for each timestep working backwards, take the discounted expectation
    # under the risk-neutral measure.
    for t in range(steps - 1, -1, -1):
        sprices = [sprice * u * Y for sprice in sprices[:-1]]
        oprices = [
            (oprices[i] * pd + oprices[i+1] * pu) / R
            for i in range(len(oprices) - 1)
        ]
        if model == 'A':
            oprices = [
                max(oprice, pc_flag * (sprice - strike))
                for sprice, oprice in zip(sprices, oprices)
            ]
    
    assert len(sprices) == len(oprices) == 1
    assert abs(sprices[0] - spot) < 1e-10

    return oprices[0]


@numba.njit
def discrete_divs(
    model: str,                   # 'A' for American, 'E' for European.
    pc_flag: float,               # +1 for call, -1 for put.
    spot: float,                  # Spot price of the underlying stock.
    strike: float,                # Strike price of the option.
    ivol: float,                  # Implied volatility (annualised).
    tau: float,                   # Time to expiry (years).
    rate: float = 0,              # Risk-free rate (annualised, continuously compounding).
    div_yield: float = 0,         # Dividend yield (annualised, continuously compounding).
    div_times: list[float] = [],  # Times to distribute dividends (years)
    div_amts: list[float] = [],   # Amounts to distribute.
    steps: int = 1000,            # Number of steps in the tree, eg [0, 1, ..., 100].
):
    """
    Binomial tree approximation for valuing an American or European option on a stock,
    with a continuously compounding risk-free rate and dividend yield. Additionally,
    discrete dividends at points in time may be specified: these are converted into
    percentage returns on the dividend-discounted price of the stock at that time.
    """
    assert model in 'AE'
    assert len(div_times) == len(div_amts)
    assert steps >= 1

    # Set up the binomial tree parameters. Here we will not build the dividend yields
    # into the risk-neutral measure, but treat them as affecting the prices of the tree.
    Δt = tau / steps              # Time step.
    u = math.exp(ivol * Δt**0.5)  # Up factor.
    d = 1 / u                     # Down factor.
    R = math.exp(rate * Δt)       # Risk-free rate on a step.
    Y = math.exp(div_yield * Δt)  # Dividend yield on a step.
    pu = (R - d) / (u - d)        # Risk-neutral up probability.
    pd = 1 - pu                   # Risk-neutral down probability.

    # Set up the discrete dividends.
    # We treat discrete dividends as percentage returns, converting a dollar amount to
    # a percentage return using the forward price of the stock, i.e. inflating by the
    # time-scaled (rate - div_yield).
    #
    # Distribute the discrete dividends into time buckets, where divs[t] is the dividend
    # yield (including both discrete and continuous) from timestep t to t+1.
    divs = [Y for i in range(steps)]
    for time, amt in zip(div_times, div_amts):
        # Bucket the discrete dividend, reject if it is outside our time range.
        t = round(time / Δt)
        if not (0 <= t < steps):
            continue

        # Calculate the cumulative dividend so far, so that we can discount the spot.
        div_sofar = 1.0
        for i in range(t):
            div_sofar *= divs[i]
        
        # Insert the discrete dividend, as a percentage on the dividend-discounted spot.
        divs[t] *= 1 + amt / (spot / div_sofar)

    # Need to know our total dividend to set up the final prices in the tree.
    total_div = 1.0
    for div in divs:
        total_div *= div
    
    # Spot prices of the underlying at the maximum timestep.
    # The lowest index is the lowest price.
    sprices = [
        spot * u**t * d**(steps - t) / total_div
        for t in range(steps + 1)
    ]

    # Option payoffs at the maximum timestep.
    oprices = [max(0, pc_flag * (sprice - strike)) for sprice in sprices]

    # Now for each timestep working backwards, take the discounted expectation
    # under the risk-neutral measure.
    for t in range(steps-1, -1, -1):
        sprices = [sprice * u * divs[t] for sprice in sprices[:-1]]
        oprices = [
            (oprices[i] * pd + oprices[i+1] * pu) / R
            for i in range(len(oprices) - 1)
        ]
        if model == 'A':
            oprices = [
                max(oprice, pc_flag * (sprice - strike))
                for sprice, oprice in zip(sprices, oprices)
            ]
    
    # Did we loop the right number of times?
    assert len(sprices) == len(oprices) == 1

    # Catch any errors in our pricing tree: the 0th price should just be
    # equal to the spot.
    assert abs(sprices[0] - spot) < 1e-4

    return oprices[0]


# Wrapper function so I can replace discrete_divs_cy with my thing.
def discrete_divs_cy(
    model: int,  # 1 for American, 2 (should this be 0?) for European
    pc_flag: float,  # Flag to indicate whether it's a call or put option (+1 call, -1 put).
    spot: float,  # Initial stock price
    strike: float,  # Strike price
    rate: float,  # Risk-free rate (annualised, compounding?)
    ivol: float,  # Volatility (annualised)
    tau: float,  # Time to expiration (years)
    steps: int,  # Number of steps in the binomial tree
    div_times: list[float],  # Array of dividend times
    div_amts: list[float],  # Array of dividend amounts
    div_yield: float,  # Dividend yield
):
    return discrete_divs(
        model='A' if model else 'E',
        pc_flag=pc_flag,
        spot=spot,
        strike=strike,
        rate=rate,
        ivol=ivol,
        tau=tau,
        steps=steps,
        div_times=div_times,
        div_amts=div_amts,
        div_yield=div_yield,
    )
    

if __name__ == '__main__':
    print(black_scholes(pc_flag=1, spot=100, strike=95, ivol=0.2, tau=0.5, rate=0.01, div_yield=0.10))
    print(binomial_tree('E', pc_flag=1, spot=100, strike=95, ivol=0.2, tau=0.5, rate=0.01, div_yield=0.10))
    print(binomial_tree('A', pc_flag=1, spot=100, strike=95, ivol=0.2, tau=0.5, rate=0.01, div_yield=0.10))