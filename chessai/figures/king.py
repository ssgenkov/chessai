from chessai.figures.figure import Figure
from chessai.figures.figure_type import FigureType


class King(Figure):
    def __init__(self, color):
        super().__init__(color, FigureType.KING)

    def get_possible_moves(self, state, col, row):
        return []
