from dataclasses import dataclass, field


@dataclass(frozen=True)
class GameSize:
    size: int
    ship_sizes: list[int] = field(default_factory=list)


SIZES = {6: GameSize(size=6, ship_sizes=[1, 1, 1, 2, 2, 3]),
         7: GameSize(size=7, ship_sizes=[1, 1, 1, 2, 2, 3, 4]),
         8: GameSize(size=8, ship_sizes=[1, 1, 1, 2, 2, 2, 3, 3, 4]),
         10: GameSize(size=10, ship_sizes=[1, 1, 1, 1, 2, 2, 2, 3, 3, 4, 5]),
         12: GameSize(size=12, ship_sizes=[1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 4, 5]),
         15: GameSize(size=15, ship_sizes=[1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 4, 4, 5])}
