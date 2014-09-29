import numpy as np


def day_count(start, end):
    delta = end - start
    return delta.days


def ffill(data):
    for i in range(1, len(data)):
        if np.isnan(data[i]):
            data[i] = data[i-1]
    return data

