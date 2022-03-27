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


class TestValidActionsDeterminer:
    def _get_all_castles_board(self):
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

        return board

    def test_all_castles_valid(self):

        board = self._get_all_castles_board()

        state = State(board)

        valid_actions_determiner = ValidActionsDeterminer()

        for row, color in zip([1, 8], [Color.WHITE, Color.BLACK]):

            valid_actions = valid_actions_determiner.get_valid_actions(color, state)

            castling_moves = []

            for action in valid_actions:
                if action[0] == PlyCategory.CASTLE:
                    castling_moves.append(action)

            assert len(castling_moves) == 2

            kingside_castling = (
                PlyCategory.CASTLE,
                ((row, 5), (row, 7)),
                ((row, 8), (row, 6)),
            )
            queenside_castling = (
                PlyCategory.CASTLE,
                ((row, 5), (row, 3)),
                ((row, 1), (row, 4)),
            )

            assert set([kingside_castling, queenside_castling]) == set(castling_moves)

    def test_castles_not_valid_because_of_piece_movement(self):

        board = self._get_all_castles_board()

        valid_actions_determiner = ValidActionsDeterminer()

        for color in [Color.WHITE, Color.BLACK]:

            state = State(board)

            state.set_has_moved(color, CastleFigureType.KING)

            valid_actions = valid_actions_determiner.get_valid_actions(color, state)

            castling_moves = []

            for action in valid_actions:
                if action[0] == PlyCategory.CASTLE:
                    castling_moves.append(action)

            assert len(castling_moves) == 0

        for row, color in zip([1, 8], [Color.WHITE, Color.BLACK]):

            state = State(board)

            state.set_has_moved(color, CastleFigureType.ROOK_KINGSIDE)

            valid_actions = valid_actions_determiner.get_valid_actions(color, state)

            castling_moves = []

            for action in valid_actions:
                if action[0] == PlyCategory.CASTLE:
                    castling_moves.append(action)

            assert len(castling_moves) == 1

            queenside_castling = (
                PlyCategory.CASTLE,
                ((row, 5), (row, 3)),
                ((row, 1), (row, 4)),
            )

            assert set([queenside_castling]) == set(castling_moves)

        for row, color in zip([1, 8], [Color.WHITE, Color.BLACK]):

            state = State(board)

            state.set_has_moved(color, CastleFigureType.ROOK_QUEENSIDE)

            valid_actions = valid_actions_determiner.get_valid_actions(color, state)

            castling_moves = []

            for action in valid_actions:
                if action[0] == PlyCategory.CASTLE:
                    castling_moves.append(action)

            assert len(castling_moves) == 1

            kingside_castling = (
                PlyCategory.CASTLE,
                ((row, 5), (row, 7)),
                ((row, 8), (row, 6)),
            )

            assert set([kingside_castling]) == set(castling_moves)

    def test_castles_not_valid_because_current_check(self):

        board = self._get_all_castles_board()

        valid_actions_determiner = ValidActionsDeterminer()

        w_bishop_cord = (5, 8)
        b_bishop_cord = (4, 8)

        board[w_bishop_cord] = get_figure(Color.WHITE, FigureType.BISHOP)

        board[b_bishop_cord] = get_figure(Color.BLACK, FigureType.BISHOP)

        for color in [Color.WHITE, Color.BLACK]:

            state = State(board)

            state.set_has_moved(color, CastleFigureType.KING)

            valid_actions = valid_actions_determiner.get_valid_actions(color, state)

            castling_moves = []

            for action in valid_actions:
                if action[0] == PlyCategory.CASTLE:
                    castling_moves.append(action)

            assert len(castling_moves) == 0

    def test_only_one_castles_because_path_check(self):

        valid_actions_determiner = ValidActionsDeterminer()

        for cord in [(4, 4), (4, 3), (4, 6), (4, 7)]:
            for color in [Color.WHITE, Color.BLACK]:

                board = self._get_all_castles_board()

                opposite_color = color.BLACK if color == Color.WHITE else Color.WHITE

                board[cord] = get_figure(opposite_color, FigureType.ROOK)

                state = State(board)

                valid_actions = valid_actions_determiner.get_valid_actions(color, state)

                castling_moves = []

                for action in valid_actions:
                    if action[0] == PlyCategory.CASTLE:
                        castling_moves.append(action)

                assert len(castling_moves) == 1

    def test_zero_castles_because_path_check(self):

        valid_actions_determiner = ValidActionsDeterminer()

        for cord1 in [(4, 4), (4, 3)]:
            for cord2 in [(4, 6), (4, 7)]:
                for color in [Color.WHITE, Color.BLACK]:

                    board = self._get_all_castles_board()

                    opposite_color = (
                        color.BLACK if color == Color.WHITE else Color.WHITE
                    )

                    board[cord1] = get_figure(opposite_color, FigureType.ROOK)
                    board[cord2] = get_figure(opposite_color, FigureType.ROOK)

                    state = State(board)

                    valid_actions = valid_actions_determiner.get_valid_actions(
                        color, state
                    )

                    castling_moves = []

                    for action in valid_actions:
                        if action[0] == PlyCategory.CASTLE:
                            castling_moves.append(action)

                    assert len(castling_moves) == 0

    def test_check_and_piece_to_capture_possible(self):

        valid_actions_determiner = ValidActionsDeterminer()

        for color in [Color.WHITE, Color.BLACK]:

            opposite_color = color.BLACK if color == Color.WHITE else Color.WHITE

            ch_king_cord = (3, 3)
            ch_knight_nm_cord = (5, 3)
            ch_knight_cp_cord = (3, 7)
            ch_bishop_cord = (2, 7)

            atk_king_cord = (7, 5)
            atk_rook_cord = (7, 3)
            atk_knight_cord = (4, 5)

            b_pawn_cord = (5, 4)
            w_pawn_cord = (3, 4)

            board = {}

            board[ch_king_cord] = get_figure(color, FigureType.KING)
            board[ch_knight_nm_cord] = get_figure(color, FigureType.KNIGHT)
            board[ch_knight_cp_cord] = get_figure(color, FigureType.KNIGHT)
            board[ch_bishop_cord] = get_figure(color, FigureType.BISHOP)

            board[atk_king_cord] = get_figure(opposite_color, FigureType.KING)
            board[atk_rook_cord] = get_figure(opposite_color, FigureType.ROOK)
            board[atk_knight_cord] = get_figure(opposite_color, FigureType.KNIGHT)

            board[w_pawn_cord] = get_figure(Color.WHITE, FigureType.PAWN)
            board[b_pawn_cord] = get_figure(Color.BLACK, FigureType.PAWN)

            state = State(board)

            valid_actions = valid_actions_determiner.get_valid_actions(color, state)

            expected_actions = [
                (PlyCategory.MOVE, (ch_king_cord, (4, 4))),
                (PlyCategory.MOVE, (ch_king_cord, (4, 2))),
                (PlyCategory.MOVE, (ch_king_cord, (2, 3))),
                (PlyCategory.MOVE, (ch_king_cord, (2, 2))),
                (PlyCategory.MOVE, (ch_king_cord, (3, 2))),
                (PlyCategory.MOVE, (ch_knight_cp_cord, atk_knight_cord)),
                (PlyCategory.MOVE, (ch_bishop_cord, atk_knight_cord)),
            ]

            if color == Color.WHITE:
                expected_actions.append(
                    (PlyCategory.MOVE, (w_pawn_cord, atk_knight_cord))
                )
            else:
                expected_actions.append(
                    (PlyCategory.MOVE, (b_pawn_cord, atk_knight_cord))
                )
                expected_actions.append((PlyCategory.MOVE, (ch_king_cord, w_pawn_cord)))

            print(valid_actions)
            assert set(valid_actions) == set(expected_actions)
