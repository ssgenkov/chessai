from abc import ABC, abstractmethod


class Figure(ABC):
    def __init__(self, color, figure_type):
        self.color = color
        self.figure_type = figure_type

    @abstractmethod
    def get_possible_moves(self, state, col, row):
        pass

    def _is_in_the_board(self, row, col):
        return row > 0 and row < 9 and col > 0 and col < 9
