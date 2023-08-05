"""flax.nn.Module for predicting a constant value

Todo:
    * Validate data and add negative tests
"""
from numbers import Real
from typing import Union

import flax
import jax.numpy as np
import numpy as onp


class PredictConstant(flax.nn.Module):
    """Constant online learner"""

    def apply(self, x: onp.ndarray, c: Union[onp.ndarray, Real] = 0):
        """
        Note:
            * Returns `c` in the shape of `x` as the prediction for the next time step

        Args:
            x (onp.ndarray): input data
            c (Real): prediction

        Returns:
            onp.ndarray: result

        Raises:
            ValueError: if `c` is not a scalar or does not match the shape of `x`
        """

        if np.isscalar(c):
            return np.ones_like(x) * c

        if c.shape != x.shape:
            raise ValueError("Constant must be scalar or match input shape")

        return c
