import json

import flask
from flask import Flask, request, send_from_directory
app = Flask(__name__, static_url_path='/static')

data = None
features = None


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


@app.route('/roads')
def get_roads():
    start = int(request.args.get('start', 0))
    offset = int(request.args.get('offset', 200))
    print start, offset
    roads = []
    for feature in features[start:start+offset]:
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
        roads.append(road)

    ret_val = {'roads': roads}
    return flask.jsonify(**ret_val)


if __name__ == '__main__':
    with open('roads.json', 'r') as f:
        data = json.load(f)
        features = data['features']

    app.run(debug=True)
