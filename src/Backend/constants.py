from enum import Enum

DESCRIPTION = 'Enter chart description here...'
DATATYPE_LIST = ['datetime', 'category', 'float', 'int']
HUE_DIMENSION = ['scatterplot', 'countplot']
TWO_DIMENSIONS = ['scatterplot', 'catplot']
THREE_DIMENSIONS = ['catplot']

class ItemType(Enum):
    HEADING = 1
    PLOT = 2
    
class InfoBoxItem(Enum):
    CURRENT_DATATYPE = 1
    COUNT_RESPONSES = 2
    NO_UNIQUE_RESPONES = 3
    
class PlotDimension(Enum):
    CAT_1 = 1
    CAT_2 = 2
    CAT_3 = 3
    CAT_4 = 4