from chessai.figures.figure import Figure
from chessai.figures.figure_type import FigureType
from chessai.moves.move import Move
from chessai.moves.moves_factory import get_movement
from chessai.utils.cord import ROW, COLUMN


class King(Figure):
    def __init__(self, color):
        super().__init__(color, FigureType.KING)

    def get_potential_moves(self, state, cord):
        row = cord[ROW]  
        col = cord[COLUMN]
        
        potential_moves = []
        for move in Move:
            mov_row, mov_col = get_movement(move)
            pot_row = row + mov_row
            pot_col = col + mov_col
            if self._is_in_the_board(pot_row, pot_col):
                pot_fig = state.get_figure_by_cord((pot_row, pot_col))
                if pot_fig:
                    if pot_fig.color != self.color:
                        potential_moves.append((pot_row, pot_col))
                else:
                    potential_moves.append((pot_row, pot_col))

        return potential_moves
