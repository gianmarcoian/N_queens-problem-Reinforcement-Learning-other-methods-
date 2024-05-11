import sys
import numpy as np

if len(sys.argv) != 2:
    print("Usage: python name_file.py <problem_size_from_to_8>")
    sys.exit(1)

# I take the size of the problem
n_queens = int(sys.argv[1])

# Check if the size is within the allowed range
if n_queens < 2 or n_queens > 8:
    print("The size of the problem must be between 2 and 8.")
    sys.exit(1)

# Function to generate initial state
def generate_initial_state():
    return np.full((n_queens,), -1)

# Function to determine possible actions given a state
def get_possible_actions(state):
    return [col for col in range(n_queens) if state[col] == -1]

# Function to execute an action to obtain a new state
def take_action(state, action):
    new_state = state.copy()
    row = np.count_nonzero(new_state != -1)

    # Check if the action is within the valid range
    if 0 <= action < len(new_state):
        new_state[row] = action
        if is_valid_solution(new_state): 
            return new_state
        else:
            return state
    else:
        # Handle the case where the action is outside the valid range
        return state

# Function to print the chessboard with queens
def print_chessboard(state):
    for row in range(n_queens):
        line = ""
        for col in range(n_queens):
            if col == state[row]:
                line += "Q "
            else:
                line += ". "
        print(line)
    print()

# Get reward function, state-based
def get_reward(state, prec_state):
    queens_placed = np.count_nonzero(state != -1)
    queens_placed_before = np.count_nonzero(prec_state != -1)
    if queens_placed == n_queens and is_valid_solution(state):
        return 1.0
    else:
        return 0.2

# Function to check the validity of the solution
def is_valid_solution(state):
    queens_placed = np.count_nonzero(state != -1)
    if queens_placed < 2:
        return True
    
    for i in range(queens_placed):
        for j in range(i + 1, queens_placed):
            if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                return False
    return True

# Testing phase
q_values = np.zeros(n_queens)
epsilon = 0.4
test_state = generate_initial_state()
counter = 0
counter_restart = 0

while not get_reward(test_state, test_state) == 1 and counter < 100:
    counter += 1
    counter_restart += 1
    if np.random.rand() < epsilon:
        action = np.random.choice(get_possible_actions(test_state))
    else:
        action = np.argmax(q_values) 

    # Take action only if the required number of queens is not yet placed
    if np.count_nonzero(test_state != -1) < n_queens:
        actual_position = np.count_nonzero(test_state != -1) - 1
        test_state_bef = test_state
        test_state = take_action(test_state, action)
        reward = get_reward(test_state, test_state_bef)
        q_values[action] -= reward

        print(f"Chessboard:")
        print_chessboard(test_state)
    else:
        print("Required number of queens already placed. Stopping.")
        break

    if counter_restart > 18: 
        test_state = generate_initial_state()
        counter_restart = 0

print("Final state:")
print_chessboard(test_state)
