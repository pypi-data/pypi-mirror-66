"""flax.nn.Module for a principal component regression online learner."""
from typing import Tuple
from typing import Union

import flax
import jax
import jax.numpy as jnp
import numpy as onp

from timecast.learners._ar import _compute_kernel_bias
from timecast.learners.base import FitMixin
from timecast.utils import historify


def _compute_pca_projection(X: onp.ndarray, k: int, center=False) -> onp.ndarray:
    """Compute PCA projection"""

    if center:
        X = X - X.mean(axis=0)
        # X /= X.shape[0] - 1

    # Compute SVD
    # X: (steps - history_len + 1, history_len * input_dim) -> (H, d)
    # U: (H, H), but because full_matrices=False, (H, d)
    # S: (min(H, d),)
    # VT: (d, d)
    U, S, VT = jnp.linalg.svd(X, full_matrices=False, compute_uv=True)

    # Get index of top K eigen values
    top_k = (-jnp.square(S)).argsort()[:k]

    # Get projection
    # projection: (d, k)
    projection = VT[top_k].T

    return projection


class PCR(FitMixin, flax.nn.Module):
    """PCR online learner"""

    def apply(
        self,
        x: onp.ndarray,
        history_len: int,
        projection: onp.ndarray,
        output_features: Union[Tuple[int, ...], int] = 1,
        history: onp.ndarray = None,
    ):
        """
        Todo:
            * AR doesn't take any history
        output_features (Union[Tuple[int, ...], int]): int or tuple describing
        output shape
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
        elif not self.is_initializing():
            self.history.value = jnp.vstack((self.history.value, x))[x.shape[0] :]

        projected = self.history.value.reshape(1, -1) @ projection
        y = flax.nn.DenseGeneral(
            inputs=projected,
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

    @classmethod
    def fit(
        cls,
        X: onp.ndarray,
        Y: onp.ndarray,
        history_len: int,
        k: int = None,
        alpha: float = 0.0,
        seed: int = 0,
        name: str = "pcr",
        **kwargs
    ) -> flax.nn.Model:
        """Receives data as an iterable of tuples containing input time series,
        true time series

        Todo:
            * We assume input_dim is one-dimensional; we should flatten if not

        Notes:
            * Use (1, history_len * input_dim) vectors as features (could
            consider other representations)
            * Ignore true value (i.e., look at features only) (should we
            consider impact of features on dependent variable?)
            * We also train the underlying AR model
            * Given a time series of length N and a history of length H,
            construct N - H + 1 windows
            * Should we run PCA on input data or on windows?

        Args:
            X: input data
            Y: ground truth
            history_len: length of history to consider
            k: number of PCA components to keep. Default is min(num_histories,
            input_dim)
            alpha: Parameter to pass to ridge regression for AR fit
            seed: random seed for jax random
            name: name for the top-level module
            kwargs: Extra keyword arguments

        Returns:
            flax.nn.Model: initialized model
        """
        if not hasattr(X, "shape") or not hasattr(Y, "shape") or X.ndim == 0 or Y.ndim == 0:
            raise ValueError("Data must be ndarrays with at least 1 dimension")
        if X.shape[0] != Y.shape[0]:
            raise ValueError("Input and output data must have the same number of observations")

        # Get input/output dim
        input_dim = 1 if X.ndim == 1 else X.shape[1]
        output_dim = 1 if Y.ndim == 1 else Y.shape[1]

        # The total number of samples we will have
        num_histories = X.shape[0] - history_len + 1

        # Expand input time series X into histories, whic should result in a
        # (num_histories, history_len * input_dim)-shaped array
        history = historify(
            X, num_histories=num_histories, history_len=history_len, offset=0
        ).reshape(num_histories, -1)

        # Compute k
        k = k or min(num_histories, history_len * input_dim)

        projection = _compute_pca_projection(history, k)

        with flax.nn.stateful() as state:
            model_def = PCR.partial(
                history_len=history_len,
                projection=projection,
                output_features=output_dim,
                name=name,
            )
            _, params = model_def.init_by_shape(jax.random.PRNGKey(seed), [(1, input_dim)])
            model = flax.nn.Model(model_def, params)

        kernel, bias = _compute_kernel_bias(
            history @ projection, Y[-len(history) :], fit_intercept=True, alpha=alpha
        )

        kernel = kernel.reshape(1, k, 1)

        model.params["linear"]["kernel"] = kernel
        model.params["linear"]["bias"] = bias

        return model, state
