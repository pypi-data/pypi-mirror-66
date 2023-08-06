"""Helper functions and classes for timecast.learners"""
import abc

import flax
import jax
import numpy as onp


class FitMixin(abc.ABC):
    """Mixin class that provides a fit function for offline training / learner
    initialization"""

    @classmethod
    def fit(cls, X: onp.ndarray, Y: onp.ndarray, seed: int = 0, **kwargs) -> flax.nn.Model:
        """Fit and initialize learner on training data

        Args:
            X: input data
            Y: ground truth
            seed: random seed for jax random
            kwargs: Extra keyword arguments

        Returns:
            flax.nn.Model: initialized model
        """
        with flax.nn.stateful() as state:
            model_def = cls.partial(name=cls.__name__, **kwargs)
            _, params = model_def.init_by_shape(jax.random.PRNGKey(seed), [(1, X.shape[1])])
            model = flax.nn.Model(model_def, params)

        return model, state
