import numpy as np


DAYS_PER_YEAR = 252.0


def generate_gbm_prices(periods, start_price, mu, sigma, delta):
    t = delta / DAYS_PER_YEAR
    prices = np.zeros(periods)
    epsilon_sigma_t = np.random.normal(0, 1, periods-1) * sigma * np.sqrt(t)
    prices[0] = start_price
    for i in range(1, len(prices)):
        prices[i] = prices[i-1] * \
                    np.exp((mu - 0.5 * sigma**2) * t +
                           epsilon_sigma_t[i-1])
    return prices


def lag(data, empty_term=0.):
    lagged = np.roll(data, 1)
    lagged[0] = empty_term
    return lagged


def calculate_returns(prices):
    lagged_pnl = lag(prices)
    returns = (prices - lagged_pnl) / lagged_pnl

    # All values prior to our position opening in pnl will have a
    # value of inf. This is due to division by 0.0
    returns[np.isinf(returns)] = 0.
    # Additionally, any values of 0 / 0 will produce NaN
    returns[np.isnan(returns)] = 0.
    return returns


def calculate_max_drawdown(returns):
    size = len(returns)
    highwatermark = np.zeros(size)
    drawdown = np.zeros(size)
    dd_duration = np.zeros(size, dtype=int)

    for i in range(1, size):
        highwatermark[i] = max(highwatermark[i-1], returns[i])
        drawdown[i] = ((1.0 + returns[i]) / (1.0 + highwatermark[i])) - 1.0
        if drawdown[i] == 0.:
            dd_duration[i] = 0
        else:
            dd_duration[i] = dd_duration[i-1] + 1

    min_dd_idx = drawdown.argmin()
    return min(drawdown), max(dd_duration), \
           min_dd_idx, dd_duration.argmax(), \
           np.where(returns == highwatermark[min_dd_idx-1])[-1]
