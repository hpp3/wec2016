import json
from astar import astar

roads_file = open('roads.json', 'r')

all_data = json.load(roads_file)
graph = {}
dist = {}
coord_to_seg = {}

black_list = set([26896, 1517, 7608, 1526, 7947, 7494, 7469, 9064, 9062, 7572, 7514, 259, 1621, 29101, 30205, 7289, 274, 348])

for road in all_data['features']:
    if road['properties']['SEGMENT_ID'] in black_list:
        continue

    from_coord = tuple(road['geometry']['coordinates'][0])
    to_coord = tuple(road['geometry']['coordinates'][-1])

    if road['geometry']['type'] == 'LineString':
        coord_to_seg[(from_coord, to_coord)] = road['properties']['SEGMENT_ID']
        coord_to_seg[(to_coord, from_coord)] = road['properties']['SEGMENT_ID']
        if road['properties']['FLOW_DIR'] == 'TwoWay':
            if from_coord not in graph:
                graph[from_coord] = []
            graph[from_coord].append(to_coord)
            dist[(from_coord, to_coord)] = road['properties']['LENGTH_M']
            dist[(to_coord, from_coord)] = road['properties']['LENGTH_M']
            if to_coord not in graph:
                graph[to_coord] = []
            graph[to_coord].append(from_coord)
        elif road['properties']['FLOW_DIR'] == 'ToFrom':
            if to_coord not in graph:
                graph[to_coord] = []
            graph[to_coord].append(from_coord)
            dist[(to_coord, from_coord)] = road['properties']['LENGTH_M']
        elif road['properties']['FLOW_DIR'] == 'FromTo':
            if from_coord not in graph:
                graph[from_coord] = []
            graph[from_coord].append(to_coord)
            dist[(from_coord, to_coord)] = road['properties']['LENGTH_M']

start = (-80.5328174269999, 43.4732988380001)
end = (-80.5002613569999,43.511091493)
for (a, b) in astar(start, end, graph, dist):
    print(b, ',', a)

#optimal_path = list(reversed(astar(start, end, graph, dist)))
#seg_path = []
#for i in range(1, len(optimal_path)):
#    seg_path.append(coord_to_seg[(optimal_path[i-1], optimal_path[i])])
#print seg_path
