from audioop import reverse
from chessai.engine.valid_actions_determiner import ValidActionsDeterminer
from chessai.engine.state_evaluator import StateEvaluator
from chessai.engine.state_changer import StateChanger
from chessai.utils.color import Color
from chessai.moves.ply_category import PlyCategory
from chessai.moves.move import CURNT, DEST


class Game:
    def __init__(self, to_move=Color.WHITE):
        self._to_move = to_move

        self._valid_actions_determiner = ValidActionsDeterminer()
        self._state_evaluator = StateEvaluator()
        self._state_changer = StateChanger()

    def get_actions(self, color, state):
        actions = self._valid_actions_determiner.get_valid_actions(color, state)

        ACTION_PLY_CATEGORY = 0
        ACTION_MOVE = 1

        promotions = []
        taking_a_piece = []
        simple_move = []
        for action in actions:
            if action[ACTION_PLY_CATEGORY] == PlyCategory.PROMOTION:
                promotions.append(action)
            elif action[ACTION_PLY_CATEGORY] == PlyCategory.MOVE:
                move = action[ACTION_MOVE]
                figure_dest = state.get_figure_by_cord(move[DEST])
                if figure_dest:
                    taking_a_piece.append((action, figure_dest.figure_type))
                else:
                    simple_move.append(action)
            else:
                simple_move.append(action)

        taking_a_piece.sort(reverse=True, key=lambda x: self._state_evaluator.get_piece_value(x[1]))
        taking_a_piece = [x[0] for x in taking_a_piece]

        return promotions + taking_a_piece + simple_move


    def is_terminal(self, color, state):
        return len(self._valid_actions_determiner.get_valid_actions(color, state)) == 0

    def get_utility(self, color, state):
        if self.is_terminal(color, state):
            if color == self._to_move:
                return float("-inf")
            else:
                return float("inf")
        else:
            return None

    def get_heuristic(self, color, state):
        opposite_color = color.BLACK if color == Color.WHITE else Color.WHITE
        sign = 1 if color == self._to_move else -1
        return sign * (self._state_evaluator.evaluate(color, state) - self._state_evaluator.evaluate(opposite_color, state))

    def to_move(self, state):
        return self._to_move

    def get_result(self, color, state, action):
        return self._state_changer.get_new_state(color, state, action)
