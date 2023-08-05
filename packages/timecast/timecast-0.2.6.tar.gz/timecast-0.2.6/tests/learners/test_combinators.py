"""Test combinators"""
import flax
import jax
import numpy as onp
import pytest

from timecast.learners import Ensemble
from timecast.learners import Sequential

shapes = [(4, 32), (10,), (10, 1), (1,), (1, 10)]


class Identity(flax.nn.Module):
    """Identity layer"""

    def apply(self, x: onp.ndarray):
        """
        Args:
            x (onp.ndarray): input data
        Returns:
            onp.ndarray: result
        """
        return x


class Plus(flax.nn.Module):
    """Adds constant"""

    def apply(self, x, z):
        """
        Args:
            x (onp.ndarray): input data
        Returns:
            onp.ndarray: result
        """
        return x + z


@pytest.mark.parametrize("shape", shapes)
def test_ensemble(shape):
    """Test Ensemble combinator"""
    model_def = Ensemble.partial(modules=[Identity, Identity], args=[{}, {}])
    _, params = model_def.init_by_shape(jax.random.PRNGKey(0), [shape])
    model = flax.nn.Model(model_def, params)

    X = onp.random.rand(*shape)
    ys = model(X)

    for y in ys:
        onp.testing.assert_array_almost_equal(X, y)


@pytest.mark.parametrize("shape", shapes)
def test_sequential(shape):
    """Test Sequential combinator"""
    model_def = Sequential.partial(modules=[Identity, Plus], args=[{}, {"z": 2}])
    _, params = model_def.init_by_shape(jax.random.PRNGKey(0), [shape])
    model = flax.nn.Model(model_def, params)

    X = onp.random.rand(*shape)
    ys = model(X)

    onp.testing.assert_array_almost_equal(X + 2, ys)
