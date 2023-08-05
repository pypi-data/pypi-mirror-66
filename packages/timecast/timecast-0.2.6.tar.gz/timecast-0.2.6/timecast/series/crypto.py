"""timecast.series.crypto"""
import os
from typing import Tuple

import jax.numpy as jnp
import numpy as onp
import pandas as pd


def generate(path=None) -> Tuple[onp.ndarray, onp.ndarray]:
    """
    Description: Outputs the daily price of bitcoin from 2013-04-28 to 2018-02-10
    """

    data = pd.read_csv(
        path or os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data/crypto.csv")
    )

    data = jnp.asarray(data[data.Currency == "bitcoin"].Price)

    return data[:-1], data[1:]
