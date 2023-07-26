from pathlib import Path

from loader import load_board
from plot import plot
from solver import solve

if __name__ == '__main__':
    board = load_board(Path(__file__).parent / "data" / "15_a.json")
    plot(board)
    print("Solving...")
    solve(board)
    plot(board)
    print("Done")
