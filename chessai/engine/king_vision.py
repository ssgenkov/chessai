from chessai.moves.move import Move
from chessai.moves.moves_factory import get_movement
from chessai.figures.figure_type import FigureType


class KingVision:
    def __init__(self, color, state):
        self.color = color
        self.vision = self._get_vision(state)

    def _get_vision(self, state):
        king_row, king_col = state.get_figures_cord(self.color, FigureType.KING)[0]

        vision = {}

        for move in Move:
            mov_row, mov_col = get_movement(move)
            row_chk = king_row + mov_row
            col_chk = king_col + mov_col
            while row_chk > 0 and row_chk < 9 and col_chk > 0 and col_chk < 9:
                if state.get_figure_by_cord((row_chk, col_chk)):
                    vision[(row_chk, col_chk)] = (state.get_figure_by_cord((row_chk, col_chk)), move)
                    break

                row_chk = row_chk + mov_row
                col_chk = col_chk + mov_col


        return vision

    def get_vision(self):
        return self.vision
