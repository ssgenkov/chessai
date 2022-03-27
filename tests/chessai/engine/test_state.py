from chessai.engine.state import State
from chessai.figures.figure_type import FigureType
from chessai.figures.factory import get_figure
from chessai.utils.color import Color
from chessai.utils.castle_figures import CastleFigureType


class TestState:
    def setup_method(self):
        board = dict()
        self.w_bishop_cord = (5, 1)
        self.w_king_cord = (5, 6)
        self.b_rook1_cord = (3, 2)
        self.b_rook2_cord = (1, 6)
        self.b_king_cord = (1, 7)
        board[self.w_bishop_cord] = get_figure(Color.WHITE, FigureType.BISHOP)
        board[self.w_king_cord] = get_figure(Color.WHITE, FigureType.KING)
        board[self.b_rook1_cord] = get_figure(Color.BLACK, FigureType.ROOK)
        board[self.b_rook2_cord] = get_figure(Color.BLACK, FigureType.ROOK)
        board[self.b_king_cord] = get_figure(Color.BLACK, FigureType.KING)
        self.board = board

    def test_get_figures_cord(self):
        state = State(self.board)
        black_rooks_coords = state.get_figures_cord(Color.BLACK, FigureType.ROOK)

        assert len(black_rooks_coords) == 2

        expected_cords_rook = set([self.b_rook1_cord, self.b_rook2_cord])
        for rook_coords in black_rooks_coords:
            assert rook_coords in expected_cords_rook
            expected_cords_rook.remove(rook_coords)

        white_king_coords = state.get_figures_cord(Color.WHITE, FigureType.KING)

        assert len(white_king_coords) == 1

        for white_king_coord in white_king_coords:
            assert white_king_coord == self.w_king_cord

    def test_get_figure_by_cord(self):
        state = State(self.board)

        black_king = state.get_figure_by_cord(self.b_king_cord)

        assert black_king.color == Color.BLACK
        assert black_king.figure_type == FigureType.KING

    def test_has_moved(self):
        state = State(self.board)

        assert state.has_moved(Color.WHITE, CastleFigureType.ROOK_KINGSIDE) == False

        state.set_has_moved(Color.WHITE, CastleFigureType.ROOK_KINGSIDE)

        assert state.has_moved(Color.WHITE, CastleFigureType.ROOK_KINGSIDE) == True

        assert state.has_moved(Color.BLACK, CastleFigureType.KING) == False

        state.set_has_moved(Color.BLACK, CastleFigureType.KING)

        assert state.has_moved(Color.BLACK, CastleFigureType.KING) == True

        assert state.get_copy().has_moved(Color.BLACK, CastleFigureType.KING) == True
        assert (
            state.get_copy().has_moved(Color.WHITE, CastleFigureType.ROOK_KINGSIDE)
            == True
        )
