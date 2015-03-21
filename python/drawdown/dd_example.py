import matplotlib.pyplot as plt
import numpy as np
import seaborn

import utils


np.random.seed(3)


def main():

    prices = utils.generate_gbm_prices(500, 70.0, 0.05, 0.3, 1.0)
    returns = (utils.calculate_returns(prices) + 1.0).cumprod()

    max_dd, max_count, max_dd_idx, max_duration_idx, hwm_idx = \
        utils.calculate_max_drawdown(returns - 1.0)

    plt.plot(returns)

    plt.plot((hwm_idx, max_dd_idx),
             (returns[hwm_idx], returns[max_dd_idx]), color='black')
    plt.annotate('max dd ({0:.2f}%)'.format(max_dd * 100.0),
                 xy=(max_dd_idx, returns[max_dd_idx]),
                 xycoords='data', xytext=(0, -50),
                 textcoords='offset points',
                 arrowprops=dict(facecolor='black', shrink=0.05))

    max_duration_start_idx = max_duration_idx - max_count
    max_duration_x1x2 = (max_duration_start_idx, max_duration_idx)
    max_duration_y1y2 = (returns[max_duration_start_idx],
                         returns[max_duration_start_idx])

    plt.plot(max_duration_x1x2, max_duration_y1y2, color='black')
    plt.annotate('max dd duration ({} days)'.format(max_count),
                 xy=((max_duration_start_idx + max_duration_idx) / 2,
                     returns[max_duration_start_idx]),
                 xycoords='data',
                 xytext=(-100, 30), textcoords='offset points',
                 arrowprops=dict(facecolor='black', shrink=0.05))

    plt.show()


if __name__ == '__main__':
    main()