from chessai.utils.color import Color
from chessai.figures.figure import Figure
from chessai.figures.figure_type import FigureType
from chessai.utils.cord import ROW, COLUMN


class Pawn(Figure):
    def __init__(self, color):
        super().__init__(color, FigureType.PAWN)
        self.two_moves_pos = 2 if color == Color.WHITE else 7
        self.move_direction = 1 if color == Color.WHITE else -1

    def get_potential_moves(self, state, cord):
        row = cord[ROW]  
        col = cord[COLUMN]

        potential_moves = []

        for row_inc in [1, 2]:
            pot_row = row + row_inc * self.move_direction
            pot_col = col

            if self._is_in_the_board(pot_row, pot_col):
                if state.get_figure_by_cord((pot_row, pot_col)):
                    break
                else:
                    potential_moves.append((pot_row, pot_col))
                if row != self.two_moves_pos:
                    break

        for col_inc in [-1, 1]:
            pot_row = row + self.move_direction
            pot_col = col + col_inc * self.move_direction

            if self._is_in_the_board(pot_row, pot_col):
                pot_fig =  state.get_figure_by_cord((pot_row, pot_col))

                if pot_fig and pot_fig.color != self.color:
                    potential_moves.append((pot_row, pot_col))

        return potential_moves


    def _is_in_the_board(self, idx):
        return idx > 0 and idx < 9
