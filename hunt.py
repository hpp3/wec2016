import json
import itertools

def flatten(l):
    return flatten(l[0]) + (flatten(l[1:]) if len(l) > 1 else []) if type(l) is list else [l]

def dist(a, b):
    return (a[0] - b[0])**2 + (a[1]-b[1])**2

with open('roads.json') as f:
    data = json.load(f)['features']

def doit(thresh):
    coords = {}
    for seg in data:
        last = None
        dd = flatten(seg['geometry']['coordinates'])
        for key in [(dd[0], dd[1]), (dd[-2], dd[-1])]:

            # print key, seg['properties']['SEGMENT_ID']
            if thresh:
                for old in coords:
                    if dist(old, key) < thresh:
                        key = old
            coords[key] = coords.get(key, [])
            coords[key].append(seg)

    rev = {}

    lone = [] 
    for coord in coords:
        rev[len(coords[coord])] = rev.get(len(coords[coord]), 0) + 1
        if len(coords[coord]) == 1: 
            lone.append((coord, coords[coord]))
    print rev
    return lone 

def printify(segment):
    print "segment {}, from: {}, to: {}:".format(segment['properties']['SEGMENT_ID'], segment['properties']['FROM_STR'], segment['properties']['TO_STR'])
    for x,y in segment['geometry']['coordinates']:
        print "{}, {}".format(y, x)
    print "---"

def hunt(street):
    for x in data:
        if street in x['properties']['STREET_NM']: printify(x) 

