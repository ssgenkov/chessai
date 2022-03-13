from chessai.figures.bishop import Bishop
from chessai.figures.pawn import Pawn
from chessai.figures.knight import Knight
from chessai.figures.king import King
from chessai.figures.rook import Rook
from chessai.figures.queen import Queen
from chessai.figures.figure_type import FigureType


def get_figure(color, figure_type):
    if figure_type == FigureType.BISHOP:
        return Bishop(color)
    elif figure_type == FigureType.PAWN:
        return Pawn(color)
    elif figure_type == FigureType.KNIGHT:
        return Knight(color)
    elif figure_type == FigureType.KING:
        return King(color)
    elif figure_type == FigureType.ROOK:
        return Rook(color)
    elif figure_type == FigureType.QUEEN:
        return Queen(color)
