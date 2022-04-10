from chessai.engine.state_changer import StateChanger
from chessai.figures.pawn import Pawn
from chessai.moves.move import Move
from chessai.engine.king_vision import KingVision
from chessai.engine.state import State
from chessai.engine.check_analyst import CheckAnalyst
from chessai.engine.valid_actions_determiner import ValidActionsDeterminer
from chessai.figures.figure_type import FigureType
from chessai.figures.factory import get_figure
from chessai.utils.color import Color
from chessai.moves.ply_category import PlyCategory
from chessai.moves.move import CURNT, DEST
from chessai.utils.castle_figures import CastleFigureType
from chessai.utils.cord import ROW, COLUMN


class TestStateChanger:


    def _get_casual_board(self):
        w_king_cord = (2, 5)
        w_rook_cord = (1, 1)
        w_pawn_cord = (7, 6)
        w_pawn2_cord = (2, 3)
        w_knight_cord = (4, 7)

        b_king_cord = (7, 5)
        b_rook_cord = (8, 1)
        b_pawn_cord = (2, 6)
        b_pawn2_cord = (7, 3)
        b_knight_cord = (6, 7)

        board = dict()

        board[w_king_cord] = get_figure(Color.WHITE, FigureType.KING)
        board[w_rook_cord] = get_figure(Color.WHITE, FigureType.ROOK)
        board[w_pawn_cord] = get_figure(Color.WHITE, FigureType.PAWN)
        board[w_pawn2_cord] = get_figure(Color.WHITE, FigureType.PAWN)
        board[w_knight_cord] = get_figure(Color.WHITE, FigureType.KNIGHT)

        board[b_king_cord] = get_figure(Color.BLACK, FigureType.KING)
        board[b_rook_cord] = get_figure(Color.BLACK, FigureType.ROOK)
        board[b_pawn_cord] = get_figure(Color.BLACK, FigureType.PAWN)
        board[b_pawn2_cord] = get_figure(Color.BLACK, FigureType.PAWN)
        board[b_knight_cord] = get_figure(Color.WHITE, FigureType.KNIGHT)

        return board


    def test_castles_move(self):

        w_king_cord = (1, 5)
        w_rook_ks_cord = (1, 8)
        w_rook_qs_cord = (1, 1)

        b_king_cord = (8, 5)
        b_rook_ks_cord = (8, 8)
        b_rook_qs_cord = (8, 1)

        board = dict()

        board[w_king_cord] = get_figure(Color.WHITE, FigureType.KING)
        board[w_rook_ks_cord] = get_figure(Color.WHITE, FigureType.ROOK)
        board[w_rook_qs_cord] = get_figure(Color.WHITE, FigureType.ROOK)

        board[b_king_cord] = get_figure(Color.BLACK, FigureType.KING)
        board[b_rook_ks_cord] = get_figure(Color.BLACK, FigureType.ROOK)
        board[b_rook_qs_cord] = get_figure(Color.BLACK, FigureType.ROOK)

        state = State(board)

        state_changer = StateChanger()

        for row, color in zip([1, 8], [Color.WHITE, Color.BLACK]):
            expected_board = dict()

            if color == Color.WHITE:

                expected_board[(1, 7)] = get_figure(Color.WHITE, FigureType.KING)
                expected_board[(1, 6)] = get_figure(Color.WHITE, FigureType.ROOK)

                expected_board[b_king_cord] = get_figure(Color.BLACK, FigureType.KING)
                expected_board[b_rook_ks_cord] = get_figure(Color.BLACK, FigureType.ROOK)
            else:
                expected_board[w_king_cord] = get_figure(Color.WHITE, FigureType.KING)
                expected_board[w_rook_ks_cord] = get_figure(Color.WHITE, FigureType.ROOK)

                expected_board[(8, 7)] = get_figure(Color.BLACK, FigureType.KING)
                expected_board[(8, 6)] = get_figure(Color.BLACK, FigureType.ROOK)


            expected_board[w_rook_qs_cord] = get_figure(Color.WHITE, FigureType.ROOK)
            expected_board[b_rook_qs_cord] = get_figure(Color.BLACK, FigureType.ROOK)

            expected_state = State(expected_board)

            expected_state.set_has_moved(color, CastleFigureType.KING)
            expected_state.set_has_moved(color, CastleFigureType.ROOK_KINGSIDE)

            kingside_castling = (
                PlyCategory.CASTLE,
                ((row, 5), (row, 7)),
                ((row, 8), (row, 6)),
            )

            new_state = state_changer.get_new_state(color, state, kingside_castling)

            assert expected_state == new_state

        for row, color in zip([1, 8], [Color.WHITE, Color.BLACK]):
            expected_board = dict()

            if color == Color.WHITE:

                expected_board[(1, 3)] = get_figure(Color.WHITE, FigureType.KING)
                expected_board[(1, 4)] = get_figure(Color.WHITE, FigureType.ROOK)

                expected_board[b_king_cord] = get_figure(Color.BLACK, FigureType.KING)
                expected_board[b_rook_qs_cord] = get_figure(Color.BLACK, FigureType.ROOK)
            else:
                expected_board[w_king_cord] = get_figure(Color.WHITE, FigureType.KING)
                expected_board[w_rook_qs_cord] = get_figure(Color.WHITE, FigureType.ROOK)

                expected_board[(8, 3)] = get_figure(Color.BLACK, FigureType.KING)
                expected_board[(8, 4)] = get_figure(Color.BLACK, FigureType.ROOK)


            expected_board[w_rook_ks_cord] = get_figure(Color.WHITE, FigureType.ROOK)
            expected_board[b_rook_ks_cord] = get_figure(Color.BLACK, FigureType.ROOK)

            expected_state = State(expected_board)

            expected_state.set_has_moved(color, CastleFigureType.KING)
            expected_state.set_has_moved(color, CastleFigureType.ROOK_QUEENSIDE)

            queenside_castling = (
                PlyCategory.CASTLE,
                ((row, 5), (row, 3)),
                ((row, 1), (row, 4)),
            )

            new_state = state_changer.get_new_state(color, state, queenside_castling)

            assert expected_state == new_state

    def test_promotion_move(self):
        w_king_cord = (2, 5)
        w_rook_cord = (4, 4)
        w_pawn_cord = (7, 6)

        b_king_cord = (7, 5)
        b_rook_cord = (5, 4)
        b_pawn_cord = (2, 6)

        board = dict()

        board[w_king_cord] = get_figure(Color.WHITE, FigureType.KING)
        board[w_rook_cord] = get_figure(Color.WHITE, FigureType.ROOK)
        board[w_pawn_cord] = get_figure(Color.WHITE, FigureType.PAWN)

        board[b_king_cord] = get_figure(Color.BLACK, FigureType.KING)
        board[b_rook_cord] = get_figure(Color.BLACK, FigureType.ROOK)
        board[b_pawn_cord] = get_figure(Color.BLACK, FigureType.PAWN)

        state = State(board)

        state_changer = StateChanger()

        for row, color in zip([8, 1], [Color.WHITE, Color.BLACK]):
            expected_board = dict()

            if color == Color.WHITE:
                expected_board[(8, 6)] = get_figure(Color.WHITE, FigureType.QUEEN)
                expected_board[b_pawn_cord] = get_figure(Color.BLACK, FigureType.PAWN)
            else:
                expected_board[w_pawn_cord] = get_figure(Color.WHITE, FigureType.PAWN)
                expected_board[(1, 6)] = get_figure(Color.BLACK, FigureType.QUEEN)

            expected_board[w_king_cord] = get_figure(Color.WHITE, FigureType.KING)
            expected_board[w_rook_cord] = get_figure(Color.WHITE, FigureType.ROOK)
            
            expected_board[b_king_cord] = get_figure(Color.BLACK, FigureType.KING)
            expected_board[b_rook_cord] = get_figure(Color.BLACK, FigureType.ROOK)
            
            expected_state = State(expected_board)

            current_row = 7 if color == Color.WHITE else 2
            promotion_move = (
                PlyCategory.PROMOTION,
                ((current_row, 6), (row, 6)),
            )

            new_state = state_changer.get_new_state(color, state, promotion_move)

            assert expected_state == new_state

    def test_knight_take_a_piece(self):
        rook_cord = (5, 4)
        knight_cord = (4, 2)

        board = self._get_casual_board()
        
        
        state_changer = StateChanger()

        for color in [Color.WHITE, Color.BLACK]:
            opposite_color = color.BLACK if color == Color.WHITE else Color.WHITE

            cl_board = dict(board)

            cl_board[knight_cord] = get_figure(opposite_color, FigureType.KNIGHT)
            cl_board[rook_cord] = get_figure(opposite_color, FigureType.ROOK)

            state = State(cl_board)

            expected_board = self._get_casual_board()

            expected_board[rook_cord] = get_figure(opposite_color, FigureType.KNIGHT)

            expected_state = State(expected_board)

            take_a_piece_move = (
                PlyCategory.MOVE,
                (knight_cord, rook_cord),
            )

            new_state = state_changer.get_new_state(color, state, take_a_piece_move)

            assert expected_state == new_state

    def test_bishop_take_a_piece(self):

        bishop_cord = (3, 2)
        rook_cord = (5, 4)
        

        board = self._get_casual_board()
        
        
        state_changer = StateChanger()

        for color in [Color.WHITE, Color.BLACK]:
            opposite_color = color.BLACK if color == Color.WHITE else Color.WHITE

            cl_board = dict(board)

            cl_board[bishop_cord] = get_figure(opposite_color, FigureType.BISHOP)
            cl_board[rook_cord] = get_figure(opposite_color, FigureType.ROOK)

            state = State(cl_board)

            expected_board = self._get_casual_board()

            expected_board[rook_cord] = get_figure(opposite_color, FigureType.BISHOP)

            expected_state = State(expected_board)

            take_a_piece_move = (
                PlyCategory.MOVE,
                (bishop_cord, rook_cord),
            )

            new_state = state_changer.get_new_state(color, state, take_a_piece_move)

            assert expected_state == new_state

    def test_rook_plain_move(self):
        rook_new_cord = (4, 8)
        
        board = self._get_casual_board()
        
        
        state_changer = StateChanger()

        for row, color in zip([1, 8], [Color.WHITE, Color.BLACK]):

            cl_board = dict(board)

            cl_board[(row, 8)] = get_figure(color, FigureType.ROOK)

            state = State(cl_board)

            expected_board = self._get_casual_board()

            expected_board[rook_new_cord] = get_figure(color, FigureType.ROOK)

            expected_state = State(expected_board)

            expected_state.set_has_moved(color, CastleFigureType.ROOK_KINGSIDE)

            plain_move = (
                PlyCategory.MOVE,
                ((row, 8), rook_new_cord),
            )

            new_state = state_changer.get_new_state(color, state, plain_move)

            assert expected_state == new_state
