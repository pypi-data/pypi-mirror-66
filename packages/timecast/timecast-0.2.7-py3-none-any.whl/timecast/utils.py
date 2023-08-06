"""Utility functions"""
import jax.numpy as jnp
import numpy as onp


def historify(X: onp.ndarray, num_histories: int, history_len: int, offset: int = 0):
    """Generate (num_histories, history_len, feature_dim) history from time series data

    Todo:
        * Implement striding

    Args:
        X: 2D array of features organized as (time, feature_dim)
        num_histories: number of history windows to create
        history_len: length of a history window
        offset: how many time steps to offset

    Returns:
        onp.ndarray: 3D array organized as (num_histories, history_len,
        feature_dim)
    """
    if num_histories < 1 or history_len < 1:
        raise ValueError("Must have positive history_len and at least one window")
    if X.shape[0] < offset + num_histories + history_len - 1:
        raise ValueError(
            "Not enough history ({}) to produce {} windows of length {} with offset {}".format(
                X.shape[0], num_histories, history_len, offset
            )
        )
    return jnp.swapaxes(
        jnp.stack([jnp.roll(X, shift=-(i + offset), axis=0) for i in range(history_len)]), 0, 1
    )[:num_histories]
