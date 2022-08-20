from enum import Enum
import numpy as np

class CI_COLORS(Enum):
    GREY_DARK   = (112, 111, 111)
    RED         = (205,  23,  25)
    YELLOW      = (255, 221,   0)
    RED_DARK    = (140,  14,  40)
    GREY        = (154, 140, 129)
    GREEN       = (  0, 160, 122)
    WHITE       = (255, 255, 255)
    BLACK       = (  0,   0,   0)
    GREY_LIGHT  = (218, 218, 218)
    BLUE        = (  0,   0, 255)

def one_if_negative(value: int) -> int:
    if value < 0: return 1

