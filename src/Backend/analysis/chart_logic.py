import pandas as pd
import numpy as np


def get_chart_options_single(data: np.array) -> list:
    if not data:
        return []
    else:
        if data.dtype == np.str_ or data.dtype == np.unicode_:
            pass