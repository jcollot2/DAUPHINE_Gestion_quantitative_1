from math import exp, log, sqrt
from typing import Union

import numpy as np


# Classic HESTON formulas
def compute_current_variance(
    previous_variance: np.float64,
    kappa: np.float64,
    theta: np.float64,
    xi: np.float64,
    dt: np.float64,
    dW: np.float64,
) -> np.float64:
    """Compute the current variance at time t + dt.

    Args:
    ----
        previous_variance (np.float64): Variance at time t.
        kappa (np.float64): Mean reversion speed.
        theta (np.float64): Long-run mean of variance.
        xi (np.float64): Volatility of volatility.
        dt (np.float64): Time step.
        dW (np.float64): Brownian motion step.

    Returns:
    ----
        np.float64: THe variance at time t + dt.
    """
    v = (
        np.abs(previous_variance)
        + kappa * (theta - np.abs(previous_variance)) * dt
        + xi * np.sqrt(np.abs(previous_variance)) * dW
    )
    return v


def compute_current_price(
    previous_price: np.float64,
    previous_variance: np.float64,
    mu: np.float64,
    dt: np.float64,
    dW: np.float64,
) -> np.float64:
    """The current price at time t + dt.

    Args:
    ----
        previous_price (np.float64): The price at time t.
        previous_variance (np.float64): The variance at time t.
        mu (np.float64): The drift of the price.
        dt (np.float64): The time step.
        dW (np.float64): The Brownian motion step.

    Returns:
    ----
        np.float64: The price at time t + dt.
    """
    return previous_price * (
        1
        + (mu - 0.5 * previous_variance) * dt
        + np.sqrt(np.exp(previous_variance)) * dW
    )


# FROM ARTICLE :


def compute_next_step_log_vol(
    current_step_log_vol: np.float64,
    current_step_price: np.float64,
    previous_step_price: np.float64,
    current_step_z: np.float64,
    kappa: np.float64,
    theta: np.float64,
    xi: np.float64,
    rho: np.float64,
    mu: np.float64,
    p: np.float64,
    dt: int = 1,
) -> np.float64:
    """Compute the log volatility at time t + dt.

    Args:
        current_step_log_vol (np.float64):  The log volatility at time t.
        current_step_price (np.float64): _description_
        previous_step_price (np.float64): _description_
        current_step_z (np.float64): _description_
        kappa (np.float64):  The mean reversion speed.
        theta (np.float64): The mean reversion level.
        xi (np.float64): The volatility of volatility.
        rho (np.float64): The correlation between the log volatility and the Brownian motion.
        mu (np.float64): The drift of the log price.
        p (np.float64): The power of the log volatility.
        dt (int, optional): The time step. Defaults to 1.

    Returns:
        np.float64: The log volatility at time t + dt.
    """
    current_step_vol = exp(current_step_log_vol)
    return (
        current_step_log_vol
        + (1 / current_step_vol)
        * (
            kappa * (theta - current_step_vol)
            - 0.5 * xi**2 * current_step_vol ** (2 * p - 1)
            - rho * xi * current_step_vol ** (p - 0.5) * (mu - 0.5 * current_step_vol)
        )
        * dt
        + rho
        * xi
        * current_step_vol ** (p - (3 / 2))
        * (log(current_step_price) - log(previous_step_price))
        + xi * current_step_vol ** (p - 1) * sqrt(dt) * sqrt(1 - rho) * current_step_z
    )


def compute_currrent_step_log_price(
    previous_step_log_price: np.float64,
    current_step_log_vol: np.float64,
    mu: np.float64,
    current_step_b: np.float64,
    dt: int = 1,
) -> np.float64:
    """Compute the current log price at time t.

    Args:
        previous_step_log_price (np.float64): The log price at time t - dt.
        current_step_log_vol (np.float64): The log volatility at time t.
        mu (np.float64): _description_
        current_step_b (np.float64): _description_
        dt (np.float64): The time step.

    Returns:
        np.float64: The log price at time t.
    """
    return (
        previous_step_log_price
        + (mu - 0.5 * exp(current_step_log_vol)) * dt
        + sqrt(dt) * sqrt(exp(current_step_log_vol)) * current_step_b
    )
