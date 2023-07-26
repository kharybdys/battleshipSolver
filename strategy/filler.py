from analysis import analyze_row_or_column
from strategy.abstract import AbstractStrategy


class FillRowsAndColumns(AbstractStrategy):

    def solve(self):
        for row, row_pieces in self.board.rows_with_pieces():
            self.fill_row_or_column(row, row_pieces)
        for column, column_pieces in self.board.columns_with_pieces():
            self.fill_row_or_column(column, column_pieces)

    def fill_row_or_column(self, row_or_column, pieces_expected: int):
        empty, filled, unknown = analyze_row_or_column(row_or_column)
        if filled == pieces_expected:
            # fill the rest of the row or column with empty
            for entry in row_or_column:
                if entry.unknown:
                    entry.set_empty(self.change_tracker)
        elif filled + unknown == pieces_expected:
            # fill the rest of the row or column with filled
            for entry in row_or_column:
                if entry.unknown:
                    entry.set_filled(self.change_tracker)


