from chessai.figures.figure_type import FigureType

class StateEvaluator:


    def __init__(self, piece_value=None):

        if piece_value:
            self._piece_value = piece_value
        else:
            self._piece_value = {}
            self._piece_value[FigureType.KING] = 0
            self._piece_value[FigureType.PAWN] = 1
            self._piece_value[FigureType.KNIGHT] = 3.05
            self._piece_value[FigureType.BISHOP] = 3.33
            self._piece_value[FigureType.ROOK] = 5.63
            self._piece_value[FigureType.QUEEN] = 9.5

    def evaluate(self, color, state):
        figures_cords = state.get_pieces_cords_for_color(color)
        
        h_value = 0
        for cords in figures_cords:
            figure = state.get_figure_by_cord(cords)
            h_value += self._piece_value[figure.figure_type]

        return h_value
        
