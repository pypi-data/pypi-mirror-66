"""Helper flax.nn.Modules for composing models

Todo:
    * Implement `WeightedEnsemble` with trainable weights
"""
from typing import List

import flax
import numpy as onp


class Sequential(flax.nn.Module):
    """Create a module from a sequential set of modules

    Notes:
        * Takes the output of the first model, passes in to the second, etc
    """

    def apply(self, x: onp.ndarray, modules: List[flax.nn.Module], args: List[dict]):
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
        for module, arg in zip(modules, args):
            result = module(result, **arg)
        return result


class Ensemble(flax.nn.Module):
    """Create a module from a sequential set of modules

    Notes:
        * Return a list of outputs from each model
    """

    def apply(self, x: onp.ndarray, modules: List[flax.nn.Module], args: List[dict]):
        """
        Args:
            x (onp.ndarray): input data
            modules (List[flax.nn.module]): list of flax modules
            args (List[dict]): list of kwargs corresponding to the `modules`
                argument to initialize modules

        returns:
            List[onp.ndarray]: list of results
        """
        return [module(x, **arg) for (module, arg) in zip(modules, args)]
