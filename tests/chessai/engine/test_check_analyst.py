from chessai.moves.move import Move
from chessai.engine.king_vision import KingVision
from chessai.engine.state import State
from chessai.engine.check_analyst import CheckAnalyst
from chessai.figures.figure_type import FigureType
from chessai.figures.factory import get_figure
from chessai.utils.color import Color


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
