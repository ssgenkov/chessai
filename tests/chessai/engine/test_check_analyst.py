from chessai.moves.move import Move
from chessai.engine.king_vision import KingVision
from chessai.engine.state import State
from chessai.engine.check_analyst import CheckAnalyst
from chessai.figures.figure_type import FigureType
from chessai.figures.factory import get_figure
from chessai.utils.color import Color
from chessai.moves.move import CURNT, DEST


class TestCheckAnalyst:
    def test_get_checking_pieces_b_2p(self):

        b_king_cord = (4, 5)
        b_rook_cord = (4, 7)
        b_knight_cord = (5, 4)
        b_bishop_cord = (7, 8)

        w_queen_cord = (4, 2)
        w_knight_cord = (6, 4)
        w_bishop_cord = (7, 2)
        w_pawn_cord = (3, 5)

        board = dict()

        king_to_check = get_figure(Color.BLACK, FigureType.KING)

        board[b_king_cord] = king_to_check
        board[b_rook_cord] = get_figure(Color.BLACK, FigureType.ROOK)
        board[b_knight_cord] = get_figure(Color.BLACK, FigureType.KNIGHT)
        board[b_bishop_cord] = get_figure(Color.BLACK, FigureType.BISHOP)

        board[w_queen_cord] = get_figure(Color.WHITE, FigureType.QUEEN)
        board[w_knight_cord] = get_figure(Color.WHITE, FigureType.KNIGHT)
        board[w_bishop_cord] = get_figure(Color.WHITE, FigureType.BISHOP)
        board[w_pawn_cord] = get_figure(Color.WHITE, FigureType.PAWN)

        state = State(board)

        check_analyst = CheckAnalyst()

        checking_pieces = check_analyst.get_checking_pieces(
            king_to_check.color, state, KingVision(king_to_check.color, state)
        )

        assert len(checking_pieces) == 2

        assert set(checking_pieces) == set(
            [
                (w_queen_cord, state.get_figure_by_cord(w_queen_cord), Move.LEFT),
                (w_knight_cord, state.get_figure_by_cord(w_knight_cord), None),
            ]
        )

    def test_get_checking_pieces_b_1p(self):

        b_king_cord = (4, 5)
        b_rook_cord = (4, 7)
        b_knight_cord = (5, 4)
        b_bishop_cord = (7, 8)
        b_pawn_cord = (4, 3)

        w_queen_cord = (4, 2)
        w_knight_cord = (6, 4)
        w_bishop_cord = (7, 2)
        w_pawn_cord = (3, 5)

        board = dict()

        king_to_check = get_figure(Color.BLACK, FigureType.KING)

        board[b_king_cord] = king_to_check
        board[b_rook_cord] = get_figure(Color.BLACK, FigureType.ROOK)
        board[b_knight_cord] = get_figure(Color.BLACK, FigureType.KNIGHT)
        board[b_bishop_cord] = get_figure(Color.BLACK, FigureType.BISHOP)
        board[b_pawn_cord] = get_figure(Color.BLACK, FigureType.PAWN)

        board[w_queen_cord] = get_figure(Color.WHITE, FigureType.QUEEN)
        board[w_knight_cord] = get_figure(Color.WHITE, FigureType.KNIGHT)
        board[w_bishop_cord] = get_figure(Color.WHITE, FigureType.BISHOP)
        board[w_pawn_cord] = get_figure(Color.WHITE, FigureType.PAWN)

        state = State(board)

        check_analyst = CheckAnalyst()

        checking_pieces = check_analyst.get_checking_pieces(
            king_to_check.color, state, KingVision(king_to_check.color, state)
        )

        assert len(checking_pieces) == 1

        assert set(checking_pieces) == set(
            [
                (w_knight_cord, state.get_figure_by_cord(w_knight_cord), None),
            ]
        )

    def test_get_checking_pieces_w_0p(self):

        b_king_cord = (4, 5)
        b_rook_cord = (4, 7)
        b_knight_cord = (5, 4)
        b_bishop_cord = (7, 8)
        b_pawn_cord = (4, 3)

        w_king_cord = (6, 3)
        w_queen_cord = (4, 2)
        w_knight_cord = (6, 4)
        w_bishop_cord = (7, 2)
        w_pawn_cord = (3, 5)

        board = dict()

        

        board[b_king_cord] = get_figure(Color.BLACK, FigureType.KING)
        board[b_rook_cord] = get_figure(Color.BLACK, FigureType.ROOK)
        board[b_knight_cord] = get_figure(Color.BLACK, FigureType.KNIGHT)
        board[b_bishop_cord] = get_figure(Color.BLACK, FigureType.BISHOP)
        board[b_pawn_cord] = get_figure(Color.BLACK, FigureType.PAWN)

        king_to_check = get_figure(Color.WHITE, FigureType.KING)

        board[w_king_cord] = king_to_check
        board[w_queen_cord] = get_figure(Color.WHITE, FigureType.QUEEN)
        board[w_knight_cord] = get_figure(Color.WHITE, FigureType.KNIGHT)
        board[w_bishop_cord] = get_figure(Color.WHITE, FigureType.BISHOP)
        board[w_pawn_cord] = get_figure(Color.WHITE, FigureType.PAWN)

        state = State(board)

        check_analyst = CheckAnalyst()

        checking_pieces = check_analyst.get_checking_pieces(
            king_to_check.color, state, KingVision(king_to_check.color, state)
        )

        assert len(checking_pieces) == 0

    def test_get_checking_pieces_w_1p(self):

        b_king_cord = (4, 5)
        b_rook_cord = (4, 7)
        b_knight_cord = (5, 4)
        b_bishop_cord = (7, 8)
        b_pawn_cord = (4, 3)

        w_king_cord = (3, 2)
        w_queen_cord = (4, 2)
        w_knight_cord = (6, 4)
        w_bishop_cord = (7, 2)
        w_pawn_cord = (3, 5)

        board = dict()

        

        board[b_king_cord] = get_figure(Color.BLACK, FigureType.KING)
        board[b_rook_cord] = get_figure(Color.BLACK, FigureType.ROOK)
        board[b_knight_cord] = get_figure(Color.BLACK, FigureType.KNIGHT)
        board[b_bishop_cord] = get_figure(Color.BLACK, FigureType.BISHOP)
        board[b_pawn_cord] = get_figure(Color.BLACK, FigureType.PAWN)

        king_to_check = get_figure(Color.WHITE, FigureType.KING)

        board[w_king_cord] = king_to_check
        board[w_queen_cord] = get_figure(Color.WHITE, FigureType.QUEEN)
        board[w_knight_cord] = get_figure(Color.WHITE, FigureType.KNIGHT)
        board[w_bishop_cord] = get_figure(Color.WHITE, FigureType.BISHOP)
        board[w_pawn_cord] = get_figure(Color.WHITE, FigureType.PAWN)

        state = State(board)

        check_analyst = CheckAnalyst()

        checking_pieces = check_analyst.get_checking_pieces(
            king_to_check.color, state, KingVision(king_to_check.color, state)
        )

        assert len(checking_pieces) == 1

        assert set(checking_pieces) == set(
            [
                (b_pawn_cord, state.get_figure_by_cord(b_pawn_cord), Move.RU_DIAG),
            ]
        )


    def test_get_check_analysis_b_2cp(self):

        b_king_cord = (4, 5)
        b_rook_cord = (4, 7)
        b_knight_cord = (5, 4)
        b_bishop_cord = (7, 8)

        w_queen_cord = (4, 2)
        w_knight_cord = (6, 4)
        w_bishop_cord = (7, 2)
        w_pawn_cord = (3, 5)

        board = dict()

        king_to_check = get_figure(Color.BLACK, FigureType.KING)

        board[b_king_cord] = king_to_check
        board[b_rook_cord] = get_figure(Color.BLACK, FigureType.ROOK)
        board[b_knight_cord] = get_figure(Color.BLACK, FigureType.KNIGHT)
        board[b_bishop_cord] = get_figure(Color.BLACK, FigureType.BISHOP)

        board[w_queen_cord] = get_figure(Color.WHITE, FigureType.QUEEN)
        board[w_knight_cord] = get_figure(Color.WHITE, FigureType.KNIGHT)
        board[w_bishop_cord] = get_figure(Color.WHITE, FigureType.BISHOP)
        board[w_pawn_cord] = get_figure(Color.WHITE, FigureType.PAWN)

        state = State(board)

        check_analyst = CheckAnalyst()

        check_analysis = check_analyst.get_analysis(
            king_to_check.color, state, KingVision(king_to_check.color, state)
        )

        assert check_analysis.there_is_check

        assert check_analysis.cord_of_piece_to_capture == None

        assert check_analysis.interposing_dest_coordinates == []

        assert set([b_king_cord]) == set((mov[CURNT] for mov in check_analysis.king_legal_moves))

        assert set((mov[DEST] for mov in check_analysis.king_legal_moves)) == set([(5, 5), (3, 5),(3, 4),(3, 6)])
