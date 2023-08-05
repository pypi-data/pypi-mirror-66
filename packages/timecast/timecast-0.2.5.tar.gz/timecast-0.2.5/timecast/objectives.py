"""Objective functions for composing loss functions for multiple learners"""
from functools import partial
from typing import Callable
from typing import Tuple
from typing import Union

import flax
import jax
import numpy as onp


def smap(
    X: Union[onp.ndarray, Tuple[onp.ndarray, ...]],
    Y: Union[onp.ndarray, Tuple[onp.ndarray, ...]],
    optimizer: flax.optim.Optimizer,
    state: flax.nn.base.Collection,
    objective: Callable[
        [
            onp.ndarray,
            onp.ndarray,
            Callable[[onp.ndarray, onp.ndarray], onp.ndarray],
            flax.nn.base.Model,
        ],
        Tuple[onp.ndarray, onp.ndarray],
    ],
    loss_fn: Callable[[onp.ndarray, onp.ndarray], onp.ndarray],
):
    """Take gradients steps performantly on one data item at a time

    Args:
        X: onp.ndarray or tuple of onp.ndarray of inputs
        Y: onp.ndarray or tuple of onp.ndarray of outputs
        optimizer: initialized optimizer
        state: state required by flax
        objective: function composing loss functions
        loss_fn: loss function to compose

    Returns:
        onp.ndarray: result
    """

    def _smap(optstate, xy):
        """Helper function"""
        x, y = xy
        optimizer, state = optstate
        with flax.nn.stateful(state) as state:
            loss, y_hat, grad = optimizer.compute_gradients(partial(objective, x, y, loss_fn))
            return (optimizer.apply_gradient(grad), state), y_hat

    _, pred = jax.lax.scan(_smap, (optimizer, state), (X, Y))
    return pred


def residual(x, y, loss_fn, model):
    """List of learners where each learner trains on the residual of the previous"""
    y_hats = model(x)
    target, y_hat, loss = y, y_hats[0], 0
    for i in range(len(y_hats) - 1):
        loss += loss_fn(target - y_hats[i], y_hats[i + 1])
        target -= y_hats[i]
        y_hat += y_hats[i + 1]
    return loss, y_hat


def xboost(x, y, loss_fn, model, reg=1.0):
    """List of learners governed by xboost

    Notes:
        * See: https://arxiv.org/pdf/1906.08720.pdf
    """
    y_hats = model(x)
    g = jax.grad(loss_fn)
    u, loss = 0, 0
    for i in range(len(y_hats)):
        eta = 2 / (i + 2)
        loss += g(y, u) * y_hats[i] + (reg / 2) * y_hats[i] * y_hats[i]
        u = (1 - eta) * u + eta * y_hats[i]
    return loss.reshape(()), u
