from abc import ABC, abstractmethod


class Figure(ABC):
    def __init__(self, color, figure_type):
        self.color = color
        self.figure_type = figure_type

    @abstractmethod
    def get_potential_moves(self, state, cord):
        pass

    def _is_in_the_board(self, row, col):
        return row > 0 and row < 9 and col > 0 and col < 9

    def __eq__(self, obj):
        return (
            isinstance(obj, Figure)
            and self.color == obj.color
            and self.figure_type == obj.figure_type
        )

    def __hash__(self):
        return hash((self.color, self.figure_type))
