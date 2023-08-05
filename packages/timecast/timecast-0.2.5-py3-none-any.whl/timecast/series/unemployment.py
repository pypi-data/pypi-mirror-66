"""timecast.series.unemployment"""
import os
from typing import Tuple

import numpy as onp

from timecast.series._core import generate_timeline


def generate() -> Tuple[onp.ndarray, onp.ndarray]:
    """
    Description: Monthly unemployment rate since 1948.

    References:
        * https://fred.stlouisfed.org/series/UNRATE
    """

    return generate_timeline(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data/unemployment.csv"),
        name="UNRATE",
    )
