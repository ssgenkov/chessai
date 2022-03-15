from chessai.figures.figure import Figure
from chessai.moves.move import Move
from chessai.moves.moves_factory import get_movement
from chessai.utils.cord import ROW, COLUMN


class QRBPiece(Figure):
    def __init__(self, color, figure_type, moves):
        super().__init__(color, figure_type)
        self.moves = moves

    def get_potential_moves(self, state, cord):
        row = cord[ROW]
        col = cord[COLUMN]

        potential_moves = []

        for move in self.moves:
            mov_row, mov_col = get_movement(move)
            pot_row = row + mov_row
            pot_col = col + mov_col
            while self._is_in_the_board(pot_row, pot_col):
                pot_fig = state.get_figure_by_cord((pot_row, pot_col))
                if pot_fig:
                    if pot_fig.color != self.color:
                        potential_moves.append((pot_row, pot_col))
                    break
                else:
                    potential_moves.append((pot_row, pot_col))
                pot_row = pot_row + mov_row
                pot_col = pot_col + mov_col

        return potential_moves

    def get_moves(self):
        return self.moves
