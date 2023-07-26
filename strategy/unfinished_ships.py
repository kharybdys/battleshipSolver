from analysis import BattleshipBoardEntry, Status
from strategy.abstract import AbstractStrategy


class ExtendUnfinishedShips(AbstractStrategy):
    def _check_and_set_neighbour(self, x: int, y: int, neighbour: BattleshipBoardEntry):
        if neighbour.empty:
            raise ValueError(f"Neighbour on the open end of a FILLED_END_xxx entry is empty, coordinates {x}, {y}")
        elif neighbour.unknown:
            neighbour.set_filled(self.change_tracker)
            return True
        else:
            return False

    def solve(self):
        for x, y, entry in self.board.iterate():
            left, right, top, bottom = self.board.get_neighbours(x, y)
            match entry.status:
                case Status.FILLED_SQUARE:
                    if left.empty and right.empty:
                        # vertical
                        if not top.filled:
                            top.set_filled(self.change_tracker)
                        if not bottom.filled:
                            bottom.set_filled(self.change_tracker)
                    if bottom.empty and top.empty:
                        # horizontal
                        if not left.filled:
                            left.set_filled(self.change_tracker)
                        if not right.filled:
                            right.set_filled(self.change_tracker)
                case Status.FILLED_END_LEFT:
                    self._check_and_set_neighbour(x=x, y=y, neighbour=right)
                case Status.FILLED_END_RIGHT:
                    self._check_and_set_neighbour(x=x, y=y, neighbour=left)
                case Status.FILLED_END_TOP:
                    self._check_and_set_neighbour(x=x, y=y, neighbour=bottom)
                case Status.FILLED_END_BOTTOM:
                    self._check_and_set_neighbour(x=x, y=y, neighbour=top)
                case _:
                    pass
