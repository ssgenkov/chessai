from chessai.figures.qrb_piece import QRBPiece
from chessai.figures.figure_type import FigureType


class Bishop(QRBPiece):
    def __init__(self, color):
        super().__init__(color, FigureType.BISHOP, {})
