from chessai.figures.figure_type import FigureType
from chessai.figures.factory import get_figure
from chessai.utils.color import Color
from chessai.engine.state_evaluator import StateEvaluator
from chessai.engine.state import State


class TestStateEvaluator:
    def test_scores(self):
        board = dict()

        board[(1, 5)] = get_figure(Color.WHITE, FigureType.KING)
        board[(2, 4)] = get_figure(Color.WHITE, FigureType.QUEEN)
        board[(2, 7)] = get_figure(Color.WHITE, FigureType.ROOK)
        board[(3, 3)] = get_figure(Color.WHITE, FigureType.ROOK)
        board[(4, 5)] = get_figure(Color.WHITE, FigureType.BISHOP)
        board[(5, 1)] = get_figure(Color.WHITE, FigureType.KNIGHT)
        board[(5, 7)] = get_figure(Color.WHITE, FigureType.KNIGHT)
        board[(2, 6)] = get_figure(Color.WHITE, FigureType.PAWN)
        board[(3, 5)] = get_figure(Color.WHITE, FigureType.PAWN)

        board[(8, 5)] = get_figure(Color.BLACK, FigureType.KING)
        board[(7, 3)] = get_figure(Color.BLACK, FigureType.QUEEN)
        board[(8, 4)] = get_figure(Color.BLACK, FigureType.ROOK)
        board[(6, 1)] = get_figure(Color.BLACK, FigureType.BISHOP)
        board[(6, 8)] = get_figure(Color.BLACK, FigureType.BISHOP)
        board[(5, 3)] = get_figure(Color.BLACK, FigureType.KNIGHT)
        board[(6, 6)] = get_figure(Color.BLACK, FigureType.KNIGHT)
        board[(7, 4)] = get_figure(Color.BLACK, FigureType.PAWN)
        board[(5, 5)] = get_figure(Color.BLACK, FigureType.PAWN)

        state = State(board)

        state_evaluator = StateEvaluator()

        white_score = state_evaluator.evaluate(Color.WHITE, state)

        assert 32.19 == white_score

        black_score = state_evaluator.evaluate(Color.BLACK, state)

        assert 29.89 == black_score
