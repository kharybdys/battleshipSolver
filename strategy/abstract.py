from abc import ABC, abstractmethod

from board import BattleshipBoard
from strategy.change_tracker import ChangeTracker


class AbstractStrategy(ABC):
    def __init__(self, board: BattleshipBoard, change_tracker: ChangeTracker):
        self.board = board
        self.change_tracker = change_tracker

    @abstractmethod
    def solve(self):
        pass
