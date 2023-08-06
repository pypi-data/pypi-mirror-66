# coding: utf-8
# !/usr/bin/python

"""
Project: datascitools
Sat 18 Apr 13:08:50 2020
"""

import numpy as np

from scipy.signal import lfilter

# Author
__author__ = 'Jason Xing Zhang'
__email__ = 'jason.xing.zhang@gmail.com'


def derivative_gauss(x, chi=0.8, delta=1):
    """
    First-order derivative of Gauss function. This function is the FIR's impulse response.
        Gauss function: $$G(x) = exp(-\frac{x^2}{2\delta ^2})$$
        First-order derivative: $$G'(x) = -\frac{x}{\chi^2}exp(-\frac{x^2}{2\delta^2})$$

    Args:
        x (np.array or float): input
        chi (float): parameter to change the function shape
        delta (float): parameter to change the function shape

    Returns:
        function value
    """
    return -1.0 * x / chi**2.0 * np.exp(-1.0 * x**2 / 2.0 / delta**2.0)

def one_dim_canny(x, domain, order=21, chi=0.8):
    """
    One dimention Canny Edge Detection.

    Args:
        x (np.array): input data
        order (int): FIR filter order
        chi (int): impulse response parameter
        domain (tuple): domain

    Returns:
        jump point inside domain
    """
    if len(x) >= 3:
        order = min(order, len(x))
        order = order if order % 2 else order-1
        coefficients = derivative_gauss(np.linspace(-3, 3, order), chi)
        filtered = lfilter(coefficients, 1.0, x)
        if domain[0] >= 0 and domain[0] < len(x):
            return np.argmax(filtered[domain[0]:min(domain[1], len(x))]) + domain[0] - (order-1)/2
