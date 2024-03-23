import pandas as pd
import matplotlib.pyplot as plt

from chart_data import ChartData

"""Script for visualizing charts.
"""

def create_chart(data: pd.DataFrame, params: ChartData):
    data.plot(kind=params.kind)
    plt.show()


