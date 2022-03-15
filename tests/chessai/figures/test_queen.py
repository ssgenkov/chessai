from chessai.engine.state import State
from chessai.figures.figure_type import FigureType
from chessai.figures.factory import get_figure
from chessai.utils.color import Color


class TestQueen:

    def test_queen(self):

        w_queen_cord = (6, 6)

        w_pawn1_cord = (6, 3)
        w_pawn2_cord = (6, 8)
        w_pawn3_cord = (8, 4)

        b_rook_cord = (4, 6)
        b_knight_cord = (4, 4)
        

        board = dict()

        queen_to_test = get_figure(Color.WHITE, FigureType.QUEEN)
    
        board[w_queen_cord] = queen_to_test

        board[w_pawn1_cord] = get_figure(Color.WHITE, FigureType.PAWN)
        board[w_pawn2_cord] = get_figure(Color.WHITE, FigureType.PAWN)
        board[w_pawn3_cord] = get_figure(Color.WHITE, FigureType.PAWN)

        board[b_rook_cord] = get_figure(Color.BLACK, FigureType.ROOK)
        board[b_knight_cord] = get_figure(Color.BLACK, FigureType.KNIGHT)
        

        state = State(board)

        potential_moves = queen_to_test.get_potential_moves(state, w_queen_cord)

        assert len(potential_moves) == 14

        assert set([b_rook_cord,b_knight_cord,  (5,6), (6,4),  (6,5), (6,7), (7,6), (8, 6), (5,5), (5,7), (4,8), (7,5), (7,7), (8,8)]) == set(potential_moves)