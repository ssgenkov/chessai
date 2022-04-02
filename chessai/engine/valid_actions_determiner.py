from chessai.moves.move import Move
from chessai.moves.ply_category import PlyCategory
from chessai.engine.king_vision import KingVision
from chessai.engine.state import State
from chessai.engine.check_analyst import CheckAnalyst
from chessai.figures.figure_type import FigureType
from chessai.figures.factory import get_figure
from chessai.utils.color import Color
from chessai.moves.move import CURNT, DEST
from chessai.utils.cord import ROW, COLUMN
from chessai.utils.castle_figures import CastleFigureType, get_init_coord


class ValidActionsDeterminer:
    def __init__(self):
        self._check_analyst = CheckAnalyst()

    def get_valid_actions(self, color, state):
        king_vision = KingVision(color, state)

        check_analysis = self._check_analyst.get_analysis(color, state, king_vision)

        if check_analysis.there_is_check:
            valid_moves = []
            for move in check_analysis.king_legal_moves:
                valid_moves.append(self.get_ply_category(move))

            if check_analysis.cord_of_piece_to_capture != None:
                for cord in state.get_pieces_cords_for_color(color):
                    figure = state.get_figure_by_cord(cord)
                    potential_moves = figure.get_potential_moves(state, cord)
                    for move in potential_moves:
                        if (
                            move[DEST] == check_analysis.cord_of_piece_to_capture
                            or move[DEST] in check_analysis.interposing_dest_coordinates
                        ) and not self._move_lead_to_own_check(color, state, move):
                            valid_moves.append(self.get_ply_category(move, figure))

            return valid_moves

        else:
            valid_moves = []
            for cord in state.get_pieces_cords_for_color(color):
                figure = state.get_figure_by_cord(cord)
                potential_moves = figure.get_potential_moves(state, cord)

                if (
                    cord in king_vision.get_vision()
                    or figure.figure_type == FigureType.KING
                ):
                    for move in potential_moves:
                        if not self._move_lead_to_own_check(color, state, move):
                            valid_moves.append(self.get_ply_category(move, figure))
                else:
                    for move in potential_moves:
                        valid_moves.append(self.get_ply_category(move, figure))

            if not state.has_moved(color, CastleFigureType.KING):

                for direction, rook_type in zip(
                    [1, -1],
                    [
                        CastleFigureType.ROOK_KINGSIDE,
                        CastleFigureType.ROOK_QUEENSIDE,
                    ],
                ):
                    rook_was_moved = state.has_moved(color, rook_type)
                    if not rook_was_moved:
                        row = 1 if color == Color.WHITE else 8
                        castling_valid = True

                        king_cords = get_init_coord(color, CastleFigureType.KING)
                        col_to_check = king_cords[COLUMN] + direction
                        rook_cords = get_init_coord(color, rook_type)

                        while col_to_check != rook_cords[COLUMN]:
                            if state.get_figure_by_cord(
                                (rook_cords[ROW], col_to_check)
                            ):
                                castling_valid = False
                                break
                            else:
                                col_to_check += direction

                        if castling_valid:
                            for col_inc in [1, 2]:
                                move = ((row, 5), (row, 5 + direction * col_inc))
                                if self._move_lead_to_own_check(color, state, move):
                                    castling_valid = False

                        if castling_valid:
                            move_king = (
                                (row, 5),
                                (
                                    row,
                                    5 + direction * 2,
                                ),
                            )
                            move_rook = (
                                (
                                    row,
                                    8 if direction == 1 else 1,
                                ),
                                (row, 5 + direction),
                            )
                            valid_moves.append(
                                (PlyCategory.CASTLE, move_king, move_rook)
                            )

            return valid_moves

    def _move_lead_to_own_check(self, color, state, move):
        figure = state.get_figure_by_cord(move[CURNT])
        state_copy = state.get_copy()
        state_copy.remove_figure_by_cord(move[CURNT])
        state_copy.add_figure(move[DEST], figure)
        king_vision_copy = KingVision(color, state_copy)
        return (
            len(
                self._check_analyst.get_checking_pieces(
                    color, state_copy, king_vision_copy
                )
            )
            != 0
        )

    def get_ply_category(self, move, figure=None):
        if figure and figure.figure_type == FigureType.PAWN:
            if move[DEST][ROW] == 8 or move[DEST][ROW] == 1:
                return (PlyCategory.PROMOTION, move)
            else:
                return (PlyCategory.MOVE, move)
        else:
            return (PlyCategory.MOVE, move)
