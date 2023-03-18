import pandas as pd
from Classes import *
from Functions import *

# READING AND UNDERSTANDING DATA
df = pd.read_csv('connection_graph.csv', low_memory=False, header=0)
df = df.drop(['Unnamed: 0.1', 'Unnamed: 0'], axis=1)

# grouping df by place and setting its lat and lon as mean()
new_end_stop = pd.DataFrame(df.groupby(by=['end_stop'])[['end_stop_lat', 'end_stop_lon']].mean())
new_start_stop = pd.DataFrame(df.groupby(by=['start_stop'])[['start_stop_lat', 'start_stop_lon']].mean())

# CREATING GRAPH
graph = Graph({}, {})

for place, index in new_end_stop.iterrows():
    lat, lon = index
    vertex = Vertex(place, lat, lon)
    graph.addVertex(vertex)

for place, index in new_start_stop.iterrows():
    lat, lon = index
    vertex = Vertex(place, lat, lon)
    graph.addVertex(vertex)

# Reading data and filling the graph
for i, row in df.iterrows():
    edge = Edge(row['departure_time'], row['arrival_time'], row['line'])
    graph.add_edge(row['start_stop'], row['end_stop'], edge)

aStar_time(graph,start="PILCZYCE",goal="KRZYKI",time='23:00:00')
