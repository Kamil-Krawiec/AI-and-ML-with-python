# class for Priority queue
from datetime import timedelta

import pandas as pd

from Classes import *


def decode_path(came_from, goal, start):
    path = []
    current = goal
    path.append([goal, 'end'])
    while current != start:
        info = came_from[current]
        edge = info[1]
        path.append([info[0], edge.start_time.time(), edge.end_time.time(), edge.line])
        current = info[0]
    path.reverse()

    path_df = pd.DataFrame(path, columns=['start_stop', 'start_time', 'end_time', 'line'])

    print(path_df)
    return path


# ------------------------- DIJKSTRA

def dijkstra_time(graph, start, goal, time):
    time = pd.to_datetime(time)
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = dict()
    cost_so_far = dict()
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        time_from_beginning, current = frontier.get()

        current_time = time + timedelta(seconds=cost_so_far[current])

        if current == goal:
            break

        for next_stop, edge in graph.getDeparturesAfterTime(current_time, current):

            new_cost = cost_so_far[current] + (edge.end_time - current_time).total_seconds()

            if next_stop not in cost_so_far or new_cost < cost_so_far[next_stop]:
                cost_so_far[next_stop] = new_cost
                priority = new_cost
                frontier.put(next_stop, priority)

                came_from[next_stop] = [current, edge]

    return decode_path(came_from, start=start, goal=goal)


# ----------------------------------------- ASTAR

# ----------------------------------------- TIME
def time_heuristic(goal, next_stop):
    return (abs(goal.start_stop_lat - next_stop.start_stop_lat) + abs(
        goal.start_stop_lon - next_stop.start_stop_lon)) * 10


def aStar_time(graph, start, goal, time):
    time = pd.to_datetime(time)
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = dict()
    cost_so_far = dict()
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        time_from_beginning, current = frontier.get()

        current_time = time + timedelta(seconds=cost_so_far[current])

        if current == goal:
            break

        for next_stop, edge in graph.getDeparturesAfterTime(current_time, current):

            new_cost = cost_so_far[current] + (edge.end_time - current_time).total_seconds()

            if next_stop not in cost_so_far or new_cost < cost_so_far[next_stop]:
                cost_so_far[next_stop] = new_cost
                priority = new_cost + time_heuristic(graph.vertexes[goal], graph.vertexes[next_stop])
                frontier.put(next_stop, priority)

                came_from[next_stop] = [current, edge]

    return decode_path(came_from, start=start, goal=goal)


# ----------------------------------------- TRANSFERS

def transfer_heuristic(prev_stop, next_stop):
    return 100000 if prev_stop.line != next_stop.line else 0


def aStar_transfers(graph, start, goal, time):
    time = pd.to_datetime(time)
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = dict()
    cost_so_far = dict()
    prev_stop = start
    came_from[start] = None
    cost_so_far[start] = 0


    while not frontier.empty():
        time_from_beginning, current = frontier.get()

        current_time = time + timedelta(seconds=cost_so_far[current])

        if current == goal:
            break

        for next_stop, edge in graph.getDeparturesAfterTime(current_time, current):

            new_cost = cost_so_far[current] + (edge.end_time - current_time).total_seconds()

            if next_stop not in cost_so_far or new_cost < cost_so_far[next_stop]:
                cost_so_far[next_stop] = new_cost

                priority = new_cost + transfer_heuristic(
                        came_from[current][1] if came_from[current] is not None else edge,
                        edge
                    )

                frontier.put(next_stop, priority)

                came_from[next_stop] = [current, edge]



    return decode_path(came_from, start=start, goal=goal)
