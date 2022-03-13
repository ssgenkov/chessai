from enum import Enum


class Move(Enum):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    LU_DIAG = "LU_DIAG"
    RU_DIAG = "RU_DIAG"
    LD_DIAG = "LD_DIAG"
    RD_DIAG = "RD_DIAG"
