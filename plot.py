from board import BattleshipBoard


def plot(board: BattleshipBoard):
    headers = [" "]
    headers.extend(map(str, board.column_pieces))
    print(" ".join(headers))
    for row, row_piece in board.rows_with_pieces():
        row_to_print = [str(row_piece)]
        row_to_print.extend(map(lambda e: e.status.print_chr, row))
        print(" ".join(row_to_print))
    print()
    print()
