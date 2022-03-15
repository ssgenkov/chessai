from chessai.utils.cord import ROW, COLUMN
from collections import defaultdict
from chessai.utils.color import Color
from chessai.figures.figure_type import FigureType


class State:
    def __init__(self, board, figures=None):
        self._board = board
        if figures is None:
            self._figures = self._build_and_get_figures(board)

    def _build_and_get_figures(self, board):
        figures = self._get_init_figures_dict()
        for cord, figure in board.items():
            figures[figure.color][figure.figure_type].append(cord)

        return figures

    def _get_init_figures_dict(self):
        figures = defaultdict(dict)
        for color in Color:
            figures[color] = defaultdict(dict)
            for figure_type in FigureType:
                figures[color][figure_type] = []

        return figures

    def get_board_copy(self):
        return dict(self._board)

    def get_figure_by_cord(self, cords):
        row = cords[ROW]
        col = cords[COLUMN]
        return self._board[(row, col)] if (row, col) in self._board else None

    def get_figures_cord(self, color, figure_type):
        # TODO this list() may be removed due to performance issues
        return list(self._figures[color][figure_type])
