from chessai.figures.qrb_piece import QRBPiece
from chessai.figures.figure_type import FigureType
from chessai.moves.move import Move


class Queen(QRBPiece):
    def __init__(self, color):
        super().__init__(color, FigureType.QUEEN, set([move for move in Move]))
