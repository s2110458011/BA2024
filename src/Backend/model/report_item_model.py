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
    
    def get_description(self) -> str:
        return self.description
    
    def get_image(self) -> Image:
        return self.fig