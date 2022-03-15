from chessai.figures.qrb_piece import QRBPiece
from chessai.figures.figure_type import FigureType
from chessai.moves.move import Move


class Bishop(QRBPiece):
    def __init__(self, color):
        super().__init__(
            color,
            FigureType.BISHOP,
            set([Move.LU_DIAG, Move.RU_DIAG, Move.LD_DIAG, Move.RD_DIAG]),
        )
