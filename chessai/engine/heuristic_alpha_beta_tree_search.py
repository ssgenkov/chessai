from chessai.utils.color import Color

class HeuristicAlphaBetaSearch:
    def __init__(self, max_depth):
        self._max_depth = max_depth

    def alpha_beta_search(self, game, state):
        color = game.to_move(state)
        value, move = self.max_value(1, color, game, state, float("-inf"), float("inf"))

        return value, move

    def max_value(self, depth, color, game, state, alpha, beta):
        if game.is_terminal(color, state):
            return game.get_utility(color, state), None
        if self._max_depth == depth:
            return game.get_heuristic(color, state), None

        v = float("-inf")

        opposite_color = color.BLACK if color == Color.WHITE else Color.WHITE

        for action in game.get_actions(color, state):
            v2, a2 = self.min_value(
                depth + 1,
                opposite_color,
                game,
                game.get_result(color, state, action),
                alpha,
                beta,
            )
            if v2 > v:
                v, move = v2, action
                alpha = max(alpha, v)
            if v >= beta:
                return v, move
        return v, move
        
    def min_value(self, depth, color, game, state, alpha, beta):
        if game.is_terminal(color, state):
            return game.get_utility(color, state), None
        if self._max_depth == depth:
            return (-1)*game.get_heuristic(color, state), None

        v = float("inf")

        opposite_color = color.BLACK if color == Color.WHITE else Color.WHITE
        for action in game.get_actions(color, state):
            v2, a2 = self.max_value(
                depth + 1,
                opposite_color,
                game,
                game.get_result(color, state, action),
                alpha,
                beta,
            )
            if v2 < v:
                v, move = v2, action
                beta = min(beta, v)
            if v <= alpha:
                return v, move
        return v, move
