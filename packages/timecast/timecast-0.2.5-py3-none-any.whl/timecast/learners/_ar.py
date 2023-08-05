"""flax.nn.Module for an auto-regressive online learner.

Todo:
    * Implement offline `fit` class method for closed-form, out of core training
    * Implement strided history
    * Add link functions for GLM
    * Add checks on data and corresponding negative tests
"""
from typing import Tuple
from typing import Union

import flax
import jax.numpy as jnp
import numpy as onp


class AR(flax.nn.Module):
    """AR online learner"""

    def apply(
        self,
        x: onp.ndarray,
        output_features: Union[Tuple[int, ...], int],
        history_len: int,
        history: onp.ndarray = None,
    ):
        """
        Note:
            * We expect that `x` is one- or two-dimensional
            * We reshape `x` to ensure its first axis is time and its second
              axis is input_features

        Args:
            x (onp.ndarray): input data
            output_features (Union[Tuple[int, ...], int]): int or tuple
                describing output shape
            history_len (int): length of AR history length
            history (onp.ndarray, optional): Defaults to None. Optional initialization
                for history

        Returns:
            onp.ndarray: result
        """

        if x.ndim == 1:
            x = x.reshape(1, -1)

        if history is not None and history.shape == x.shape:
            x = history

        self.history = self.state(
            "history", shape=(history_len, x.shape[1]), initializer=flax.nn.initializers.zeros
        )

        if self.is_initializing() and history is not None:
            self.history.value = jnp.vstack((self.history.value, history))[history.shape[0] :]
        else:
            self.history.value = jnp.vstack((self.history.value, x))[x.shape[0] :]

        y = flax.nn.DenseGeneral(
            inputs=self.history.value,
            features=output_features,
            axis=(0, 1),
            batch_dims=(),
            bias=True,
            dtype=jnp.float32,
            kernel_init=flax.nn.initializers.zeros,
            bias_init=flax.nn.initializers.zeros,
            precision=None,
            name="linear",
        )
        return y
