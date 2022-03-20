from chessai.utils.color import Color

from enum import Enum


class CastleFigureType(Enum):
    KING = "KING"
    ROOK_KINGSIDE = "ROOK_KINGSIDE"
    ROOK_QUEENSIDE = "ROOK_QUEENSIDE"


def get_init_coord(color, castle_figure_type):
    init_row = 1 if color == Color.WHITE else 8

    if castle_figure_type == CastleFigureType.KING:
        return (init_row, 5)
    elif castle_figure_type == CastleFigureType.ROOK_KINGSIDE:
        return (init_row, 8)
    elif castle_figure_type == CastleFigureType.ROOK_QUEENSIDE:
        return (init_row, 1)
    else:
        raise Exception(f"The type {castle_figure_type} is not a valid one")
