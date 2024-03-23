from typing import Union

class ChartParams():

    def __init__(self, kind: str = None, 
                 title: str = None, 
                 legend: Union[bool, str] = True) -> None:
        self.kind = kind
        self.title = title
        self.legend = legend

    def set_kind(self, kind: str):
        self.kind = kind
    
    def set_title(self, title: str):
        self.title = title
    
    def set_legend(self, legend: Union[bool, str]):
        self.legend = legend

    