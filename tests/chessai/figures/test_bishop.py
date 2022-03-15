from chessai.engine.state import State
from chessai.figures.figure_type import FigureType
from chessai.figures.factory import get_figure
from chessai.utils.color import Color


class TestBishop:

    def test_bishop(self):

        w_bishop_cord = (5, 7)

        w_pawn1_cord = (3, 5)
        w_pawn2_cord = (4, 8)
        w_pawn3_cord = (5, 6)

        b_rook_cord = (7, 5)
        

        board = dict()

        bishop_to_test = get_figure(Color.WHITE, FigureType.BISHOP)
    
        board[w_bishop_cord] = bishop_to_test

        board[w_pawn1_cord] = get_figure(Color.WHITE, FigureType.PAWN)
        board[w_pawn2_cord] = get_figure(Color.WHITE, FigureType.PAWN)
        board[w_pawn3_cord] = get_figure(Color.WHITE, FigureType.PAWN)

        board[b_rook_cord] = get_figure(Color.BLACK, FigureType.ROOK)
        

        state = State(board)

        potential_moves = bishop_to_test.get_potential_moves(state, w_bishop_cord)

        assert len(potential_moves) == 4

        assert set([b_rook_cord, (4,6),  (6,6), (6,8)]) == set(potential_moves)