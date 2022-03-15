from chessai.engine.state import State
from chessai.figures.figure_type import FigureType
from chessai.figures.factory import get_figure
from chessai.utils.color import Color
from chessai.moves.move import CURNT, DEST


class TestRook:
    def test_rook(self):

        w_rook_cord = (6, 6)

        w_pawn1_cord = (6, 3)
        w_pawn2_cord = (6, 8)
        w_pawn3_cord = (8, 4)

        b_rook_cord = (4, 6)

        board = dict()

        rook_to_test = get_figure(Color.WHITE, FigureType.ROOK)

        board[w_rook_cord] = rook_to_test

        board[w_pawn1_cord] = get_figure(Color.WHITE, FigureType.PAWN)
        board[w_pawn2_cord] = get_figure(Color.WHITE, FigureType.PAWN)
        board[w_pawn3_cord] = get_figure(Color.WHITE, FigureType.PAWN)

        board[b_rook_cord] = get_figure(Color.BLACK, FigureType.ROOK)

        state = State(board)

        potential_moves = rook_to_test.get_potential_moves(state, w_rook_cord)

        (mov[1] for mov in potential_moves)

        assert len(potential_moves) == 7

        assert set([w_rook_cord]) == set((mov[CURNT] for mov in potential_moves))

        assert set(
            [b_rook_cord, (5, 6), (6, 4), (6, 5), (6, 7), (7, 6), (8, 6)]
        ) == set((mov[DEST] for mov in potential_moves))
