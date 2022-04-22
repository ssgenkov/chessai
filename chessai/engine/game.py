from chessai.engine.valid_actions_determiner import ValidActionsDeterminer
from chessai.engine.state_evaluator import StateEvaluator
from chessai.engine.state_changer import StateChanger
from chessai.utils.color import Color


class Game:
    def __init__(self, to_move=Color.WHITE):
        self._to_move = to_move

        self._valid_actions_determiner = ValidActionsDeterminer()
        self._state_evaluator = StateEvaluator()
        self._state_changer = StateChanger()

    def get_actions(self, color, state):
        return self._valid_actions_determiner.get_valid_actions(color, state)

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
        return self._state_evaluator.evaluate(color, state) - self._state_evaluator.evaluate(opposite_color, state)

    def to_move(self, state):
        return self._to_move

    def get_result(self, color, state, action):
        return self._state_changer.get_new_state(color, state, action)
