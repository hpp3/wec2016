import json
import parse
import flask
import copy
from flask import Flask, request, send_from_directory
app = Flask(__name__, static_url_path='/static')

data = None
features = None
closures = None
closures_features = None

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)


@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)


@app.route('/')
def home():
    return app.send_static_file('index.html')


@app.route('/roads_count')
def get_roads_count():
    ret_val = {'roads_count': len(features)}
    return flask.jsonify(**ret_val)


def process_coordinates(input_features):
    input_copy = copy.deepcopy(input_features)
    roads_with_coordinates = []
    for feature in input_copy:
        coordinates = feature['geometry']['coordinates']
        if feature['geometry']['type'] == 'MultiLineString':
            coordinates_flatten = []
            for i in range(len(coordinates)):
                for j in range(len(coordinates[i])):
                    coordinates_flatten.append(coordinates[i][j][::-1])
            coordinates = coordinates_flatten
        else:
            for i in range(len(coordinates)):
                coordinates[i] = coordinates[i][::-1]

        road = {
            'geo_type': feature['geometry']['type'],
            'coords': coordinates
        }
        roads_with_coordinates.append(road)
    return roads_with_coordinates


@app.route('/roads')
def get_roads():
    start = int(request.args.get('start', 0))
    offset = int(request.args.get('offset', 200))
    roads = process_coordinates(features[start:start+offset])

    ret_val = {'roads': roads}
    return flask.jsonify(**ret_val)


@app.route('/closures')
def get_closures():
    closures = process_coordinates(closures_features)
    ret_val = {'closures': closures}
    return flask.jsonify(**ret_val)


@app.route('/optimal', methods=['POST'])
def get_optimal():
    input = request.data
    segment_ids = map(int, input.split(","))
    ret_val = {'optimal_paths': parse.getPaths(segment_ids)}
    return flask.jsonify(**ret_val)


@app.route('/original', methods=['POST'])
def get_original():
    input = request.data
    segment_ids = map(int, input.split(","))
    ret_val = {'original_path': parse.getCoords(segment_ids)}
    return flask.jsonify(**ret_val)


if __name__ == '__main__':
    with open('roads.json', 'r') as f:
        data = json.load(f)
        features = data['features']

    with open('closures.json', 'r') as f:
        closures = json.load(f)
        closures_features = closures['features']

    app.run(debug=True)
