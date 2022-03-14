
from chessai.moves.move import Move
from chessai.moves.moves_factory import get_movement
from chessai.figures.figure_type import FigureType

class CheckAnalysis:

    def __init__(self, color, state, king_vision):
        self._color = color
        self._state = state
        self._king_vision = king_vision
        self._do_analysis()

    def check(self):
        return self._check

    def _do_analysis(self):
        checking_pieces = []
        qrb_type = set([FigureType.QUEEN, FigureType.ROOK, FigureType.BISHOP])
        for cord in self._king_vision:
            figure = self._king_vision[cord][0]
            move = self._king_vision[cord][1]
            if figure.color != self._color:
                if figure.figure_type in qrb_type:
                    if move in figure.get_moves():
                       checking_pieces.append((cord, figure, move))
                 
        