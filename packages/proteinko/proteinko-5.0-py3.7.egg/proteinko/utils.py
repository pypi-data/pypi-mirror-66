import numpy as np


def pdf(x, sigma):
    """
    Calculates normal probability density function at x data points. Assumes
    mean of 0 and std provided by sigma parameter.
    :param x: data points
    :param sigma: std
    :return: np.array
    """
    y = np.exp(-x**2/(2*sigma))/(sigma*np.sqrt(2*np.pi))
    y = (y - y.min())/(y.max()-y.min())
    return y
