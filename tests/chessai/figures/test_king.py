from chessai.engine.state import State
from chessai.figures.figure_type import FigureType
from chessai.figures.factory import get_figure
from chessai.utils.color import Color
from chessai.moves.move import CURNT, DEST


class TestKing:
    def test_wk_all_block_except_one_empty_on_opponent_piece(self):
        w_king_cord = (5, 6)
        w_queen_cord = (5, 7)
        w_rook1_cord = (5, 5)
        w_rook2_cord = (6, 6)
        w_pawn1_cord = (6, 7)
        w_pawn2_cord = (4, 6)
        w_pawn3_cord = (4, 7)

        b_king_cord = (8, 6)
        b_rook_cord = (6, 5)

        board = dict()

        king_to_test = get_figure(Color.WHITE, FigureType.KING)

        board[w_king_cord] = king_to_test
        board[w_queen_cord] = get_figure(Color.WHITE, FigureType.QUEEN)
        board[w_rook1_cord] = get_figure(Color.WHITE, FigureType.ROOK)
        board[w_rook2_cord] = get_figure(Color.WHITE, FigureType.ROOK)
        board[w_pawn1_cord] = get_figure(Color.WHITE, FigureType.PAWN)
        board[w_pawn2_cord] = get_figure(Color.WHITE, FigureType.PAWN)
        board[w_pawn3_cord] = get_figure(Color.WHITE, FigureType.PAWN)

        board[b_king_cord] = get_figure(Color.BLACK, FigureType.KING)
        board[b_rook_cord] = get_figure(Color.BLACK, FigureType.ROOK)

        state = State(board)

        potential_moves = king_to_test.get_potential_moves(state, w_king_cord)

        assert len(potential_moves) == 2

        assert set([w_king_cord]) == set((mov[CURNT] for mov in potential_moves))

        assert set([b_rook_cord, (4, 5)]) == set((mov[DEST] for mov in potential_moves))

    def test_wk_all_free(self):
        w_king_cord = (5, 6)

        b_king_cord = (8, 6)

        board = dict()

        king_to_test = get_figure(Color.WHITE, FigureType.KING)

        board[w_king_cord] = king_to_test

        board[b_king_cord] = get_figure(Color.BLACK, FigureType.KING)

        state = State(board)

        potential_moves = king_to_test.get_potential_moves(state, w_king_cord)

        assert len(potential_moves) == 8

        assert set([w_king_cord]) == set((mov[CURNT] for mov in potential_moves))

        assert set(
            [(5, 7), (5, 5), (6, 6), (6, 7), (4, 6), (4, 7), (6, 5), (4, 5)]
        ) == set((mov[DEST] for mov in potential_moves))

    def test_king_distance_rule(self):
        w_king_cord = (5, 6)

        b_king1_cord = (7, 6)
        b_king2_cord = (5, 4)
        b_king3_cord = (3, 6)
        b_king4_cord = (5, 8)

        board = dict()

        king_to_test = get_figure(Color.WHITE, FigureType.KING)

        board[w_king_cord] = king_to_test

        board[b_king1_cord] = get_figure(Color.BLACK, FigureType.KING)
        board[b_king2_cord] = get_figure(Color.BLACK, FigureType.KING)
        board[b_king3_cord] = get_figure(Color.BLACK, FigureType.KING)
        board[b_king4_cord] = get_figure(Color.BLACK, FigureType.KING)

        state = State(board)

        potential_moves = king_to_test.get_potential_moves(state, w_king_cord)

        assert len(potential_moves) == 0

        del board[b_king4_cord]

        state = State(board)

        potential_moves = king_to_test.get_potential_moves(state, w_king_cord)

        assert len(potential_moves) == 1

        assert set([w_king_cord]) == set((mov[CURNT] for mov in potential_moves))

        assert set((mov[DEST] for mov in potential_moves)) == set([(5, 7)])
