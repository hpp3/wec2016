var app = angular.module('road', []);

app.controller('MapController', ['$scope', '$http', function($scope, $http) {
    var map = L.map('mapid').setView([43.4643, -80.5204], 15);
    var roads = [];

    L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    $http({
      method: 'GET',
      url: '/roads_count'
    }).then(function successCallback(response) {
        var totalRoadsCount = response.data.roads_count;
        var batchSize = 200;
        var receivedBatches = 0;
        var totalBatchesNeeded = Math.ceil(totalRoadsCount / batchSize);
        for (var batchStart = 0; batchStart < totalRoadsCount; batchStart += batchSize) {
            var offset = batchSize;
            if (totalRoadsCount - batchStart < batchSize) {
                offset = totalRoadsCount - batchStart;
            }
            $http({
              method: 'GET',
              params: {start: batchStart, offset: offset},
              url: '/roads'
            }).then(function successCallback(response) {
                receivedBatches += 1;
                if (receivedBatches == totalBatchesNeeded) {
                    getClosures();
                }

                roads = response.data.roads;

                _.each(roads, function(road) {
                    var coordinates = road.coords;
                    if (coordinates && coordinates.length) {
                        var line = new L.Polyline(coordinates, {
                            color: 'blue',
                            weight: 3,
                            opacity: 0.5,
                            smoothFactor: 1
                        });
                        line.addTo(map);
                    }
                });
            }, function errorCallback(response) {
                console.log('error', response);
            });
        }
    }, function errorCallback(response) {
        console.log('error', response);
    });
    addLegend();

    var closures = [];

    function getClosures() {
        $http({
          method: 'GET',
          url: '/closures'
        }).then(function successCallback(response) {
            closures = response.data.closures;

            _.each(closures, function(road) {
                var coordinates = road.coords;
                if (coordinates && coordinates.length) {
                    var line = new L.Polyline(coordinates, {
                        color: 'red',
                        weight: 3,
                        opacity: 0.5,
                        smoothFactor: 1
                    });
                    line.addTo(map);
                }
            });
        }, function errorCallback(response) {
            console.log('error', response);
        });
    }

    $scope.getPaths = function() {
        $scope.getOptimalRoute();
        $scope.getOriginal();
    };

    $scope.optimalPaths = [];
    $scope.pathsReturned = false;
    $scope.getOptimalRoute = function() {

        var LeafIcon = L.Icon.extend({
            options: {
                shadowUrl: 'static/images/leaf-shadow.png',
                iconSize:     [38, 95],
                shadowSize:   [50, 64],
                iconAnchor:   [22, 94],
                shadowAnchor: [4, 62],
                popupAnchor:  [-3, -76]
            }
        });

        var greenIcon = new LeafIcon({iconUrl: 'static/images/leaf-green.png'}),
            redIcon = new LeafIcon({iconUrl: 'static/images/leaf-red.png'}),
            orangeIcon = new LeafIcon({iconUrl: 'static/images/leaf-orange.png'});

        var iconSelection = [greenIcon, redIcon, orangeIcon];

        $http({
            method: 'POST',
            data: $scope.segmentIds,
            url: '/optimal'
        }).then(function successCallback(response) {
            var optimalCoords = response.data.optimal_paths;

            _.each(optimalCoords, function(pathCoords, idx) {
                _.each(pathCoords, function (coord) {
                   var marker = L.marker(coord, {icon: iconSelection[idx]}).addTo(map);
                });
            });
            $scope.optimalPaths = optimalPaths;
        }, function errorCallback(response) {
            console.log('error', response);
        });
    };

    $scope.getOriginal = function() {
        $http({
            method: 'POST',
            data: $scope.segmentIds,
            url: '/original'
        }).then(function successCallback(response) {
            var originalCoords = [response.data.original_path];
            var optimalPaths = [];
            _.each(originalCoords, function(pathCoords) {
                var line = new L.Polyline(pathCoords, {
                    color: 'yellow',
                    weight: 5,
                    opacity: 1,
                    smoothFactor: 1
                });
                optimalPaths.push(line);
                line.addTo(map);
            });
            $scope.optimalPaths = optimalPaths;
        }, function errorCallback(response) {
            console.log('error', response);
        });
    };

    function addLegend() {
        var legend = L.control({position: 'bottomright'});

        legend.onAdd = function(map) {

            var div = L.DomUtil.create('div', 'road-legend');
            var labels = [
                {
                    color: 'red',
                    label: 'Closure'
                },
                {
                    color: 'yellow',
                    label: 'Original Route'
                }
            ];

            var labelsOptimal = [
                {
                    color: 'Green Leafs',
                    label: 'Most optimal route'
                },
                {
                    color: 'Red Leafs',
                    label: 'Second most optimal Route'
                },
                {
                    color: 'Orange Leafs',
                    label: 'Third most optimal Route'
                }
            ];

            // loop through our density intervals and generate a label with a colored square for each interval
            div.innerHTML += '<ul class="list-unstyled">';
            for (var i = 0; i < labels.length; i++) {
                div.innerHTML += '<li><span style="background:' + labels[i].color + '">&#x25A2;</span>&nbsp;&nbsp;' + labels[i].label + '</li>'
            }

            for (var i = 0; i < labelsOptimal.length; i++) {
                div.innerHTML += '<li>' + labelsOptimal[i].color + ' - ' + labelsOptimal[i].label + '</li>';
            }
            div.innerHTML += '</ul>';

            return div;
        };

        legend.addTo(map);
    }

}]);
