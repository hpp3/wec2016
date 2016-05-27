import json

def dijkstra(graph, edges, initial):
  visited = {initial: 0}
  path = {}

  nodes = set(graph)

  while nodes: 
    min_node = None
    for node in nodes:
      if node in visited:
        if min_node is None:
          min_node = node
        elif visited[node] < visited[min_node]:
          min_node = node

    if min_node is None:
      break

    nodes.remove(min_node)
    current_weight = visited[min_node]

    for edge in graph.edges[min_node]:
      weight = current_weight + graph.distance[(min_node, edge)]
      if edge not in visited or weight < visited[edge]:
        visited[edge] = weight
        path[edge] = min_node

  return visited, path

roads_file = open('roads.json', 'r')
all_data = json.load(roads_file)
graph = {}
dist = {}

for road in all_data['features']:
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
