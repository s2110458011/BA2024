from enum import Enum

DESCRIPTION = 'Enter chart description here...'
DATATYPE_LIST = ['datetime', 'category', 'float', 'int']
TWO_DIMENSIONS = ['scatterplot', 'countplot']
THREE_DIMENSIONS = ['catplot']

class ItemType(Enum):
    HEADING = 1
    PLOT = 2
    
class InfoBoxItem(Enum):
    CURRENT_DATATYPE = 1
    COUNT_RESPONSES = 2
    NO_UNIQUE_RESPONES = 3
