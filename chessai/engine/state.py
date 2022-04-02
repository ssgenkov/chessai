from chessai.utils.cord import ROW, COLUMN
from collections import defaultdict
from chessai.utils.color import Color
from chessai.figures.figure_type import FigureType


class State:
    def __init__(self, board, figures=None, has_moved=None):
        self._board = board
        if figures is None:
            self._figures = self._build_and_get_figures(board)

        self._has_moved = has_moved

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

    def set_has_moved(self, color, castle_figure_type):
        if self._has_moved is None:
            self._has_moved = defaultdict(set)

        self._has_moved[color].add(castle_figure_type)

    def has_moved(self, color, castle_figure_type):
        if self._has_moved:
            return (
                color in self._has_moved
                and castle_figure_type in self._has_moved[color]
            )
        else:
            return False

    def get_board_copy(self):
        return dict(self._board)

    def remove_figure_by_cord(self, cord):
        if cord in self._board:
            del self._board[cord]
            self._figures = self._build_and_get_figures(self._board)

    def add_figure(self, cord, figure):
        self._board[cord] = figure
        self._figures = self._build_and_get_figures(self._board)

    def get_copy(self):
        has_moved_cpy = None
        if self._has_moved:
            has_moved_cpy = defaultdict(set)
            for color in self._has_moved:
                has_moved_cpy[color] = set(self._has_moved[color])
        return State(board=self.get_board_copy(), has_moved=has_moved_cpy)

    def get_figure_by_cord(self, cords):
        row = cords[ROW]
        col = cords[COLUMN]
        return self._board[(row, col)] if (row, col) in self._board else None

    def get_figures_cord(self, color, figure_type):
        # TODO this list() may be removed due to performance issues
        return list(self._figures[color][figure_type])

    def get_pieces_cords_for_color(self, color):
        return [cord for cord in self._board if self._board[cord].color == color]
