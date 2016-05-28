import json
from astar import astar

roads_file = open('roads.json', 'r')

all_data = json.load(roads_file)
graph = {}
dist = {}
coord_to_seg = {}
seg_to_coord = {}

black_list = set([26896, 1517, 7608, 1526, 7947, 7494, 7469, 9064, 9062, 7572, 7514, 259, 1621, 29101, 30205, 7289, 274, 348, 80267])

# Update coord-seg mapping and vice versa
for road in all_data['features']:
    from_coord = tuple(road['geometry']['coordinates'][0])
    to_coord = tuple(road['geometry']['coordinates'][-1])

    if road['geometry']['type'] == 'LineString':
        coord_to_seg[(from_coord, to_coord)] = road['properties']['SEGMENT_ID']
        coord_to_seg[(to_coord, from_coord)] = road['properties']['SEGMENT_ID']
        seg_to_coord[road['properties']['SEGMENT_ID']] = road['geometry']['coordinates']
for road in all_data['features']:
    if road['properties']['SEGMENT_ID'] in black_list:
        continue

    from_coord = tuple(road['geometry']['coordinates'][0])
    to_coord = tuple(road['geometry']['coordinates'][-1])

    if road['geometry']['type'] == 'LineString':
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

def getCoords(input_list=[7294, 274, 389]):
    coord = []
    for i in input_list:
        coord.extend(seg_to_coord[i])
    coord = [[y,x] for x, y in coord]
    return coord


def getClosures(input_list=[7294, 274, 389]):
    coord = []
    for i in input_list:
        if i in black_list:
            coord.append(seg_to_coord[i])
    coord = [[[y,x] for x, y in kappa] for kappa in coord]
    return coord


def getPaths(input_list=[7294, 274, 389]):
    # get start and end coords
    if len(input_list) == 1:
        start = seg_to_coord[input_list[0]][0]
        end = seg_to_coord[input_list[-1]][-1]
    else:
        if seg_to_coord[input_list[0]][0] in seg_to_coord[input_list[1]]:
            start = seg_to_coord[input_list[0]][-1]
        else:
            start = seg_to_coord[input_list[0]][0]

        if seg_to_coord[input_list[-1]][0] in seg_to_coord[input_list[-2]]:
            end = seg_to_coord[input_list[-1]][-1]
        else:
            end = seg_to_coord[input_list[-1]][0]
    start = tuple(start)
    end = tuple(end)

    # calculate best paths
    bestPaths = []
    segblacklist = set()
    bestPaths.append(astar(start, end, graph, dist, set()))
    for z in range(2):
        seg = set()
        for i in range(len(bestPaths[-1])-1):
            seg.add((bestPaths[-1][i+1], bestPaths[-1][i]))
        for i in range(2-z):
            if len(seg) < 5:
                break
            top = max(seg, key=lambda s: dist[s])
            segblacklist.add(top)
            seg.remove(top) 
            new = astar(start, end, graph, dist, segblacklist)
        if new not in bestPaths:
            bestPaths.append(new)

    pathCoords = []
    for path in bestPaths:
        seg = set() 
        p = list(reversed(path)) 
        coord = []
        for i in range(1, len(p)):
            seg = coord_to_seg[(p[i-1], p[i])]
            c = seg_to_coord[seg]
            c = [(b,a) for a, b in c]
            coord.extend(c)
        pathCoords.append(coord)
    return pathCoords
