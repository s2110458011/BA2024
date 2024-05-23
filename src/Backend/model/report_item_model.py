from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from PIL import Image


class ReportItem():
    def __init__(self, item_number: int, fig: Figure, short_description: str,  description: str) -> None:
        self.item_number = item_number
        self.fig = fig
        self.short_description = short_description
        self.description = description
        return None
    
    def convert_figure_to_image(self) -> Image:
        canvas = FigureCanvas(self.fig)
        canvas.draw()
        img = Image.fromarray(np.asarray(canvas.buffer_rgba()))
        return img
    
    def get_description(self) -> str:
        return self.description
    
    def get_plot_image(self) -> Image:
        image = self.convert_figure_to_image()
        return image