from chessai.moves.move import Move
from chessai.engine.king_vision import KingVision
from chessai.engine.state import State
from chessai.figures.figure_type import FigureType
from chessai.figures.factory import get_figure
from chessai.utils.color import Color


class TestKingVision:
    def setup_method(self):

        self.w_king_cord = (2, 7)
        self.w_queen_cord = (3, 6)
        self.w_rook1_cord = (4, 4)
        self.w_rook2_cord = (5, 8)
        self.w_pawn1_cord = (2, 2)
        self.w_pawn2_cord = (2, 6)
        self.w_pawn3_cord = (3, 7)
        self.w_pawn4_cord = (4, 3)
        self.w_pawn5_cord = (5, 4)

        self.b_king_cord = (7, 6)
        self.b_queen_cord = (5, 7)
        self.b_rook1_cord = (8, 7)
        self.b_rook2_cord = (1, 5)
        self.b_pawn1_cord = (6, 2)
        self.b_pawn2_cord = (6, 4)
        self.b_pawn3_cord = (5, 6)
        self.b_pawn4_cord = (4, 2)
        self.b_knight_cord = (5, 5)

        board = dict()
        board[self.w_king_cord] = get_figure(Color.WHITE, FigureType.KING)
        board[self.w_queen_cord] = get_figure(Color.WHITE, FigureType.QUEEN)
        board[self.w_rook1_cord] = get_figure(Color.WHITE, FigureType.ROOK)
        board[self.w_rook2_cord] = get_figure(Color.WHITE, FigureType.ROOK)
        board[self.w_pawn1_cord] = get_figure(Color.WHITE, FigureType.PAWN)
        board[self.w_pawn2_cord] = get_figure(Color.WHITE, FigureType.PAWN)
        board[self.w_pawn3_cord] = get_figure(Color.WHITE, FigureType.PAWN)
        board[self.w_pawn4_cord] = get_figure(Color.WHITE, FigureType.PAWN)
        board[self.w_pawn5_cord] = get_figure(Color.WHITE, FigureType.PAWN)

        board[self.b_king_cord] = get_figure(Color.BLACK, FigureType.KING)
        board[self.b_queen_cord] = get_figure(Color.BLACK, FigureType.QUEEN)
        board[self.b_rook1_cord] = get_figure(Color.BLACK, FigureType.ROOK)
        board[self.b_rook2_cord] = get_figure(Color.BLACK, FigureType.ROOK)
        board[self.b_pawn1_cord] = get_figure(Color.BLACK, FigureType.PAWN)
        board[self.b_pawn2_cord] = get_figure(Color.BLACK, FigureType.PAWN)
        board[self.b_pawn3_cord] = get_figure(Color.BLACK, FigureType.PAWN)
        board[self.b_pawn4_cord] = get_figure(Color.BLACK, FigureType.PAWN)
        board[self.b_knight_cord] = get_figure(Color.BLACK, FigureType.KNIGHT)

        self.state = State(board)

    def test_white_king_vision(self):
        king_vision = KingVision(Color.WHITE, self.state)

        vision = king_vision.get_vision()

        assert len(vision) == 3

        expected_vision = {}
        expected_vision[self.w_queen_cord] = (
            self.state.get_figure_by_cord(self.w_queen_cord),
            Move.LU_DIAG,
        )
        expected_vision[self.w_pawn3_cord] = (
            self.state.get_figure_by_cord(self.w_pawn3_cord),
            Move.UP,
        )
        expected_vision[self.w_pawn2_cord] = (
            self.state.get_figure_by_cord(self.w_pawn2_cord),
            Move.LEFT,
        )

        assert expected_vision == vision

    def test_black_king_vision(self):
        king_vision = KingVision(Color.BLACK, self.state)
        vision = king_vision.get_vision()

        assert len(vision) == 4

        expected_vision = {}
        expected_vision[self.b_rook1_cord] = (
            self.state.get_figure_by_cord(self.b_rook1_cord),
            Move.RU_DIAG,
        )
        expected_vision[self.w_pawn5_cord] = (
            self.state.get_figure_by_cord(self.w_pawn5_cord),
            Move.LD_DIAG,
        )
        expected_vision[self.b_pawn3_cord] = (
            self.state.get_figure_by_cord(self.b_pawn3_cord),
            Move.DOWN,
        )
        expected_vision[self.w_rook2_cord] = (
            self.state.get_figure_by_cord(self.w_rook2_cord),
            Move.RD_DIAG,
        )

        assert expected_vision == vision
