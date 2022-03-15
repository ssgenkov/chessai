from chessai.engine.state import State
from chessai.figures.figure_type import FigureType
from chessai.figures.factory import get_figure
from chessai.utils.color import Color


class TestKnight:

    def test_knight_all_moves(self):
        b_knigh_cord = (5, 4)
        
        board = dict()

        knight_to_test = get_figure(Color.BLACK, FigureType.KNIGHT)
    
        board[b_knigh_cord] = knight_to_test
        

        state = State(board)

        potential_moves = knight_to_test.get_potential_moves(state, b_knigh_cord)

        assert len(potential_moves) == 8

        assert set([(6,6), (7,5), (7,3), (6,2), (4,2), (3,3), (3,5), (4,6)]) == set(potential_moves)

    
    def test_knight(self):
        b_knigh_cord = (5, 4)
        b_pawn_cord = (6,2)
        b_rook_cord =  (7,5)

        w_pawn_cord = (6,6)
        w_rook_cord =  (3,5)

        board = dict()

        knight_to_test = get_figure(Color.BLACK, FigureType.KNIGHT)
    
        board[b_knigh_cord] = knight_to_test
        board[b_pawn_cord] = get_figure(Color.BLACK, FigureType.PAWN)
        board[b_rook_cord] = get_figure(Color.BLACK, FigureType.ROOK)

        board[w_pawn_cord] = get_figure(Color.WHITE, FigureType.PAWN)
        board[w_rook_cord] = get_figure(Color.WHITE, FigureType.ROOK)

        state = State(board)

        potential_moves = knight_to_test.get_potential_moves(state, b_knigh_cord)

        assert len(potential_moves) == 6

        assert set([w_pawn_cord, (7,3), (4,2), (3,3), w_rook_cord, (4,6)]) == set(potential_moves)


    def test_knight_two_moves(self):
        w_knigh_cord = (8, 8)
        
        board = dict()

        knight_to_test = get_figure(Color.WHITE, FigureType.KNIGHT)
    
        board[w_knigh_cord] = knight_to_test
        

        state = State(board)

        potential_moves = knight_to_test.get_potential_moves(state, w_knigh_cord)

        assert len(potential_moves) == 2

        assert set([(7,6), (6,7)]) == set(potential_moves)
