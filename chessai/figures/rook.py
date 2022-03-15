from chessai.figures.qrb_piece import QRBPiece
from chessai.figures.figure_type import FigureType
from chessai.moves.move import Move


class Rook(QRBPiece):
    def __init__(self, color):
        super().__init__(
            color, FigureType.ROOK, set([Move.UP, Move.DOWN, Move.LEFT, Move.RIGHT])
        )
