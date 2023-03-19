# class for Priority queue
from datetime import timedelta

import pandas as pd

from Classes import *


def decode_path(came_from, goal, start, DEPTH, NODES):
    path = []
    current = goal
    changes = set()
    path.append([goal, 'end'])
    while current != start:
        info = came_from[current]
        edge = info[1]
        changes.add(edge.line)
        path.append([info[0], edge.start_time.time(), edge.end_time.time(), edge.line])
        current = info[0]

    time_diff = datetime.combine(date.today(), path[1][1]) - datetime.combine(date.today(), path[len(path) - 1][1])

    path.reverse()

    path_df = pd.DataFrame(path, columns=['start_stop', 'start_time', 'end_time', 'line'])

    # print(path_df)
    return path, path_df, len(changes), time_diff, DEPTH, NODES


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
        goal.start_stop_lon - next_stop.start_stop_lon)) * 10


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
        DEPTH+=1
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
                NODES+=1
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
        DEPTH+=1
        current = frontier.get()

        current_time = time + timedelta(seconds=time_delta[current])

        if current == goal:
            return decode_path(came_from, start=start, goal=goal, DEPTH=DEPTH, NODES=NODES)

        for next_stop, edge in graph.getDeparturesAfterTime(current_time, current):

            new_time_delta = time_delta[current] + (edge.end_time - current_time).total_seconds()

            new_cost = cost_so_far[current] + (
                0 if came_from[current] is None or came_from[current][1].line == edge.line else 1) + new_time_delta / n

            if next_stop not in cost_so_far or new_cost < cost_so_far[next_stop]:
                time_delta[next_stop] = new_time_delta

                cost_so_far[next_stop] = new_cost

                priority = new_cost + transfer_heuristic(lines, edge.line)

                frontier.put(next_stop, priority)

                came_from[next_stop] = [current, edge]
                NODES+=1
    return None
