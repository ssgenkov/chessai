from chessai.utils.color import Color
from multiprocessing import Pool

class HeuristicAlphaBetaSearch:
    def __init__(self, max_depth, processes_num=6):
        self._max_depth = max_depth
        self._processes_num = processes_num

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

        if depth == 1:
            actions = game.get_actions(color, state)
            chunks = self._processes_num

            with Pool(processes=self._processes_num) as pool:
                for i in range(0,len(actions)//chunks+1):
                    chunk_actions = actions[i*chunks: (i+1)*chunks]

                    depths = [depth + 1]*len(chunk_actions)
                    opposite_colors = [opposite_color]*len(chunk_actions)
                    games = [game]*len(chunk_actions)
                    results = [game.get_result(color, state, action) for action in chunk_actions]
                    alphas = [alpha]*len(chunk_actions)
                    betas = [beta]*len(chunk_actions)
                    
                    result = pool.starmap(self.min_value,zip(depths,opposite_colors,games,results,alphas,betas))
                    for res, action in zip(result, chunk_actions):
                        v2 = res[0]
                        if v2 > v:
                            v, move = v2, action
                            alpha = max(alpha, v)
                        if v >= beta:
                            return v, move
            return v, move

            # with Pool(processes=6) as pool:
            #         actions = game.get_actions(color, state)

            #         depths = [depth + 1]*len(actions)
            #         opposite_colors = [opposite_color]*len(actions)
            #         games = [game]*len(actions)
            #         results = [game.get_result(color, state, action) for action in actions]
            #         alphas = [alpha]*len(actions)
            #         betas = [beta]*len(actions)
                    
            #         result = pool.starmap(self.min_value,zip(depths,opposite_colors,games,results,alphas,betas))
            #         for res, action in zip(result, actions):
            #             v2 = res[0]
            #             if v2 > v:
            #                 v, move = v2, action
            #                 alpha = max(alpha, v)
            #             if v >= beta:
            #                 return v, move
            # return v, move
                # depths = [depth + 1]*len(actions)
                # opposite_colors = [opposite_color]*len(actions)
                # games = [game]*len(actions)
                # results = [game.get_result(color, state, action) for action in actions]
                # alphas = [alpha]*len(actions)
                # betas = [beta]*len(actions)
                # with Pool(processes=6) as pool:
                #     # print "[0, 1, 4,..., 81]"
                #     result = pool.starmap(self.min_value,zip(depths,opposite_colors,games,results,alphas,betas))
                # for res, action in zip(result, actions):
                #     v2 = res[0]
                #     if v2 > v:
                #         v, move = v2, action
                # return v, move
        else:
            move = None
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
            return game.get_heuristic(color, state), None

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
