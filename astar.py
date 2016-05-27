import json
from pprint import pprint

def eDis(a, b):
    x1, y1 = a
    x2, y2 = b
    return (x2-x1)**2 + (y2-y2)**2

def astar(start, goal, adj, trueDis):
    closedSet = set() # nodes previously evaluated
    openSet = set([start])
    cameFrom = {}       # most efficient previous step for a node
    truePastScore = {start: 0} # best dis from start
    futureScore = {start: eDis(start, goal)} # guess of dis from start to goal that passes this node

    while openSet:
        current = min(openSet, key=lambda x: futureScore[x]) #heap this fuck
        if current == goal:
            return getPath(cameFrom, current)

        openSet.remove(current)
        closedSet.add(current)

        if current not in adj:
            continue

        for neighbor in adj[current]:
            if neighbor in closedSet:
                continue
            distance = truePastScore[current] + trueDis[current, neighbor]
            if neighbor not in openSet:
                openSet.add(neighbor)
            elif distance >= truePastScore[neighbor]:
                continue

            # found better way to reach neighbour
            cameFrom[neighbor] = current
            truePastScore[neighbor] = distance
            futureScore[neighbor] = truePastScore[neighbor] + eDis(neighbor, goal)
    return failure

def getPath(cameFrom, curr):
    path = [curr]
    while curr in cameFrom:
        curr = cameFrom[curr]
        path.append(curr)
    return path
