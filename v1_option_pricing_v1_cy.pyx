import numpy as np
cimport numpy as np
cimport cython

cdef extern from "math.h":
    double exp(double x)
    double pow(double base, double exponent)
    double sqrt(double x)
    double fmax(double x, double y)


# Disable bounds checking for performance
@cython.boundscheck(False)
# Function to calculate option price using binomial model
def option_binomial(
    bint model,  # 1 American, 0 European
    float flag,  # Flag to indicate whether it's a call or put option
    float S,  # Initial stock price
    float X,  # Strike price
    float r,  # Risk-free rate
    float sigma,  # Volatility
    float t,  # Time to expiration
    int steps,  # Number of steps in the binomial tree
    float div_yield  # Dividend yield
):
    """
    This function calculates the option price using a binomial model.

    Parameters:
    american
    flag (float): Flag to indicate whether it's a call or put option
    S (float): Initial stock price
    X (float): Strike price
    r (float): Risk-free rate
    sigma (float): Volatility
    t (float): Time to expiration
    steps (int): Number of steps in the binomial tree
    div_yield (float): Dividend yield

    Returns:
    float: The calculated option price
    """
    # Define local variables
    cdef int cstep
    cdef int x
    cdef int step
    cdef int i
    cdef float R = exp((r - div_yield) * (t/steps))  # Discount factor per step, adjusted for dividend yield
    cdef float Rinv = 1.0/R  # Inverse of discount factor
    cdef float u = exp(sigma * sqrt(t / steps))  # Upward movement factor
    cdef float uu = u * u  # Square of upward movement factor
    cdef float d = 1.0/u  # Downward movement factor
    cdef float p_up = (R - d) / (u - d)  # Probability of upward movement
    cdef float p_down = 1-p_up  # Probability of downward movement
    cdef np.ndarray[np.double_t, ndim=1] prices  # Array to store stock prices
    cdef np.ndarray[np.double_t, ndim=1] option_values  # Array to store option values
    prices = np.zeros(steps + 1, dtype=np.double)  # Initialize prices array
    option_values = np.zeros(steps + 1, dtype=np.double)  # Initialize option values array
    prices[0] = S * pow(d, steps)  # Calculate initial stock price
    for i in range(1, steps + 1):
        prices[i] = uu * prices[i-1]  # Calculate stock price for each step
    for i in range(steps+1):
        option_values[i] = max(0., flag * (prices[i]-X))  # Calculate option value for each step
    for step in range(steps-1, -1, -1):
        cstep = step
        for i in range(cstep+1):
            # Update option value based on binomial model
            option_values[i] = (p_up * option_values[i+1] + p_down * option_values[i])*Rinv
            prices[i] = d * prices[i+1]  # Update stock price
            # Update option value based on exercise decision
            if model:
                option_values[i] = max(option_values[i], flag*(prices[i]-X))
    return option_values[0]  # Return the option price


# Disable bounds checking for performance
@cython.boundscheck(False)
# Function to calculate option price with discrete dividends using binomial model
def discrete_divs_cy(
    bint model,  # 1 American, 2 European
    float flag,  # Flag to indicate whether it's a call or put option
    float S,  # Initial stock price
    float X,  # Strike price
    float r,  # Risk-free rate
    float sigma,  # Volatility
    float t,  # Time to expiration
    int steps,  # Number of steps in the binomial tree
    np.ndarray[np.double_t, ndim=1] div_times,  # Array of dividend times
    np.ndarray[np.double_t, ndim=1] div_amts,  # Array of dividend amounts
    float div_yield  # Dividend yield
):
    """
    This function calculates the option price with discrete dividends using a binomial model.

    Parameters:
    flag (float): Flag to indicate whether it's a call or put option
    S (float): Initial stock price
    X (float): Strike price
    r (float): Risk-free rate
    sigma (float): Volatility
    t (float): Time to expiration
    steps (int): Number of steps in the binomial tree
    div_times (np.ndarray): Array of dividend times
    div_amts (np.ndarray): Array of dividend amounts
    div_yield (float): Dividend yield

    Returns:
    float: The calculated option price
    """
    # Define local variables
    cdef int n_dividends = div_times.shape[0]
    if n_dividends == 0:
        # If no dividends, use simple binomial model
        return option_binomial(model, flag, S, X, r, sigma, t, steps, div_yield)
    cdef int steps_before = <int> (steps*(div_times[0]/t))
    if steps_before < 0:
        steps_before = 0
    if steps_before > steps:
        steps_before = steps-1
    cdef double value_alive
    cdef int cstep
    cdef int x
    cdef int step
    cdef int i
    cdef float R = exp((r - div_yield) * (t/steps))  # Discount factor per step, adjusted for dividend yield
    cdef float Rinv = 1.0/R  # Inverse of discount factor
    cdef float u = exp(sigma * sqrt(t/steps))  # Upward movement factor
    cdef float uu = u * u  # Square of upward movement factor
    cdef float d = 1.0/u  # Downward movement factor
    cdef float p_up = (R-d)/(u-d)  # Probability of upward movement
    cdef float p_down = 1-p_up  # Probability of downward movement
    cdef double dividend_amount = div_amts[0]
    cdef np.ndarray[np.double_t, ndim=1] tmp_dividend_times
    cdef np.ndarray[np.double_t, ndim=1] tmp_dividend_amts
    cdef np.ndarray[np.double_t, ndim=1] prices  # Array to store stock prices
    cdef np.ndarray[np.double_t, ndim=1] option_values  # Array to store option values
    if n_dividends > 1:
        tmp_dividend_times = np.zeros(n_dividends-1, dtype=np.double)
        tmp_dividend_amts = np.zeros(n_dividends-1, dtype=np.double)
        for i in range(0, n_dividends-1, 1):
            tmp_dividend_times[i] = div_times[i-1]
            tmp_dividend_amts[i] = div_amts[i-1]
        prices = np.zeros(steps_before+1, dtype=np.double)
        option_values = np.zeros(steps_before+1, dtype=np.double)
        prices[0]=S*pow(d, steps_before)
        for i in range(1, steps_before+1):
            prices[i] = uu * prices[i-1]
        for i in range(steps_before+1):
            value_alive = discrete_divs_cy(model, flag, prices[i]-dividend_amount, X, r, sigma, t-div_times[0], steps-steps_before, tmp_dividend_times,tmp_dividend_amts, div_yield)
            option_values[i] = max(value_alive, flag * (prices[i]-X))
        for step in range(steps_before-1, -1, -1):
            cstep = step
            for i in range(cstep+1):
                option_values[i] = (p_up * option_values[i+1] + p_down * option_values[i])*Rinv
                prices[i] = d * prices[i+1]
                if model:
                    option_values[i] = max(option_values[i], flag*(prices[i]-X))
    else:
        prices = np.zeros(steps_before+1, dtype=np.double)
        option_values = np.zeros(steps_before+1, dtype=np.double)
        prices[0]=S*pow(d, steps_before)
        for i in range(1, steps_before+1):
            prices[i] = uu * prices[i-1]
        for i in range(steps_before+1):
            value_alive = option_binomial(model, flag, prices[i]-dividend_amount, X, r, sigma, t-div_times[0], steps-steps_before, div_yield)
            option_values[i] = max(value_alive, flag * (prices[i]-X))
        for step in range(steps_before-1, -1, -1):
            cstep = step
            for i in range(cstep+1):
                option_values[i] = (p_up * option_values[i+1] + p_down * option_values[i])*Rinv
                prices[i] = d * prices[i+1]
                option_values[i] = max(option_values[i], flag*(prices[i]-X))
    return option_values[0]  # Return the option price
