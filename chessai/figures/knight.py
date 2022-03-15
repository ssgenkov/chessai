from chessai.figures.figure import Figure
from chessai.figures.figure_type import FigureType
from chessai.utils.cord import ROW, COLUMN


class Knight(Figure):
    def __init__(self, color):
        super().__init__(color, FigureType.KNIGHT)

    def get_potential_moves(self, state, cord):
        row = cord[ROW]
        col = cord[COLUMN]

        potential_moves = []
        for row_inc, col_inc in [(1, 2), (2, 1)]:
            for row_dir in [1, -1]:
                for col_dir in [1, -1]:
                    pot_row = row + row_inc * row_dir
                    pot_col = col + col_inc * col_dir
                    if self._is_in_the_board(pot_row, pot_col):
                        pot_fig = state.get_figure_by_cord((pot_row, pot_col))
                        if pot_fig:
                            if pot_fig.color != self.color:
                                potential_moves.append((pot_row, pot_col))
                        else:
                            potential_moves.append((pot_row, pot_col))

        return potential_moves
