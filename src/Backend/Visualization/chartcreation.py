import pandas as pd
import matplotlib.pyplot as plt

from backend.visualization.chartparameter import ChartParams

"""Script for visualizing charts.
"""

def create_chart(data: pd.DataFrame, params: ChartParams):
    data.plot(kind=params.kind)
    plt.show()


