from collections import defaultdict, Counter

from analysis import AnalysisError, Status, get_filled_status, BattleshipBoardEntry
from board import BattleshipBoard
from strategy.abstract import AbstractStrategy
from strategy.change_tracker import ChangeTracker


def tidy(board: BattleshipBoard):
    ShipsAnalysis.tidy_and_return_possible_ships(board)


class PossibleShip:
    def __init__(self):
        self.entries: list[tuple[int, int, BattleshipBoardEntry]] = []

    def __repr__(self):
        return f"{self.possible_sizes} at entries: {self.entries}"

    def add_entry(self, x: int, y: int, entry: BattleshipBoardEntry):
        if entry.empty:
            raise ValueError(f"Shouldn't be adding an empty entry to a possibleShip, for coordinates {x}, {y}, possibleShip: {self.entries}")
        self.entries.append((x, y, entry))

    def next_to(self, x: int, y: int) -> bool:
        def _next_to_entry(e_x, e_y):
            if e_x == x:
                return self.vertical and abs(e_y - y) == 1
            elif e_y == y:
                return self.horizontal and abs(e_x - x) == 1
            else:
                return False
        return any([_next_to_entry(e_x, e_y) for e_x, e_y, _ in self.entries])

    @property
    def horizontal(self) -> bool:
        if len(self.entries) <= 1:
            return True
        count_ys = Counter(y for _, y, _ in self.entries)
        return len(count_ys.keys()) == 1

    @property
    def vertical(self) -> bool:
        if len(self.entries) <= 1:
            return True
        count_xs = Counter(x for x, _, _ in self.entries)
        return len(count_xs.keys()) == 1

    @property
    def _filled_entries(self) -> list[BattleshipBoardEntry]:
        return [e for _, _, e in self.entries if e.filled]

    @property
    def possible_sizes(self) -> list[int]:
        # TODO: Too simple, doesn't tackle the splittable case
        start = len(self._filled_entries)
        stop = len(self.entries) + 1
        return list(range(start, stop))

    @property
    def partial(self) -> bool:
        return any(self._filled_entries)

    def fill_up_to_size(self, size: int, change_tracker: ChangeTracker):
        leave_empty = len(self.entries) - size
        # we also need to tackle the scenario of say a space of 7 where a ship of 5 needs to be placed,
        # meaning only the middle 3 should be filled. So leave_empty should remain empty on both sides if available.
        for x, y, entry in self.entries[leave_empty:-leave_empty]:
            if entry.unknown:
                entry.set_filled(change_tracker)


class ShipsAnalysis(AbstractStrategy):
    @staticmethod
    def tidy_and_return_possible_ships(board: BattleshipBoard) -> list[PossibleShip]:
        possible_ships: list[PossibleShip] = []
        for x, y, entry in board.iterate():
            if entry.filled:
                left, right, top, bottom = board.get_neighbours(x, y)
                expected_fill_status = get_filled_status(left=left, right=right, top=top, bottom=bottom)
                if expected_fill_status != Status.FILLED:
                    if entry.status != Status.FILLED and not entry.status.equivalent(expected_fill_status) and not expected_fill_status.equivalent(entry.status):
                        raise AnalysisError(f"Invalid intermediate solution, wrong specific fill type, actual: {entry.status}, expected: {expected_fill_status} at coordinates {x}, {y}!")
                    if entry.status.equivalent(expected_fill_status):
                        # Don't overwrite a more specific status with a more generic one
                        entry.status = expected_fill_status
            if not entry.empty:
                ship = next(filter(lambda s: s.next_to(x=x, y=y), possible_ships), None)
                if not ship:
                    ship = PossibleShip()
                    possible_ships.append(ship)
                ship.add_entry(x=x, y=y, entry=entry)
        return possible_ships

    def solve(self):
        possible_ships = self.tidy_and_return_possible_ships(self.board)
        ship_sizes: Counter[int] = Counter(self.board.size.ship_sizes)
        incomplete_ships: list[PossibleShip] = []
        for ship in possible_ships:
            if len(ship.possible_sizes) == 1 and ship.partial:
                size = ship.possible_sizes[0]
                if ship_sizes.get(size, 0):
                    ship_sizes[size] -= 1
                    if ship_sizes[size] == 0:
                        del ship_sizes[size]
                else:
                    raise ValueError(f"Too many ships of size {size} found")
            else:
                incomplete_ships.append(ship)

        # There are only enough possible ships remaining for a given ship size as the amount of ships of that size to still place: Fill those ships up
        possible_ships_by_possible_size: dict[int, list[PossibleShip]] = defaultdict(list)
        for ship in incomplete_ships:
            for size in ship.possible_sizes:
                possible_ships_by_possible_size[size].append(ship)
        for size, ships in possible_ships_by_possible_size.items():
            if len(ships) == ship_sizes.get(size, 0):
                for ship in ships:
                    ship.fill_up_to_size(size=size, change_tracker=self.change_tracker)
                    incomplete_ships.remove(ship)

        # For a started ship, only one of the possible ship sizes is a ship size we still need: Fill it up to that size
        for ship in filter(lambda s: s.partial, incomplete_ships):
            possible_sizes = list(filter(lambda s: s in ship_sizes.keys(), ship.possible_sizes))
            if len(possible_sizes) == 1:
                ship.fill_up_to_size(size=possible_sizes[0], change_tracker=self.change_tracker)

