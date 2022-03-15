from chessai.engine.state import State
from chessai.figures.figure_type import FigureType
from chessai.figures.factory import get_figure
from chessai.utils.color import Color
from chessai.moves.move import CURNT, DEST


class TestPawn:
    def test_b_pawn_init(self):

        b_pawn_cord = (7, 4)

        w_rook_cord = (6, 3)
        w_bishop_cord = (6, 5)

        pawn_to_test = get_figure(Color.BLACK, FigureType.PAWN)

        board = {}

        board[b_pawn_cord] = pawn_to_test

        board[w_rook_cord] = get_figure(Color.WHITE, FigureType.ROOK)
        board[w_bishop_cord] = get_figure(Color.WHITE, FigureType.BISHOP)

        state = State(board)

        potential_moves = pawn_to_test.get_potential_moves(state, b_pawn_cord)

        assert len(potential_moves) == 4

        assert set([b_pawn_cord]) == set((mov[CURNT] for mov in potential_moves))

        assert set((mov[DEST] for mov in potential_moves)) == set(
            [w_rook_cord, w_bishop_cord, (6, 4), (5, 4)]
        )

        board = {}

        board[b_pawn_cord] = pawn_to_test

        state = State(board)

        potential_moves = pawn_to_test.get_potential_moves(state, b_pawn_cord)

        assert len(potential_moves) == 2

        assert set([b_pawn_cord]) == set((mov[CURNT] for mov in potential_moves))

        assert set((mov[DEST] for mov in potential_moves)) == set([(6, 4), (5, 4)])

    def test_b_pawn_mid(self):

        b_pawn_cord = (6, 4)
        b_rook_cord = (5, 5)

        w_rook_cord = (4, 3)
        w_bishop_cord = (7, 5)
        w_knight_cord = (4, 5)

        pawn_to_test = get_figure(Color.BLACK, FigureType.PAWN)

        board = {}

        board[b_pawn_cord] = pawn_to_test
        board[b_rook_cord] = get_figure(Color.BLACK, FigureType.ROOK)

        board[w_rook_cord] = get_figure(Color.WHITE, FigureType.ROOK)
        board[w_bishop_cord] = get_figure(Color.WHITE, FigureType.BISHOP)
        board[w_knight_cord] = get_figure(Color.WHITE, FigureType.KNIGHT)

        state = State(board)

        potential_moves = pawn_to_test.get_potential_moves(state, b_pawn_cord)

        assert len(potential_moves) == 1

        assert set([b_pawn_cord]) == set((mov[CURNT] for mov in potential_moves))

        assert set((mov[DEST] for mov in potential_moves)) == set([(5, 4)])

    def test_w_pawn_init(self):

        w_pawn_cord = (2, 4)

        b_rook_cord = (3, 3)
        b_bishop_cord = (3, 5)

        pawn_to_test = get_figure(Color.WHITE, FigureType.PAWN)

        board = {}

        board[w_pawn_cord] = pawn_to_test

        board[b_rook_cord] = get_figure(Color.BLACK, FigureType.ROOK)
        board[b_bishop_cord] = get_figure(Color.BLACK, FigureType.BISHOP)

        state = State(board)

        potential_moves = pawn_to_test.get_potential_moves(state, w_pawn_cord)

        assert len(potential_moves) == 4

        assert set([w_pawn_cord]) == set((mov[CURNT] for mov in potential_moves))

        assert set((mov[DEST] for mov in potential_moves)) == set(
            [b_rook_cord, b_bishop_cord, (3, 4), (4, 4)]
        )

        board = {}

        board[w_pawn_cord] = pawn_to_test

        state = State(board)

        potential_moves = pawn_to_test.get_potential_moves(state, w_pawn_cord)

        assert len(potential_moves) == 2

        assert set([w_pawn_cord]) == set((mov[CURNT] for mov in potential_moves))

        assert set((mov[DEST] for mov in potential_moves)) == set([(3, 4), (4, 4)])

    def test_w_pawn_mid(self):

        w_pawn_cord = (3, 4)
        w_rook_cord = (4, 5)

        b_rook_cord = (5, 3)
        b_bishop_cord = (2, 5)
        b_knight_cord = (5, 5)

        pawn_to_test = get_figure(Color.WHITE, FigureType.PAWN)

        board = {}

        board[w_pawn_cord] = pawn_to_test
        board[w_rook_cord] = get_figure(Color.WHITE, FigureType.ROOK)

        board[b_rook_cord] = get_figure(Color.BLACK, FigureType.ROOK)
        board[b_bishop_cord] = get_figure(Color.BLACK, FigureType.BISHOP)
        board[b_knight_cord] = get_figure(Color.BLACK, FigureType.KNIGHT)

        state = State(board)

        potential_moves = pawn_to_test.get_potential_moves(state, w_pawn_cord)

        assert len(potential_moves) == 1

        assert set([w_pawn_cord]) == set((mov[CURNT] for mov in potential_moves))

        assert set((mov[DEST] for mov in potential_moves)) == set([(4, 4)])

    def test_w_pawn_no_moves(self):

        w_pawn1_cord = (3, 4)
        w_rook_cord = (4, 4)
        w_pawn2_cord = (8, 4)

        pawn1_to_test = get_figure(Color.WHITE, FigureType.PAWN)
        pawn2_to_test = get_figure(Color.WHITE, FigureType.PAWN)

        board = {}

        board[w_pawn1_cord] = pawn1_to_test
        board[w_pawn2_cord] = pawn2_to_test
        board[w_rook_cord] = get_figure(Color.WHITE, FigureType.ROOK)

        state = State(board)

        potential_moves = pawn1_to_test.get_potential_moves(state, w_pawn1_cord)

        assert len(potential_moves) == 0

        potential_moves = pawn2_to_test.get_potential_moves(state, w_pawn2_cord)

        assert len(potential_moves) == 0
