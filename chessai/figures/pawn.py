from chessai.utils.color import Color
from chessai.figures.figure import Figure
from chessai.figures.figure_type import FigureType


class Pawn(Figure):
    def __init__(self, color):
        super().__init__(color, FigureType.PAWN)
        self.two_moves_pos = 2 if color == Color.WHITE else 7
        self.move_direction = 1 if color == Color.WHITE else -1

    def get_possible_moves(self, state, col, row):
        possible_moves = []

        for i in [1, 2]:
            if (
                self._is_in_the_board(row + i * self.move_direction)
                and f"{col}{row+i*self.move_direction}" not in state
            ):
                possible_moves.append(
                    f"{col}{row}{self.sep}{col}{row+i*self.move_direction}"
                )
            else:
                break

        for i in [-1, 1]:
            if (
                self._is_in_the_board(col + i)
                and f"{col+i}{row+self.move_direction}" not in state
                and state[f"{col+i}{row+self.move_direction}"].color != self.color
            ):
                possible_moves.append(
                    f"{col}{row}{self.sep}{col+i}{row+self.move_direction}"
                )

        return possible_moves

    def _is_in_the_board(self, idx):
        return idx > 0 and idx < 9
