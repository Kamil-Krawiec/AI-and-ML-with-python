from datetime import datetime
import heapq

class Vertex:
    def __init__(self, place, start_stop_lat, start_stop_lon):
        self.place = place
        self.start_stop_lat = start_stop_lat
        self.start_stop_lon = start_stop_lon


class Edge:

    def __init__(self, start_time, end_time, line):
        self.end_time = end_time
        self.start_time = start_time
        self.line = line
        self.duration = self.getConnectionDuration()

    def __str__(self):
        return "wyjazd godzina {:^20} ->> przyjazd godzina {:^20} linia {:^14}".format(self.start_time,self.end_time,self.line)

    def getConnectionDuration(self ):
        return (datetime.strptime(self.end_time, '%H:%M:%S') - datetime.strptime(self.start_time, '%H:%M:%S')).total_seconds()


class Graph:

    def __init__(self, graph, vertexes):
        self.graph = graph
        self.vertexes = vertexes

    def addVertex(self, vertex):
        if vertex not in self.graph:
            self.vertexes[vertex.place] = vertex
            self.graph[vertex.place] = []

    def printPlanForStop(self,stop):
        for next_stop,edge in self.graph[stop]:
            print('{} on {} with line {}\n'.format(next_stop,edge.start_time,edge.line))

    def printGraph(self):
        for vertex in self.graph:
            for edges in self.graph[vertex]:
                print(vertex, " -> ", edges[0], " edge weight: ", edges[1])

    def waitingCost(self,time,edge):
        return (datetime.strptime(edge.end_time, '%H:%M:%S')-datetime.strptime(time, '%H:%M:%S')).total_seconds()

    def add_edge(self, v1, v2, e):
        if v1 not in self.graph:
            print("Vertex ", v1, " does not exist.")
        elif v2 not in self.graph:
            print("Vertex ", v2, " does not exist.")
        else:
            temp = (v2, e)
            self.graph[v1].append(temp)


class PriorityQueue:

    def __init__(self):
        self.elements: list[()] = []

    def empty(self):
        return not self.elements

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)