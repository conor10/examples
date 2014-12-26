from matplotlib.pyplot import figure, legend, plot, show
import pandas as pd
import seaborn

import volatility as vm


def main():
    data = pd.read_csv('AAPL.csv', index_col=0, parse_dates=True)
    data.sort_index(inplace=True)
    # There was a stock split on 9th June 2014, so we work prior to this date
    # as we're using non-adjusted data
    data = data[-1000:-100]

    # We don't use the adjusted close in this example, as the Parkinson
    # model uses high and low prices which are not adjusted
    std_dev = vm.population_std_dev(data['Close'], 20)
    parkinson_vol = vm.parkinson_std_dev(data['High'], data['Low'], 20)

    fig = figure()
    fig.add_subplot(2, 1, 1)
    plot(data['High'], label='High')
    plot(data['Low'], label='Low')
    plot(data['Close'], label='Close')
    legend()

    fig.add_subplot(2, 1, 2)
    plot(std_dev, label='Close to close')
    plot(parkinson_vol, label='Parkinson')
    legend()

    show()


if __name__ == '__main__':
    main()