"""timecast.series.uci"""
import os
from typing import Tuple

import numpy as onp

from timecast.series._core import generate_timeline


def generate() -> Tuple[onp.ndarray, onp.ndarray]:
    """
    Description: Outputs various weather metrics from a UCI dataset from 13/3/2012 to 11/4/2012

    References:
        * https://archive.ics.uci.edu/ml/machine-learning-databases/00274/NEW-DATA.zip
    """

    return generate_timeline(
        path=os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data/uci.txt"),
        name="7:CO2_Habitacion_Sensor",
        delimiter=" ",
    )
