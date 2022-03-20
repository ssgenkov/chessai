from chessai.moves.move import Move
from chessai.engine.king_vision import KingVision
from chessai.engine.state import State
from chessai.engine.check_analyst import CheckAnalyst
from chessai.figures.figure_type import FigureType
from chessai.figures.factory import get_figure
from chessai.utils.color import Color
from chessai.moves.move import CURNT, DEST


class ValidActionsDeterminer:

    def __init__(self):
        self._check_analyst = CheckAnalyst()

    def get_valid_actions(self, color, state):
        king_vision = KingVision(color, state)
        
        check_analysis = self._check_analyst.get_analysis(color, state, king_vision)

        if check_analysis.there_is_check:
        
            if check_analysis.cord_of_piece_to_capture == None:
                return check_analysis.king_legal_moves

            valid_moves = []
            for cord in state.get_pieces_cords_for_color(color):
                figure = state.get_figure_by_cord(cord)
                potential_moves = figure.get_potential_moves(state, cord)
                for move in potential_moves:
                    if move[DEST] == check_analysis.cord_of_piece_to_capture or move[DEST] in check_analysis.interposing_dest_coordinates:
                        valid_moves.append(move)
                
            return valid_moves

        
        else:
            valid_moves = []
            for cord in state.get_pieces_cords_for_color(color):
                figure = state.get_figure_by_cord(cord)
                potential_moves = figure.get_potential_moves(state, cord)
                
                if cord in king_vision.get_vision():
                    for move in potential_moves:
                        if not self._move_lead_to_own_check(color, state, move):
                            valid_moves.append(move)
                        
                else:
                    valid_moves = potential_moves

                potential_moves.extend(valid_moves)
            

            if not state.was_king_moved(color):

                for direction, rook_was_moved in zip([1, -1], [state.was_kingside_rook_moved(color), state.was_queenside_rook_moved(color)]):
                    if  rook_was_moved:
                        row = 1 if Color.WHITE else 8
                        move = [0, 0]
                        kingside_castle_valid = True
                        for col_inc in [1,2]:
                            move[CURNT] = (row, 5)
                            move[DEST] = (row, 5 + direction*col_inc)
                            if state.get_figure_by_cord(move[DEST]) or self._move_lead_to_own_check(color, state, move):
                                kingside_castle_valid = False

                        if kingside_castle_valid:
                            move_king = [0, 0]
                            move_rook = [0, 0]
                            move_king[CURNT], move_king[DEST] = (row, 5) , (row, 5 + direction*2)
                            move_rook[CURNT], move_rook[DEST] = (row, 8 if direction == 1 else 1) , (row, 5 + direction)
                            valid_moves.append((move_king, move_rook))

            return valid_moves

    def _move_lead_to_own_check(self, color, state, move):
        figure = state.get_figure_by_cord(move[CURNT])
        state_copy = state.get_copy()
        del state_copy[move[CURNT]]
        state_copy[move[DEST]] = figure
        king_vision_copy = KingVision(color, state_copy)
        return len(self._check_analyst.get_checking_pieces(color, state_copy, king_vision_copy)) != 0


        
        