from chessai.moves.move import Move, CURNT, DEST
from chessai.moves.moves_factory import get_movement
from chessai.figures.figure_type import FigureType
from chessai.engine.king_vision import KingVision
from chessai.engine.check_analysis import CheckAnalysis
from chessai.engine.state import State
from chessai.utils.color import Color
from chessai.utils.cord import ROW, COLUMN


class CheckAnalyst:
    def get_analysis(self, color, state, king_vision):
        checking_pieces = self.get_checking_pieces(color, state, king_vision)

        king_cord = state.get_figures_cord(color, FigureType.KING)[0]

        there_is_check = len(checking_pieces) != 0
        cord_of_piece_to_capture = None
        interposing_dest_coordinates = []
        if there_is_check:
            if len(checking_pieces) == 1:
                checking_piece = checking_pieces[0]
                cord_of_piece_to_capture = checking_piece[0]
                if checking_piece[1].figure_type in set(
                    [FigureType.QUEEN, FigureType.ROOK, FigureType.BISHOP]
                ):
                    mov_row, mov_col = get_movement(checking_piece[2])
                    interposing_row = king_cord[ROW] + mov_row
                    interposing_col = king_cord[COLUMN] + mov_col
                    while (
                        interposing_row != cord_of_piece_to_capture[ROW]
                        and interposing_col != cord_of_piece_to_capture[COLUMN]
                    ):
                        interposing_dest_coordinates.append(
                            (interposing_row, interposing_col)
                        )
                        interposing_row = interposing_row + mov_row
                        interposing_col = interposing_col + mov_col

        king = state.get_figure_by_cord(king_cord)

        king_potential_moves = king.get_potential_moves(state, king_cord)

        king_legal_moves = []
        for king_move in king_potential_moves:
            board_copy = state.get_board_copy()
            del board_copy[king_move[CURNT]]
            board_copy[king_move[DEST]] = king
            potential_state = State(board_copy)
            potential_king_vision = KingVision(king.color, potential_state)
            if (
                len(
                    self.get_checking_pieces(
                        king.color, potential_state, potential_king_vision
                    )
                )
                == 0
            ):
                king_legal_moves.append(king_move)

        return CheckAnalysis(
            there_is_check,
            cord_of_piece_to_capture,
            interposing_dest_coordinates,
            king_legal_moves,
        )

    def get_checking_pieces(self, color, state, king_vision):
        vision = king_vision.get_vision()
        king_cord = state.get_figures_cord(color, FigureType.KING)[0]
        checking_pieces = []
        qrb_type = set([FigureType.QUEEN, FigureType.ROOK, FigureType.BISHOP])
        for cord in vision:
            figure = vision[cord][0]
            move = vision[cord][1]
            if figure.color != color:
                if figure.figure_type in qrb_type:
                    if move in figure.get_moves():
                        checking_pieces.append((cord, figure, move))
                elif figure.figure_type == FigureType.PAWN:
                    potential_moves = figure.get_potential_moves(state, cord)
                    if king_cord in set((mov[DEST] for mov in potential_moves)):
                        checking_pieces.append((cord, figure, move))

        opponent_color = Color.WHITE if color == Color.BLACK else Color.BLACK
        for cord in state.get_figures_cord(opponent_color, FigureType.KNIGHT):
            figure = state.get_figure_by_cord(cord)
            potential_moves = figure.get_potential_moves(state, cord)
            if king_cord in set((mov[DEST] for mov in potential_moves)):
                checking_pieces.append((cord, figure, None))

        return checking_pieces
