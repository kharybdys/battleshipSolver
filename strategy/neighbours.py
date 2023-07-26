from analysis import BattleshipBoardEntry, Status
from strategy.abstract import AbstractStrategy


class ObeyNeighbours(AbstractStrategy):
    def _if_unknown_set_empty(self, x: int, y: int, entry: BattleshipBoardEntry):
        if entry.unknown:
            entry.set_empty(self.change_tracker)
        elif entry.filled:
            raise ValueError(f"One of the neighbours around coordinates {x}, {y} expected to be empty but is filled!")

    def solve(self):
        for x, y, entry in self.board.iterate():
            if entry.filled:
                for diagonal_neighbour in self.board.get_diagonal_neighbours(x, y):
                    self._if_unknown_set_empty(x=x, y=y, entry=diagonal_neighbour)
                left, right, top, bottom = self.board.get_neighbours(x, y)
                expected_empty: list[BattleshipBoardEntry] = []
                match entry.status:
                    case Status.FILLED_SQUARE:
                        if top.empty:
                            expected_empty.append(bottom)
                        if bottom.empty:
                            expected_empty.append(top)
                        if left.empty:
                            expected_empty.append(right)
                        if right.empty:
                            expected_empty.append(left)
                    case Status.FILLED_END_LEFT:
                        expected_empty.extend([left, top, bottom])
                    case Status.FILLED_END_RIGHT:
                        expected_empty.extend([right, top, bottom])
                    case Status.FILLED_END_TOP:
                        expected_empty.extend([left, right, top])
                    case Status.FILLED_END_BOTTOM:
                        expected_empty.extend([left, right, bottom])
                    case Status.FILLED_SINGLE:
                        expected_empty.extend([left, right, top, bottom])
                    case _:
                        pass
                for should_be_empty in expected_empty:
                    self._if_unknown_set_empty(x=x, y=y, entry=should_be_empty)
