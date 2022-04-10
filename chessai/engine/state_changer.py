from chessai.moves.ply_category import PlyCategory
from chessai.utils.castle_figures import CastleFigureType, get_init_coord
from chessai.moves.move import CURNT, DEST
from chessai.figures.figure_type import FigureType
from chessai.figures.factory import get_figure


class StateChanger:
    def get_new_state(self, color, state, action):

        new_state = state.get_copy()

        ply_category = action[0]

        if ply_category == PlyCategory.CASTLE:
            move_king = action[1]
            move_rook = action[2]

            new_state.set_has_moved(color, CastleFigureType.KING)
            if move_rook[CURNT] == get_init_coord(
                color, CastleFigureType.ROOK_KINGSIDE
            ):
                new_state.set_has_moved(color, CastleFigureType.ROOK_KINGSIDE)
            else:
                new_state.set_has_moved(color, CastleFigureType.ROOK_QUEENSIDE)

            self._apply_move(new_state, move_king)
            self._apply_move(new_state, move_rook)
        elif ply_category == PlyCategory.PROMOTION:
            move = action[1]
            self._apply_move(new_state, move)
            new_state.remove_figure_by_cord(move[DEST])
            new_state.add_figure(move[DEST], get_figure(color, FigureType.QUEEN))
        elif ply_category == PlyCategory.MOVE:
            move = action[1]
            figure_to_move = new_state.get_figure_by_cord(move[CURNT])
            if figure_to_move.figure_type == FigureType.KING:
                new_state.set_has_moved(color, CastleFigureType.KING)
            elif figure_to_move.figure_type == FigureType.ROOK:
                if move[CURNT] == get_init_coord(
                    color, CastleFigureType.ROOK_KINGSIDE
                ):
                    new_state.set_has_moved(color, CastleFigureType.ROOK_KINGSIDE)
                elif move[CURNT] == get_init_coord(
                    color, CastleFigureType.ROOK_QUEENSIDE
                ):
                    new_state.set_has_moved(color, CastleFigureType.ROOK_QUEENSIDE)

            self._apply_move(new_state, move)
        else:
            raise Exception(
                f"{ply_category} is currently not one of the expected ply categories"
            )

        return new_state

    def _apply_move(self, state, move):
        state.remove_figure_by_cord(move[DEST])
        figure_to_move = state.get_figure_by_cord(move[CURNT])
        state.remove_figure_by_cord(move[CURNT])
        state.add_figure(move[DEST], figure_to_move)

        return state
