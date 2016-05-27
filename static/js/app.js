//var app = angular.module('road', ['leaflet-directive']);
//
//app.controller('MapController', ['$scope', function($scope) {
//    angular.extend($scope, {
//        center: {
//            lat: 40.095,
//            lng: -3.823,
//            zoom: 4
//        },
//        defaults: {
//            scrollWheelZoom: false
//        }
//    });
//}]);

$(document).ready(function() {
    var map = L.map('mapid').setView([43.4643, -80.5204], 13);

    L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
});
