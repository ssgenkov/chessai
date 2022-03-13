from chessai.moves.move import Move


def get_movement(move):
    if move == Move.UP:
        return [1, 0]
    elif move == Move.DOWN:
        return [-1, 0]
    elif move == Move.LEFT:
        return [0, -1]
    elif move == Move.RIGHT:
        return [0, 1]
    elif move == Move.LU_DIAG:
        return [1, -1]
    elif move == Move.RU_DIAG:
        return [1, 1]
    elif move == Move.LD_DIAG:
        return [-1, -1]
    elif move == Move.RD_DIAG:
        return [-1, 1]
