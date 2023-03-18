from Functions import *
from time import process_time
# READING AND UNDERSTANDING DATA
df = pd.read_csv('connection_graph.csv', low_memory=False, header=0)
df = df.drop(['Unnamed: 0.1', 'Unnamed: 0'], axis=1)
df['arrival_time'] = pd.to_datetime(df['arrival_time'])
df['departure_time'] = pd.to_datetime(df['departure_time'])

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

start = 'Stalowa'
goal='Psie Pole'
time='11:00:00'

print("{} {} {}".format(30*"#","ASTAR TIME",30*"#"))
st_astar = process_time()
aStar_path = aStar_time(graph,start=start,goal=goal,time=time)
end_astar = process_time()

print("{} {} {}".format(30*"#","DIJKSTRA TIME",30*"#"))
st_dijkstra = process_time()
dijkstra_path = dijkstra_time(graph,start=start,goal=goal,time=time)
end_dijkstra = process_time()

print("{} {} {}".format(30*"#","ASTAR TRANSFER",30*"#"))
st_astar_transfer = process_time()
aStar_path_transfer = aStar_transfers(graph,start=start,goal=goal,time=time)
end_astar_transfer = process_time()

eval_time_dijkstra = end_dijkstra-st_dijkstra
eval_time_astar = end_astar-st_astar

print("{} {} {}".format(30*"#","RESULTS",30*"#"))
print("DIJKSTRA_TIME time of eval: {:0.3f}s".format(eval_time_dijkstra))
print("ASTAR_TIME time of eval: {:0.3f}s".format(eval_time_astar))
print("Difference D_TIME-A_TIME = {:0.3f}s".format(eval_time_dijkstra-eval_time_astar))
print("ASTAR_TRANSFER = {:0.3f}s".format(end_astar_transfer-st_astar_transfer))
print("The same path: {}".format(aStar_path == dijkstra_path == aStar_path_transfer))

