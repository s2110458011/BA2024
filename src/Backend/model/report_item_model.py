from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import numpy as np
from PIL import Image

class ReportItem():
    def __init__(self, item_number: int, img: Image, short_description: str,  description: str) -> None:
        self.item_number = item_number
        self.fig = img
        self.short_description = short_description
        self.description = description
        return None
    
    def convert_figure_to_image(self) -> Image:
        canvas = FigureCanvas(self.fig)
        canvas.draw()
        img = Image.fromarray(np.asarray(canvas.buffer_rgba()))
        print(img)
        return img
    
    def get_description(self) -> str:
        return self.description
    
    def get_image(self) -> Image:
        return self.fig