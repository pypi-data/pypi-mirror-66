"""flax.nn.Module for predicting last value

Todo:
    * Implement last value n steps ago (requires state)
"""
import flax
import numpy as onp


class PredictLast(flax.nn.Module):
    """Identity online learner"""

    def apply(self, x: onp.ndarray):
        """
        Note:
            * Returns `x` as the prediction for the next time step

        Args:
            x (onp.ndarray): input data

        Returns:
            onp.ndarray: result
        """

        return x
