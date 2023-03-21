# class for Priority queue
from datetime import timedelta
from time import process_time

import pandas as pd

from Classes import *


def decode_path(came_from, goal, start, DEPTH, NODES):
    path = []
    current = goal
    changes = []
    path.append([goal, (came_from[goal])[1].end_time.time()])
    while current != start:
        info = came_from[current]
        edge = info[1]
        if changes == [] or changes[-1] != edge.line: changes.append(edge.line)
        path.append([info[0], edge.start_time.time(), edge.end_time.time(), edge.line])
        current = info[0]

    time_diff = datetime.combine(date.today(), path[1][2]) - datetime.combine(date.today(), path[len(path) - 1][1])
    path.reverse()

    path_df = pd.DataFrame(path, columns=['start_stop', 'start_time', 'end_time', 'line'])
    return path, path_df, len(changes) - 1, time_diff, DEPTH, NODES


# ------------------------- DIJKSTRA

def dijkstra_time(graph, start, goal, time):
    DEPTH = 0
    NODES = 0

    time = pd.to_datetime(time)
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = dict()
    cost_so_far = dict()
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()
        DEPTH += 1
        current_time = time + timedelta(seconds=cost_so_far[current])

        if current == goal:
            return decode_path(came_from, start=start, goal=goal, DEPTH=DEPTH, NODES=NODES)

        for next_stop, edge in graph.getDeparturesAfterTime(current_time, current):

            new_cost = cost_so_far[current] + (edge.end_time - current_time).total_seconds()

            if next_stop not in cost_so_far or new_cost < cost_so_far[next_stop]:
                cost_so_far[next_stop] = new_cost
                priority = new_cost
                frontier.put(next_stop, priority)

                came_from[next_stop] = [current, edge]

            NODES += 1
    return None


# ----------------------------------------- ASTAR

# ----------------------------------------- TIME
def time_heuristic(goal, next_stop):
    return (abs(goal.start_stop_lat - next_stop.start_stop_lat) + abs(
        goal.start_stop_lon - next_stop.start_stop_lon)) * 10000


def aStar_time(graph, start, goal, time):
    DEPTH = 0
    NODES = 0

    time = pd.to_datetime(time)
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = dict()
    cost_so_far = dict()
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        DEPTH += 1
        current = frontier.get()

        current_time = time + timedelta(seconds=cost_so_far[current])

        if current == goal:
            return decode_path(came_from, start=start, goal=goal, DEPTH=DEPTH, NODES=NODES)

        for next_stop, edge in graph.getDeparturesAfterTime(current_time, current):

            new_cost = cost_so_far[current] + (edge.end_time - current_time).total_seconds()

            if next_stop not in cost_so_far or new_cost < cost_so_far[next_stop]:
                cost_so_far[next_stop] = new_cost
                priority = new_cost + time_heuristic(graph.vertexes[goal], graph.vertexes[next_stop])
                frontier.put(next_stop, priority)
                came_from[next_stop] = [current, edge]
            NODES += 1
    return None


# ----------------------------------------- TRANSFERS

def transfer_heuristic(goal_lines, next_stop):
    return 1 if next_stop not in goal_lines else 0


def aStar_transfers(graph, start, goal, time, n):
    DEPTH = 0
    NODES = 0

    time = pd.to_datetime(time)
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = dict()
    cost_so_far = dict()
    time_delta = dict()
    lines = graph.getVertexLines(goal, time)
    came_from[start] = None
    time_delta[start] = 0
    cost_so_far[start] = 0

    while not frontier.empty():
        DEPTH += 1
        current = frontier.get()

        current_time = time + timedelta(seconds=time_delta[current])

        if current == goal:
            return decode_path(came_from, start=start, goal=goal, DEPTH=DEPTH, NODES=NODES)

        for next_stop, edge in graph.getDeparturesAfterTime(current_time, current):

            new_time_delta = time_delta[current] + (edge.end_time - current_time).total_seconds()

            new_cost = cost_so_far[current] + (
                0 if came_from[current] is None or came_from[current][1].line == edge.line else 2) + new_time_delta / n

            if next_stop not in cost_so_far or new_cost < cost_so_far[next_stop]:
                time_delta[next_stop] = new_time_delta

                cost_so_far[next_stop] = new_cost

                priority = new_cost + transfer_heuristic(lines, edge.line)

                frontier.put(next_stop, priority)

                came_from[next_stop] = [current, edge]
            NODES += 1
    return None


def calculate_b_star(N, d):
    b_star = 2.0
    eps = 0.00001

    for i in range(1000):
        sum_b = 0.0
        for j in range(d + 1):
            sum_b += b_star ** j

        if abs(N - sum_b) < eps:
            return b_star
        elif sum_b > N:
            b_star -= 0.01
        else:
            b_star += 0.01

    return b_star


