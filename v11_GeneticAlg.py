import numpy as np
import time

def generate_initial_population(population_size, n_queens):
    return np.random.randint(0, n_queens, size=(population_size, n_queens))

def fitness(board):
    queens_placed = len(board)
    threats = 0

    for i in range(queens_placed):
        for j in range(i + 1, queens_placed):
            if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                threats += 1

    return threats

def calculate_average_distance(board):
    queens_placed = len(board)
    distances = []

    for i in range(queens_placed):
        for j in range(i + 1, queens_placed):
            distances.append(np.abs(board[i] - board[j]))

    return np.mean(distances) if distances else 0.0

def crossover(parent1, parent2):
    crossover_point = np.random.randint(1, len(parent1) - 1)
    child1 = np.concatenate((parent1[:crossover_point], parent2[crossover_point:]))
    child2 = np.concatenate((parent2[:crossover_point], parent1[crossover_point:]))
    return child1, child2

def mutate(child, mutation_rate):
    for i in range(len(child)):
        if np.random.rand() < mutation_rate:
            child[i] = np.random.randint(0, len(child))
    return child

def genetic_algorithm(n_queens, population_size, generations, mutation_rate):
    population = generate_initial_population(population_size, n_queens)

    for generation in range(generations):
        fitness_scores = np.array([fitness(board) for board in population])
        best_index = np.argmin(fitness_scores)
        best_fitness = fitness_scores[best_index]

        if best_fitness == 0:
            print(f"Solution found in generation {generation}!")
            print("Final Solution:")
            print_solution(population[best_index])
            final_average_distance = calculate_average_distance(population[best_index])
            print(f"Final Average Distance: {final_average_distance:.2f}")
            return population[best_index]

        selected_indices = np.argsort(fitness_scores)[:2]
        parent1, parent2 = population[selected_indices]

        child1, child2 = crossover(parent1, parent2)
        child1 = mutate(child1, mutation_rate)
        child2 = mutate(child2, mutation_rate)

        population[selected_indices] = [child1, child2]

    print("No solution found.")
    return None

def print_solution(board):
    for row in board:
        line = ""
        for col in range(len(board)):
            if col == row:
                line += "Q "
            else:
                line += ". "
        print(line)

if __name__ == "__main__":
    start_time=time.time()
    n_queens_size = int(input("Enter the size of the N-Queens problem (between 2 and 8): "))
    population_size = 50
    generations = 100000
    mutation_rate = 0.1

    if n_queens_size < 2 or n_queens_size > 8:
        print("Invalid size. Size must be between 2 and 8.")
    else:
        solution = genetic_algorithm(n_queens_size, population_size, generations, mutation_rate)
        end_time=time.time()
        diff_time=end_time-start_time
        print(f"\nTime: {diff_time}")