from chessai.figures.figure import Figure
from chessai.figures.figure_type import FigureType


class Knight(Figure):
    def __init__(self, color):
        super().__init__(color, FigureType.KNIGHT)

    def get_possible_moves(self, state, col, row):
        return []