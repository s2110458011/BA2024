from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from PIL import Image


class ReportItem():
    def __init__(self, item_number: int, fig: Figure, description: str) -> None:
        self.item_number = item_number
        self.fig = fig
        self.description = description
        return None
    
    def convert_figure_to_image(self) -> None:
        canvas = FigureCanvas(self.fig)
        canvas.draw()
        self.img = Image.fromarray(np.asarray(canvas.buffer_rgba()))
        return None