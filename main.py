from time import process_time

from Functions import *

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
start = 'OPORÓW'
goal = 'BISKUPIN'
time = '17:00:00'

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
                end_astar_transfer - start_astar_transfer,calculate_b_star(N_ATR,D_ATR)])
df_ATR = pd.DataFrame(ATR, columns=['the_same_path', 'transfers', 'duration', 'time_of_eval', 'branching_factor'])

print("{} {} {}".format(30 * '#', "Transfer A", 30 * '#'))
print(df_ATR.describe().to_string())

# TIME ASTAR
ATI = []
path_list_first_ATI = aStar_time(graph, start=start, goal=goal, time=time)[0]

for i in range(100):
    start_astar_time = process_time()
    path_list_ATI, path_df_ATI, transfers_ATI, duration_ATI, D_ATI, N_ATI = aStar_time(graph, start=start, goal=goal,
                                                                                       time=time)
    end_astar_time = process_time()
    ATI.append(
        [int(path_list_ATI == path_list_first_ATI), transfers_ATI, duration_ATI, end_astar_time - start_astar_time,
         calculate_b_star(N_ATI,D_ATI)])
df_ATI = pd.DataFrame(ATI, columns=['the_same_path', 'transfers', 'duration', 'time_of_eval', 'branching_factor'])
print("{} {} {}".format(30 * '#', "Time A", 30 * '#'))
print(df_ATI.describe().to_string())

# TIME DIJKSTRA
DI = []
path_list_first_DI = dijkstra_time(graph, start=start, goal=goal, time=time)[0]

for i in range(100):
    start_dijkstra_time = process_time()
    path_list_D, path_df_D, transfers_D, duration_D, D_D, N_D = dijkstra_time(graph, start=start, goal=goal, time=time)
    end_dijkstra_time = process_time()
    DI.append(
        [int(path_list_D == path_list_first_DI), transfers_D, duration_D, end_dijkstra_time - start_dijkstra_time,
         calculate_b_star(N_D, D_D)])
df_DI = pd.DataFrame(DI, columns=['the_same_path', 'transfers', 'duration', 'time_of_eval', 'branching_factor'])
print("{} {} {}".format(30 * '#', "Time D", 30 * '#'))
print(df_DI.describe().to_string())


