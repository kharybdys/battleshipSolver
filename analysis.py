import html
from collections import Counter
from enum import Enum
from typing import Self, Iterable

from strategy.change_tracker import ChangeTracker


class AnalysisError(Exception):
    pass


class Status(Enum):
    EMPTY = ("EMPTY", "&middot;")
    UNKNOWN = ("UNKNOWN", "&nbsp;")
    FILLED = ("FILLED", "&quest;")  # But unknown what shape
    FILLED_SINGLE = ("FILLED_SINGLE", "o")  # A ship of size one
    FILLED_SQUARE = ("FILLED_SQUARE", "+")  # Middle part of a horizontal or vertical ship
    FILLED_END_LEFT = ("FILLED_END_LEFT", "&sub;")  # End part of a ship that doesn't continue on left side
    FILLED_END_RIGHT = ("FILLED_END_RIGHT", "&sup;")  # End part of a ship that doesn't continue on right side
    FILLED_END_TOP = ("FILLED_END_TOP", "&cap;")  # End part of a ship that doesn't continue on top side
    FILLED_END_BOTTOM = ("FILLED_END_BOTTOM", "&cup;")  # End part of a ship that doesn't continue on bottom side

    def __new__(cls, value, print_chr):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.print_chr = html.unescape(print_chr)
        return obj

    def equivalent(self, other_status: Self) -> bool:
        """ Whether other_status is equivalent (maybe more specific) than self."""
        match self:
            case Status.EMPTY:
                return other_status == Status.EMPTY
            case Status.UNKNOWN:
                return True
            case Status.FILLED:
                return other_status not in [Status.UNKNOWN, Status.EMPTY]
            case Status.FILLED_SQUARE:
                return other_status not in [Status.UNKNOWN, Status.EMPTY, Status.FILLED]
            case Status.FILLED_SINGLE:
                return other_status == Status.FILLED_SINGLE
            case _:
                return self == other_status or other_status == Status.FILLED_SINGLE


class BattleshipBoardEntry:
    def __init__(self, status: Status = Status.UNKNOWN):
        self.status = status

    def __repr__(self):
        return f"{self.status}"

    @property
    def simplified(self) -> Status:
        if self.status == Status.EMPTY or self.status == Status.UNKNOWN:
            return self.status
        else:
            return Status.FILLED

    @property
    def filled(self) -> bool:
        return self.simplified == Status.FILLED

    @property
    def unknown(self) -> bool:
        return self.status == Status.UNKNOWN

    @property
    def empty(self) -> bool:
        return self.status == Status.EMPTY

    def set_filled(self, change_tracker: ChangeTracker):
        self.status = Status.FILLED
        change_tracker.set_changed()

    def set_empty(self, change_tracker: ChangeTracker):
        self.status = Status.EMPTY
        change_tracker.set_changed()


class DummyBattleshipBoardEntry(BattleshipBoardEntry):
    def __init__(self, status: Status = Status.UNKNOWN):
        super().__init__(status)
        self.status = Status.EMPTY

    def set_filled(self, change_tracker: ChangeTracker):
        pass

    def set_empty(self, change_tracker: ChangeTracker):
        pass


EDGE_ENTRY = DummyBattleshipBoardEntry()


def get_filled_status(left: BattleshipBoardEntry, right: BattleshipBoardEntry, top: BattleshipBoardEntry, bottom: BattleshipBoardEntry) -> Status:
    if left.empty and right.empty and top.empty and bottom.empty:
        return Status.FILLED_SINGLE
    if top.empty and bottom.empty:
        if left.empty and not right.empty:
            return Status.FILLED_END_LEFT
        elif right.empty and not left.empty:
            return Status.FILLED_END_RIGHT
        elif right.filled and left.filled:
            return Status.FILLED_SQUARE
        else:
            return Status.FILLED
    if left.empty and right.empty:
        if top.empty and not bottom.empty:
            return Status.FILLED_END_TOP
        elif bottom.empty and not top.empty:
            return Status.FILLED_END_BOTTOM
        elif bottom.filled and top.filled:
            return Status.FILLED_SQUARE
        else:
            return Status.FILLED
    return Status.FILLED


def analyze_row_or_column(row_or_column: Iterable[BattleshipBoardEntry]) -> tuple[int, int, int]:
    entry_counter = Counter(map(lambda e: e.simplified, row_or_column))
    return entry_counter.get(Status.EMPTY, 0), entry_counter.get(Status.FILLED, 0), entry_counter.get(Status.UNKNOWN, 0)
