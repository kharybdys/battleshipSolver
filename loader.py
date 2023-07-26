import json
from os import PathLike

from board import BattleshipBoard
from analysis import Status
from sizes import SIZES


def load_board(file_path: PathLike) -> BattleshipBoard:
    with open(file_path, "r") as f:
        dct = json.load(f)
        size = SIZES.get(dct.get("size", 0))
        if not size:
            raise ValueError(f"Invalid size defined in file {file_path}, namely {dct.get('size', 0)}")
        row_pieces = dct.get("row_pieces", [])
        column_pieces = dct.get("column_pieces", [])
        if len(row_pieces) != size.size:
            raise ValueError(f"Invalid length of row_pieces in file {file_path}, doesn't match size")
        if len(column_pieces) != size.size:
            raise ValueError(f"Invalid length of column_pieces in file {file_path}, doesn't match size")
        board = BattleshipBoard(size, row_pieces, column_pieces)
        for hint in dct.get("hints"):
            board.add_hint(x=hint["x"], y=hint["y"], status=Status(hint["status"]))
    return board