# -------------------------------------------- FUNCTION FOR TESTING EX1
def test_ex1(graph, start, goal, time):
    path_list_first_ATR = aStar_time(graph, start=start, goal=goal, time=time)[1]
    print(path_list_first_ATR)

    # TRANSFER ASTAR
    ATR = []
    path_list_first_ATR = aStar_transfers(graph, start=start, goal=goal, time=time, n=8110)[0]

    for i in range(100):
        start_astar_transfer = process_time()
        path_list_ATR, path_df_ATR, transfers_ATR, duration_ATR, D_ATR, N_ATR = aStar_transfers(graph, start=start,
                                                                                                goal=goal, time=time,
                                                                                                n=8110)
        end_astar_transfer = process_time()
        ATR.append([int(path_list_ATR == path_list_first_ATR), transfers_ATR, duration_ATR,
                    end_astar_transfer - start_astar_transfer, calculate_b_star(N_ATR, D_ATR)])
    df_ATR = pd.DataFrame(ATR, columns=['the_same_path', 'transfers', 'duration', 'time_of_eval', 'branching_factor'])

    print("{} {} {}".format(30 * '#', "Transfer A", 30 * '#'))
    print(df_ATR.describe().to_string())

    # TIME ASTAR
    ATI = []
    path_list_first_ATI = aStar_time(graph, start=start, goal=goal, time=time)[0]

    for i in range(100):
        start_astar_time = process_time()
        path_list_ATI, path_df_ATI, transfers_ATI, duration_ATI, D_ATI, N_ATI = aStar_time(graph, start=start,
                                                                                           goal=goal,
                                                                                           time=time)
        end_astar_time = process_time()
        ATI.append(
            [int(path_list_ATI == path_list_first_ATI), transfers_ATI, duration_ATI, end_astar_time - start_astar_time,
             calculate_b_star(N_ATI, D_ATI)])
    df_ATI = pd.DataFrame(ATI, columns=['the_same_path', 'transfers', 'duration', 'time_of_eval', 'branching_factor'])
    print("{} {} {}".format(30 * '#', "Time A", 30 * '#'))
    print(df_ATI.describe().to_string())

    # TIME DIJKSTRA
    DI = []
    path_list_first_DI = dijkstra_time(graph, start=start, goal=goal, time=time)[0]

    for i in range(100):
        start_dijkstra_time = process_time()
        path_list_D, path_df_D, transfers_D, duration_D, D_D, N_D = dijkstra_time(graph, start=start, goal=goal,
                                                                                  time=time)
        end_dijkstra_time = process_time()
        DI.append(
            [int(path_list_D == path_list_first_DI), transfers_D, duration_D, end_dijkstra_time - start_dijkstra_time,
             calculate_b_star(N_D, D_D)])
    df_DI = pd.DataFrame(DI, columns=['the_same_path', 'transfers', 'duration', 'time_of_eval', 'branching_factor'])
    print("{} {} {}".format(30 * '#', "Time D", 30 * '#'))
    print(df_DI.describe().to_string())


# -------------------------------- TABOO SEARCH
# Definiujemy funkcję celu (może to być dowolna funkcja, którą chcemy zminimalizować)


class Taboo:
    def __init__(self, graph):
        self.time = None
        self.graph = graph

    def decode_solution(self, best_solution):
        path_sum = []
        sum = 0
        transfers = 0
        for i in range(1, len(best_solution)):
            path, _, changes, time_diff, _, _ = aStar_time(self.graph, best_solution[i - 1], best_solution[i],
                                                     self.time + timedelta(seconds=sum))
            path_sum.extend(path)
            transfers += changes
            sum += time_diff.total_seconds()

        return pd.DataFrame(path_sum, columns=['start_stop', 'start_time', 'end_time', 'line']),transfers

    def objective_function_time(self, solution):
        sum = 0
        for i in range(1, len(solution)):
            _, _, _, time_diff, _, _ = aStar_time(self.graph, solution[i - 1], solution[i],
                                                  self.time + timedelta(seconds=sum))
            sum += time_diff.total_seconds()
        return sum

    def objective_function_transfers(self, solution):
        sum = 0
        transfers = 0
        for i in range(1, len(solution)):
            _, _, changes, time_diff, _, _ = aStar_transfers(self.graph, solution[i - 1], solution[i],
                                                             self.time + timedelta(seconds=sum), n=8100)
            sum += time_diff.total_seconds()
            transfers += changes
        return transfers

    # Definiujemy funkcję generującą sąsiedztwo (zmiany w rozwiązaniu)
    def get_neighbors(self, solution):
        neighbors = [solution.copy()]
        for i in range(1, len(solution) - 1):
            for j in range(i + 1, len(solution) - 1):
                neighbor = solution.copy()
                neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
                neighbors.append(neighbor)

        return neighbors

    # Definiujemy algorytm Tabu Search
    def taboo_search(self, initial_solution, max_iterations, time, criteria):
        objective_function = self.objective_function_time if criteria == 't' else self.objective_function_transfers
        self.time = pd.to_datetime(time)

        current_solution = initial_solution.copy()

        best_solution = current_solution.copy()

        tabu_list = []

        iteration = 0

        while iteration < max_iterations:
            neighbors = self.get_neighbors(current_solution)

            neighbors = [n for n in neighbors if n not in tabu_list]

            if not neighbors:
                break

            next_solution = min(neighbors, key=objective_function)

            tabu_list.append(next_solution)

            # if len(tabu_list) > tabu_list_size:
            #     tabu_list.pop(0)

            if objective_function(next_solution) < objective_function(best_solution):
                best_solution = next_solution.copy()

            current_solution = next_solution.copy()
            iteration += 1
        print(iteration)
        return self.decode_solution(best_solution)
