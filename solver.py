from board import BattleshipBoard
from strategy.change_tracker import ChangeTracker
from strategy.filler import FillRowsAndColumns
from strategy.neighbours import ObeyNeighbours
from strategy.unfinished_ships import ExtendUnfinishedShips
from strategy.ships_analysis import tidy, ShipsAnalysis

STRATEGIES = [FillRowsAndColumns, ExtendUnfinishedShips, ObeyNeighbours,  ShipsAnalysis]


def solve(board: BattleshipBoard):
    while True:
        change_tracker = ChangeTracker()
        for strategy_type in STRATEGIES:
            strategy = strategy_type(board, change_tracker)
            strategy.solve()
        if not change_tracker.is_changed():
            tidy(board)
            return
