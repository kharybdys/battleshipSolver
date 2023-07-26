from typing import Iterable, Optional, Generator

from analysis import Status, BattleshipBoardEntry, EDGE_ENTRY
from sizes import GameSize


class BattleshipBoard:
    def __init__(self, size: GameSize, row_pieces: list[int], column_pieces: list[int]):
        self.size = size
        self.row_pieces = row_pieces
        self.column_pieces = column_pieces
        # Inner list is the columns
        self.board: list[list[BattleshipBoardEntry]] = [[BattleshipBoardEntry() for _ in range(size.size)] for _ in range(size.size)]

    def add_hint(self, x: int, y: int, status: Status):
        self.get(x, y).status = status

    def columns_with_pieces(self) -> Iterable[tuple[list[BattleshipBoardEntry, int]]]:
        return zip(self.board, self.column_pieces)

    def rows_with_pieces(self) -> Iterable[tuple[list[BattleshipBoardEntry, int]]]:
        return zip(self.transposed_board, self.row_pieces)

    @property
    def transposed_board(self) -> list[list[BattleshipBoardEntry]]:
        return [[self.board[x][y] for x in range(self.size.size)] for y in range(self.size.size)]

    def get(self, x: int, y: int, default: Optional[BattleshipBoardEntry] = None) -> BattleshipBoardEntry:
        if 0 <= x < self.size.size:
            if 0 <= y < self.size.size:
                return self.board[x][y]
            elif default:
                return default
            else:
                raise ValueError(f"Invalid y coordinate for get: {y}, size is {self.size.size}")
        elif default:
            return default
        else:
            raise ValueError(f"Invalid x coordinate for get: {x}, size is {self.size.size}")

    def get_neighbours(self, x: int, y: int) -> tuple[BattleshipBoardEntry, BattleshipBoardEntry, BattleshipBoardEntry, BattleshipBoardEntry]:
        left = self.get(x-1, y, EDGE_ENTRY)
        right = self.get(x+1, y, EDGE_ENTRY)
        top = self.get(x, y-1, EDGE_ENTRY)
        bottom = self.get(x, y+1, EDGE_ENTRY)
        return left, right, top, bottom

    def get_diagonal_neighbours(self, x: int, y: int) -> tuple[BattleshipBoardEntry, BattleshipBoardEntry, BattleshipBoardEntry, BattleshipBoardEntry]:
        left_top = self.get(x-1, y-1, EDGE_ENTRY)
        right_top = self.get(x+1, y-1, EDGE_ENTRY)
        left_bottom = self.get(x-1, y+1, EDGE_ENTRY)
        right_bottom = self.get(x+1, y+1, EDGE_ENTRY)
        return left_top, left_bottom, right_top, right_bottom

    def iterate(self) -> Generator[tuple[int, int, BattleshipBoardEntry], None, None]:
        for x in range(self.size.size):
            for y in range(self.size.size):
                yield x, y, self.get(x, y)
