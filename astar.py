import json
from pprint import pprint

def eDis(a, b):
    x1, y1 = a
    x2, y2 = b
    return (x2-x1)**2 + (y2-y2)**2

def astar(start, goal, adj, trueDis, blacklist):
    closedSet = set()
    openSet = set([start])
    cameFrom = {}
    truePastScore = {start: 0}
    futureScore = {start: eDis(start, goal)}

    while openSet:
        current = min(openSet, key=lambda x: futureScore[x]) #heap this fuck
        if current == goal:
            return getPath(cameFrom, current)

        openSet.remove(current)
        closedSet.add(current)

        if current not in adj:
            continue

        for neighbor in adj[current]:
            if (current, neighbor) in blacklist:
                print('blocked')
                continue

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
