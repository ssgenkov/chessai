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

    def test_only_one_castle_because_piece_in_between(self):

        valid_actions_determiner = ValidActionsDeterminer()

        for col in [2, 7]:
            for color in [Color.WHITE, Color.BLACK]:
                row = 1 if color == Color.WHITE else 8
                board = self._get_all_castles_board()

                board[(row, col)] = get_figure(color, FigureType.BISHOP)

                state = State(board)

                valid_actions = valid_actions_determiner.get_valid_actions(color, state)

                castling_moves = []

                for action in valid_actions:
                    if action[0] == PlyCategory.CASTLE:
                        castling_moves.append(action)

                assert len(castling_moves) == 1

    def test_only_zero_castles_because_piece_in_between(self):

        valid_actions_determiner = ValidActionsDeterminer()

        for color in [Color.WHITE, Color.BLACK]:
            row = 1 if color == Color.WHITE else 8
            board = self._get_all_castles_board()
            board[(row, 2)] = get_figure(color, FigureType.BISHOP)
            board[(row, 7)] = get_figure(color, FigureType.BISHOP)

            state = State(board)
            valid_actions = valid_actions_determiner.get_valid_actions(color, state)
            castling_moves = []
            for action in valid_actions:
                if action[0] == PlyCategory.CASTLE:
                    castling_moves.append(action)
            assert len(castling_moves) == 0

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

    def test_check_and_intercept_possible(self):

        valid_actions_determiner = ValidActionsDeterminer()

        for color in [Color.WHITE, Color.BLACK]:

            opposite_color = color.BLACK if color == Color.WHITE else Color.WHITE

            ch_king_cord = (3, 5)
            ch_knight_nm_cord = (5, 5)
            ch_knight_incp_cord = (2, 6)
            ch_bishop_cord = (1, 6)
            ch_rook_nm_cord = (6, 2)
            ch_rook_incp_cord = (6, 4)

            atk_king_cord = (8, 5)
            atk_queen_cord = (3, 1)
            atk_rook_cord = (7, 5)
            atk_bishop_cord = (7, 1)

            b_pawn_cord = (4, 3)
            w_pawn_cord = (2, 3)

            board = {}

            board[ch_king_cord] = get_figure(color, FigureType.KING)
            board[ch_knight_nm_cord] = get_figure(color, FigureType.KNIGHT)
            board[ch_knight_incp_cord] = get_figure(color, FigureType.KNIGHT)
            board[ch_rook_nm_cord] = get_figure(color, FigureType.ROOK)
            board[ch_rook_incp_cord] = get_figure(color, FigureType.ROOK)
            board[ch_bishop_cord] = get_figure(color, FigureType.BISHOP)

            board[atk_king_cord] = get_figure(opposite_color, FigureType.KING)
            board[atk_queen_cord] = get_figure(opposite_color, FigureType.QUEEN)
            board[atk_rook_cord] = get_figure(opposite_color, FigureType.ROOK)
            board[atk_bishop_cord] = get_figure(opposite_color, FigureType.BISHOP)

            board[w_pawn_cord] = get_figure(Color.WHITE, FigureType.PAWN)
            board[b_pawn_cord] = get_figure(Color.BLACK, FigureType.PAWN)

            state = State(board)

            valid_actions = valid_actions_determiner.get_valid_actions(color, state)

            expected_actions = [
                (PlyCategory.MOVE, (ch_king_cord, (4, 6))),
                (PlyCategory.MOVE, (ch_king_cord, (4, 5))),
                (PlyCategory.MOVE, (ch_king_cord, (4, 4))),
                (PlyCategory.MOVE, (ch_king_cord, (2, 5))),
                (PlyCategory.MOVE, (ch_king_cord, (2, 4))),
                (PlyCategory.MOVE, (ch_rook_incp_cord, (3, 4))),
                (PlyCategory.MOVE, (ch_bishop_cord, (3, 4))),
                (PlyCategory.MOVE, (ch_knight_incp_cord, (3, 4))),
            ]

            if color == Color.WHITE:
                expected_actions.append((PlyCategory.MOVE, (w_pawn_cord, (3, 3))))
            else:
                expected_actions.append((PlyCategory.MOVE, (b_pawn_cord, (3, 3))))

            assert set(valid_actions) == set(expected_actions)

    def test_check_and_only_king_move_possible(self):

        valid_actions_determiner = ValidActionsDeterminer()

        for color in [Color.WHITE, Color.BLACK]:

            opposite_color = color.BLACK if color == Color.WHITE else Color.WHITE

            ch_king_cord = (3, 5)
            ch_knight_nm_cord = (5, 5)
            ch_knight_incp_cord = (2, 6)
            ch_bishop_cord = (1, 6)
            ch_rook_nm_cord = (6, 2)
            ch_rook_incp_cord = (6, 4)

            atk_king_cord = (8, 5)
            atk_queen_cord = (3, 1)
            atk_rook_cord = (7, 5)
            atk_bishop_cord = (7, 1)
            atk_knight_cord = (4, 7)

            b_pawn_cord = (4, 3)
            w_pawn_cord = (2, 3)

            board = {}

            board[ch_king_cord] = get_figure(color, FigureType.KING)
            board[ch_rook_nm_cord] = get_figure(color, FigureType.ROOK)
            board[ch_rook_incp_cord] = get_figure(color, FigureType.ROOK)
            board[ch_bishop_cord] = get_figure(color, FigureType.BISHOP)
            board[ch_knight_nm_cord] = get_figure(color, FigureType.KNIGHT)
            board[ch_knight_incp_cord] = get_figure(color, FigureType.KNIGHT)

            board[atk_king_cord] = get_figure(opposite_color, FigureType.KING)
            board[atk_queen_cord] = get_figure(opposite_color, FigureType.QUEEN)
            board[atk_rook_cord] = get_figure(opposite_color, FigureType.ROOK)
            board[atk_bishop_cord] = get_figure(opposite_color, FigureType.BISHOP)
            board[atk_knight_cord] = get_figure(opposite_color, FigureType.KNIGHT)

            board[w_pawn_cord] = get_figure(Color.WHITE, FigureType.PAWN)
            board[b_pawn_cord] = get_figure(Color.BLACK, FigureType.PAWN)

            state = State(board)

            valid_actions = valid_actions_determiner.get_valid_actions(color, state)

            expected_actions = [
                (PlyCategory.MOVE, (ch_king_cord, (4, 6))),
                (PlyCategory.MOVE, (ch_king_cord, (4, 5))),
                (PlyCategory.MOVE, (ch_king_cord, (4, 4))),
                (PlyCategory.MOVE, (ch_king_cord, (2, 5))),
                (PlyCategory.MOVE, (ch_king_cord, (2, 4))),
            ]

            print("HERE")
            print(valid_actions)
            assert set(valid_actions) == set(expected_actions)

    def test_checkmate(self):

        valid_actions_determiner = ValidActionsDeterminer()

        for color in [Color.WHITE, Color.BLACK]:

            opposite_color = color.BLACK if color == Color.WHITE else Color.WHITE

            ch_king_cord = (3, 5)
            ch_rook_nm_cord = (7, 2)

            atk_king_cord = (1, 8)
            atk_queen_cord = (3, 7)
            atk_rook1_cord = (4, 3)
            atk_rook2_cord = (2, 3)

            board = {}

            board[ch_king_cord] = get_figure(color, FigureType.KING)
            board[ch_rook_nm_cord] = get_figure(color, FigureType.ROOK)

            board[atk_king_cord] = get_figure(opposite_color, FigureType.KING)
            board[atk_queen_cord] = get_figure(opposite_color, FigureType.QUEEN)
            board[atk_rook1_cord] = get_figure(opposite_color, FigureType.ROOK)
            board[atk_rook2_cord] = get_figure(opposite_color, FigureType.ROOK)

            state = State(board)

            valid_actions = valid_actions_determiner.get_valid_actions(color, state)

            assert len(valid_actions) == 0

    def test_initial_board_moves(self):

        valid_actions_determiner = ValidActionsDeterminer()

        board = {}
        for color, direction in zip([Color.WHITE, Color.BLACK], [1, -1]):
            first_row = 1 if color == Color.WHITE else 8
            second_row = first_row + direction

            for i in range(1, 9):
                board[(second_row, i)] = get_figure(color, FigureType.PAWN)

            board[(first_row, 5)] = get_figure(color, FigureType.KING)
            board[(first_row, 4)] = get_figure(color, FigureType.QUEEN)
            board[(first_row, 1)] = get_figure(color, FigureType.ROOK)
            board[(first_row, 8)] = get_figure(color, FigureType.ROOK)
            board[(first_row, 3)] = get_figure(color, FigureType.BISHOP)
            board[(first_row, 6)] = get_figure(color, FigureType.BISHOP)
            board[(first_row, 2)] = get_figure(color, FigureType.KNIGHT)
            board[(first_row, 7)] = get_figure(color, FigureType.KNIGHT)

        state = State(board)

        for color, direction in zip([Color.WHITE, Color.BLACK], [1, -1]):
            first_row = 1 if color == Color.WHITE else 8
            second_row = first_row + direction

            expected_actions = [
                (PlyCategory.MOVE, ((first_row, 2), (first_row + 2 * direction, 3))),
                (PlyCategory.MOVE, ((first_row, 2), (first_row + 2 * direction, 1))),
                (PlyCategory.MOVE, ((first_row, 7), (first_row + 2 * direction, 6))),
                (PlyCategory.MOVE, ((first_row, 7), (first_row + 2 * direction, 8))),
            ]

            for i in range(1, 9):
                for sq in [1, 2]:
                    pawn_move = (
                        PlyCategory.MOVE,
                        ((second_row, i), (second_row + sq * direction, i)),
                    )
                    expected_actions.append(pawn_move)

            valid_actions = valid_actions_determiner.get_valid_actions(color, state)

            assert set(valid_actions) == set(expected_actions)

    def test_casual_state_move_possible(self):

        valid_actions_determiner = ValidActionsDeterminer()

        w_king_cord = (2, 4)
        w_rook_cord = (3, 3)
        w_bishop_cord = (5, 7)
        w_knight_nm_cord = (5, 4)
        w_knight_cord = (4, 6)
        w_pawn_prom_cord = (7, 7)
        w_pawn_cord = (2, 7)

        b_king_cord = (7, 6)
        b_queen_cord = (6, 5)
        b_rook_cord = (6, 4)
        b_bishop_cord = (6, 7)
        b_pawn_nm_cord = (7, 4)
        b_pawn_cord = (4, 2)

        board = {}

        board[w_king_cord] = get_figure(Color.WHITE, FigureType.KING)
        board[w_rook_cord] = get_figure(Color.WHITE, FigureType.ROOK)
        board[w_bishop_cord] = get_figure(Color.WHITE, FigureType.BISHOP)
        board[w_knight_nm_cord] = get_figure(Color.WHITE, FigureType.KNIGHT)
        board[w_knight_cord] = get_figure(Color.WHITE, FigureType.KNIGHT)
        board[w_pawn_prom_cord] = get_figure(Color.WHITE, FigureType.PAWN)
        board[w_pawn_cord] = get_figure(Color.WHITE, FigureType.PAWN)

        board[b_king_cord] = get_figure(Color.BLACK, FigureType.KING)
        board[b_queen_cord] = get_figure(Color.BLACK, FigureType.QUEEN)
        board[b_rook_cord] = get_figure(Color.BLACK, FigureType.ROOK)
        board[b_bishop_cord] = get_figure(Color.BLACK, FigureType.BISHOP)
        board[b_pawn_nm_cord] = get_figure(Color.BLACK, FigureType.PAWN)
        board[b_pawn_cord] = get_figure(Color.BLACK, FigureType.PAWN)

        all_has_moved = set(
            [
                CastleFigureType.KING,
                CastleFigureType.ROOK_KINGSIDE,
                CastleFigureType.ROOK_QUEENSIDE,
            ]
        )
        state = State(
            board, has_moved={Color.WHITE: all_has_moved, Color.BLACK: all_has_moved}
        )

        w_king_moves = [
            (PlyCategory.MOVE, (w_king_cord, (1, 4))),
            (PlyCategory.MOVE, (w_king_cord, (1, 3))),
        ]

        w_rook_moves = [
            (PlyCategory.MOVE, (w_rook_cord, (2, 3))),
            (PlyCategory.MOVE, (w_rook_cord, (1, 3))),
            (PlyCategory.MOVE, (w_rook_cord, (3, 2))),
            (PlyCategory.MOVE, (w_rook_cord, (3, 1))),
        ]

        for col in range(w_rook_cord[COLUMN] + 1, 9):
            rook_move = (PlyCategory.MOVE, (w_rook_cord, (w_rook_cord[ROW], col)))
            w_rook_moves.append(rook_move)

        for row in range(w_rook_cord[ROW] + 1, 9):
            rook_move = (PlyCategory.MOVE, (w_rook_cord, (row, w_rook_cord[COLUMN])))
            w_rook_moves.append(rook_move)

        w_knight_moves = [
            (PlyCategory.MOVE, (w_knight_cord, (5, 8))),
            (PlyCategory.MOVE, (w_knight_cord, (3, 8))),
            (PlyCategory.MOVE, (w_knight_cord, (6, 5))),
            (PlyCategory.MOVE, (w_knight_cord, (6, 7))),
            (PlyCategory.MOVE, (w_knight_cord, (3, 4))),
            (PlyCategory.MOVE, (w_knight_cord, (2, 5))),
        ]

        w_bishop_moves = [
            (PlyCategory.MOVE, (w_bishop_cord, (4, 8))),
            (PlyCategory.MOVE, (w_bishop_cord, (6, 6))),
            (PlyCategory.MOVE, (w_bishop_cord, (7, 5))),
            (PlyCategory.MOVE, (w_bishop_cord, (8, 4))),
            (PlyCategory.MOVE, (w_bishop_cord, (6, 8))),
        ]

        w_pawn_prom_moves = [
            (PlyCategory.PROMOTION, (w_pawn_prom_cord, (8, 7))),
        ]

        w_pawn_moves = [
            (PlyCategory.MOVE, (w_pawn_cord, (3, 7))),
            (PlyCategory.MOVE, (w_pawn_cord, (4, 7))),
        ]

        expected_actions_white = []

        expected_actions_white.extend(w_king_moves)
        expected_actions_white.extend(w_rook_moves)
        expected_actions_white.extend(w_knight_moves)
        expected_actions_white.extend(w_bishop_moves)
        expected_actions_white.extend(w_pawn_prom_moves)
        expected_actions_white.extend(w_pawn_moves)

        valid_actions_white = valid_actions_determiner.get_valid_actions(
            Color.WHITE, state
        )

        assert set(valid_actions_white) == set(expected_actions_white)

        b_king_moves = [
            (PlyCategory.MOVE, (b_king_cord, (8, 5))),
            (PlyCategory.MOVE, (b_king_cord, (8, 7))),
            (PlyCategory.MOVE, (b_king_cord, (7, 7))),
        ]

        b_queen_moves = [
            (PlyCategory.MOVE, (b_queen_cord, (7, 5))),
            (PlyCategory.MOVE, (b_queen_cord, (8, 5))),
            (PlyCategory.MOVE, (b_queen_cord, (6, 6))),
            (PlyCategory.MOVE, (b_queen_cord, (5, 4))),
        ]

        for row in range(b_queen_cord[ROW] - 1, 0, -1):
            queen_move = (PlyCategory.MOVE, (b_queen_cord, (row, 5)))
            b_queen_moves.append(queen_move)

        for mv in range(1, 4):
            queen_move = (
                PlyCategory.MOVE,
                (b_queen_cord, (b_queen_cord[ROW] - mv, b_queen_cord[COLUMN] + mv)),
            )
            b_queen_moves.append(queen_move)

        b_rook_moves = [
            (PlyCategory.MOVE, (b_rook_cord, (5, 4))),
        ]

        for col in range(b_rook_cord[COLUMN] - 1, 0, -1):
            rook_move = (PlyCategory.MOVE, (b_rook_cord, (6, col)))
            b_rook_moves.append(rook_move)

        b_bishop_moves = [
            (PlyCategory.MOVE, (b_bishop_cord, (7, 8))),
            (PlyCategory.MOVE, (b_bishop_cord, (5, 8))),
        ]

        for mv in range(1, 6):
            bishop_move = (
                PlyCategory.MOVE,
                (b_bishop_cord, (b_bishop_cord[ROW] - mv, b_bishop_cord[COLUMN] - mv)),
            )
            b_bishop_moves.append(bishop_move)

        b_pawn_moves = [
            (PlyCategory.MOVE, (b_pawn_cord, (3, 2))),
            (PlyCategory.MOVE, (b_pawn_cord, (3, 3))),
        ]

        expected_actions_black = []

        expected_actions_black.extend(b_king_moves)
        expected_actions_black.extend(b_queen_moves)
        expected_actions_black.extend(b_rook_moves)
        expected_actions_black.extend(b_bishop_moves)
        expected_actions_black.extend(b_pawn_moves)

        valid_actions_black = valid_actions_determiner.get_valid_actions(
            Color.BLACK, state
        )

        assert set(valid_actions_black) == set(expected_actions_black)
