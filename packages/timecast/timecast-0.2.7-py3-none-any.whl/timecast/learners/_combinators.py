"""Helper flax.nn.Modules for composing models

Todo:
    * Implement `WeightedParallel` with trainable weights
"""
from typing import List

import flax
import numpy as onp


class Sequential(flax.nn.Module):
    """Create a module from a sequential set of modules

    Notes:
        * Takes the output of the first model, passes in to the second, etc
    """

    def apply(self, x: onp.ndarray, learners: List[flax.nn.Model]):
        """
        Args:
            x (onp.ndarray): input data
            modules (List[flax.nn.module]): list of flax modules
            args (List[dict]): list of kwargs corresponding to the `modules`
                argument to initialize modules

        returns:
            onp.ndarray: result
        """
        result = x
        for learner in learners:
            result = learner(result)
        return result


class Parallel(flax.nn.Module):
    """Create a module from a sequential set of modules

    Notes:
        * Return a list of outputs from each model
    """

    def apply(self, x: onp.ndarray, learners: List[flax.nn.Model]):
        """
        Args:
            x (onp.ndarray): input data
            modules (List[flax.nn.module]): list of flax modules
            args (List[dict]): list of kwargs corresponding to the `modules`
                argument to initialize modules

        returns:
            List[onp.ndarray]: list of results
        """
        return [learner(x) for learner in learners]
