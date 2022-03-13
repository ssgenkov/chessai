from chessai.moves.move import Move
from chessai.moves.moves_factory import get_movement


class KingVision:
    def __init__(self, color, state):
        self.color = color
        self.vision = self.get_vision(state)

    def get_vision(self, state):
        king_row, king_col = state.get_king_cord(self.color)

        vision = []

        for move in Move:
            mov_row, mov_col = get_movement(move)
            row_chk = king_row + mov_row
            col_chk = king_col + mov_col
            while row_chk > 0 and row_chk < 9 and col_chk > 0 and col_chk < 9:
                if state.get_figure(row_chk, col_chk):
                    vision.append(state.get_figure(row_chk, col_chk))
                    break

                row_chk = king_row + mov_row
                col_chk = king_col + mov_col
