import sys
import numpy as np
import os
import time

def is_valid_move(board, row, col):
    # Check if placing a queen in the given position is valid
    for i in range(row):
        if board[i] == col or \
           board[i] - i == col - row or \
           board[i] + i == col + row:
            return False
    return True

def forward_checking(board, row, size, remaining_cols):
    if row == size:
        return True

    for col in remaining_cols[:]:
        if is_valid_move(board, row, col):
            board[row] = col
            remaining_cols.remove(col)
            if forward_checking(board, row + 1, size, remaining_cols):
                return True
            remaining_cols.append(col)  # Backtrack
    return False

def calculate_average_distance(board):
    queens_placed = len(board)
    distances = []

    for i in range(queens_placed):
        for j in range(i + 1, queens_placed):
            distances.append(np.abs(board[i] - board[j]))

    return np.mean(distances) if distances else 0.0

def solve_n_queens(size):
    board = [-1] * size
    remaining_cols = list(range(size))
    if forward_checking(board, 0, size, remaining_cols):
        return board
    return None

def print_solution(board):
    for row in board:
        print(" ".join("Q" if col == row else "." for col in range(len(board))))

if __name__ == "__main__":
    n_queens_size = int(input("Enter the size of the N-Queens problem (between 2 and 8): "))
    if n_queens_size < 2 or n_queens_size > 8:
        print("Invalid size. Size must be between 2 and 8.")
    else:
        start_time=time.time()
        solution = solve_n_queens(n_queens_size)
        if solution:
            print("Solution found:")
            print_solution(solution)
            end_time=time.time()
            diff_time=end_time-start_time
            print(f"Time(s): {diff_time}")
            # Calcola e stampa la distanza media delle distanze medie
            final_average_distance = calculate_average_distance(solution)
            print(f"Final Average Distance: {final_average_distance:.2f}")
        else:
            print("No solution found.")
