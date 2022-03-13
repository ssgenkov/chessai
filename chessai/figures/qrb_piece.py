from chessai.figures.figure import Figure


class QRBPiece(Figure):
    def __init__(self, color, figure_type, moves):
        super().__init__(color, figure_type)
        self.moves = moves

    def get_possible_moves(self, state, col, row):
        possible_moves = []

        for col_chg, row_chg in zip(self.col_change, self.row_change):
            col_new = col + col_chg
            row_new = row + row_chg
            while self._is_in_the_board(col_new, row_new):
                if f"{col_new}{row_new}" in state:
                    if state[f"{col_new}{row_new}"].color != self.color:
                        possible_moves.append(f"{col}{row}{self.sep}{col_new}{row_new}")
                    break
                else:
                    possible_moves.append(f"{col}{row}{self.sep}{col_new}{row_new}")
                col_new = col_new + col_chg
                row_new = row_new + row_chg

        return possible_moves
