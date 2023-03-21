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

# --------------------------------------------------------- TESTING

taboo = Taboo(graph)

start = process_time()
best_result_transfers = taboo.taboo_search(
    initial_solution = ['OPORÓW', 'DWORZEC GŁÓWNY', 'Kasprowicza','Grabiszyńska','Psie Pole', 'OPORÓW'],
    max_iterations=100,
    time='17:00:00',
criteria='c'
)
end = process_time()

print(best_result_transfers[0].to_string())
print("time of eval: {} transfers {}".format(end-start,best_result_transfers[1]))

start = process_time()
best_result_time = taboo.taboo_search(
    initial_solution = ['OPORÓW', 'DWORZEC GŁÓWNY', 'Kasprowicza','Grabiszyńska','Psie Pole', 'OPORÓW'],
    max_iterations=100,
    time='17:00:00',
criteria='t'
)
end = process_time()

print(best_result_time[0].to_string())
print("time of eval: {} transfers {}".format(end-start,best_result_time[1]))