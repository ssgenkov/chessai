from multiprocessing import Pool
from chessai.figures.figure_type import FigureType
from chessai.figures.factory import get_figure
from chessai.utils.color import Color
from chessai.engine.state_evaluator import StateEvaluator
from chessai.engine.state import State
from chessai.engine.game import Game
from chessai.engine.heuristic_alpha_beta_tree_search import HeuristicAlphaBetaSearch
from chessai.utils.castle_figures import CastleFigureType
import time

if __name__ == '__main__':
    board = dict()

    board[(1, 5)] = get_figure(Color.WHITE, FigureType.KING)
    board[(1, 4)] = get_figure(Color.WHITE, FigureType.QUEEN)
    board[(1, 1)] = get_figure(Color.WHITE, FigureType.ROOK)
    board[(1, 8)] = get_figure(Color.WHITE, FigureType.ROOK)
    board[(1, 2)] = get_figure(Color.WHITE, FigureType.KNIGHT)
    board[(1, 7)] = get_figure(Color.WHITE, FigureType.KNIGHT)
    board[(1, 3)] = get_figure(Color.WHITE, FigureType.BISHOP)
    board[(1, 6)] = get_figure(Color.WHITE, FigureType.BISHOP)
    board[(2, 1)] = get_figure(Color.WHITE, FigureType.PAWN)
    board[(2, 2)] = get_figure(Color.WHITE, FigureType.PAWN)
    board[(2, 3)] = get_figure(Color.WHITE, FigureType.PAWN)
    board[(2, 4)] = get_figure(Color.WHITE, FigureType.PAWN)
    board[(2, 5)] = get_figure(Color.WHITE, FigureType.PAWN)
    board[(2, 6)] = get_figure(Color.WHITE, FigureType.PAWN)
    board[(2, 7)] = get_figure(Color.WHITE, FigureType.PAWN)
    board[(2, 8)] = get_figure(Color.WHITE, FigureType.PAWN)

    board[(8, 5)] = get_figure(Color.BLACK, FigureType.KING)
    board[(8, 4)] = get_figure(Color.BLACK, FigureType.QUEEN)
    board[(8, 1)] = get_figure(Color.BLACK, FigureType.ROOK)
    board[(8, 8)] = get_figure(Color.BLACK, FigureType.ROOK)
    board[(8, 2)] = get_figure(Color.BLACK, FigureType.KNIGHT)
    board[(8, 7)] = get_figure(Color.BLACK, FigureType.KNIGHT)
    board[(8, 3)] = get_figure(Color.BLACK, FigureType.BISHOP)
    board[(8, 6)] = get_figure(Color.BLACK, FigureType.BISHOP)
    board[(7, 1)] = get_figure(Color.BLACK, FigureType.PAWN)
    board[(7, 2)] = get_figure(Color.BLACK, FigureType.PAWN)
    board[(7, 3)] = get_figure(Color.BLACK, FigureType.PAWN)
    board[(7, 4)] = get_figure(Color.BLACK, FigureType.PAWN)
    board[(7, 5)] = get_figure(Color.BLACK, FigureType.PAWN)
    board[(7, 6)] = get_figure(Color.BLACK, FigureType.PAWN)
    board[(7, 7)] = get_figure(Color.BLACK, FigureType.PAWN)
    board[(7, 8)] = get_figure(Color.BLACK, FigureType.PAWN)

    has_moved = {}

    # has_moved_white = set(
    #             [
    #                 CastleFigureType.KING,
    #                 CastleFigureType.ROOK_KINGSIDE,
    #                 CastleFigureType.ROOK_QUEENSIDE,
    #             ]
    #         )
    # has_moved_black = set(
    #             [
    #                 CastleFigureType.KING,
    #                 CastleFigureType.ROOK_KINGSIDE,
    #                 CastleFigureType.ROOK_QUEENSIDE,
    #             ]
    #         )
    # has_moved = {Color.WHITE: has_moved_white, Color.BLACK: has_moved_black}


    state = State(
        board, has_moved=has_moved
            )

    game = Game()
    start = time.time()
    heuristic_AlphaBetaSearch = HeuristicAlphaBetaSearch(max_depth=6, processes_num=8)
    action = heuristic_AlphaBetaSearch.alpha_beta_search(game, state)
    end = time.time()
    print(end - start)
    print(action)


