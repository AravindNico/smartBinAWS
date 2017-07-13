(function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);var f=new Error("Cannot find module '"+o+"'");throw f.code="MODULE_NOT_FOUND",f}var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(require,module,exports){
function getBinLatest(map){
    console.log(map)
    const deviceModule = require('aws-iot-device-sdk').device;
    var device = deviceModule({
      keyPath: 'bls_demo.private.key',
      certPath: 'bls_demo.cert.pem',
      caPath: 'root-CA.crt',
      clientId: 'bls_demo'+ (Math.floor((Math.random() * 100000) + 1)),
      host: 'a1irgsu21jifu4.iot.ap-southeast-1.amazonaws.com'
   });
    console.log(deviceModule)
}
function customIcons(map,data){
    console.log(data)
    var iconBase = '/home/aravind/WORK/WebApp/mapRouting/final/';
    var icons = {
        lvl1: {
            url: iconBase + 'tcan_1.png',
            scaledSize: new google.maps.Size(30, 30)
        },
        lvl2: {
            url: iconBase + 'tcan_2.png',
            scaledSize: new google.maps.Size(30, 30)
        },
        lvl3: {
            url: iconBase + 'tcan_3.png',
            scaledSize: new google.maps.Size(30, 30)
        },
        lvl4: {
            url: iconBase + 'tcan_4.png',
            scaledSize: new google.maps.Size(30, 30)
        },
        lvl5: {
            url: iconBase + 'tcan_5.png',
            scaledSize: new google.maps.Size(30, 30)
        }
    };

    var features = [
        {
            position: new google.maps.LatLng(12.901060,77.614589),
            title:"BTM Layout",
            type: 'lvl1'
        }, {
            position: new google.maps.LatLng(12.926712,77.600398),
            title:"Jayanagar East",
            type: 'lvl2'
        }, {
            position: new google.maps.LatLng(12.936500,77.585078),
            title:"Tilak Nagar",
            type: 'lvl3'
        }, {
            position: new google.maps.LatLng(12.951515,77.590399),
            title:"Sudhama Nagar",
            type: 'lvl5'
        }, {
            position: new google.maps.LatLng(12.965902,77.604776),
            title:"Richmond Town",
            type: 'lvl4'
        }
    ];

    // Create markers.
    features.forEach(function(feature) {
        var marker = new google.maps.Marker({
            position: feature.position,
            title: feature.title,
            icon: icons[feature.type],
            draggable: true,
            map: map
        });
    

        var infowindow = new google.maps.InfoWindow({
            content: feature.title
        });

        marker.addListener('click', function() {
            infowindow.open(map, marker);
        });

    });

}
   
//    // Initialize the Amazon Cognito credentials provider
// AWS.config.region = 'us-east-1'; // Region
// AWS.config.credentials = new AWS.CognitoIdentityCredentials({
//     IdentityPoolId: 'us-east-1:8e43e6f1-83af-4710-83dc-2cab8f183f81',
// });             
// });

// $( document ).ready(function() {
    window.initMap = function(){
    // function initMap() {

        var directionsService = new google.maps.DirectionsService;
        var directionsDisplay = new google.maps.DirectionsRenderer;

        var map = new google.maps.Map(document.getElementById('map'), {
            zoom: 14,
            center: {lat: 12.9727151, lng: 77.6009235},
            mapTypeId: google.maps.MapTypeId.ROADMAP,
        });
        

        // var trafficLayer = new google.maps.TrafficLayer();
        // customIcons(map);
        // trafficLayer.setMap(map);
        

        directionsDisplay.setMap(map);
        getBinLatest(map);
        customIcons(map,0);
        document.getElementById('submit').addEventListener('click', function() {
            calculateAndDisplayRoute(directionsService, directionsDisplay);
        });
    }
// });

function calculateAndDisplayRoute(directionsService, directionsDisplay) {
    getBinLatest();
    var waypts = [];
    var checkboxArray = document.getElementById('waypoints');
    for (var i = 0; i < checkboxArray.length; i++) {
        if (checkboxArray.options[i].selected) {
            waypts.push({
                location: checkboxArray[i].value,
                stopover: true
            });
        }
    }

    console.log(waypts)
    console.log(document.getElementById('start').value);
    console.log(document.getElementById('end').value);
    
    var startpt = document.getElementById('start').value;
    var stoppt = document.getElementById('end').value;
    directionsService.route({
        origin: startpt,
        destination: stoppt,
        waypoints: waypts,
        optimizeWaypoints: true,
        travelMode: 'DRIVING'
    }, function(response, status) {
            if (status === 'OK') {
                directionsDisplay.setDirections(response);
                var route = response.routes[0];
                var summaryPanel = document.getElementById('directions-panel');
                summaryPanel.innerHTML = '';
        // For each route, display summary information.
                for (var i = 0; i < route.legs.length; i++) {
                    var routeSegment = i + 1;
                    summaryPanel.innerHTML += '<b>Route Segment: ' + routeSegment +  '</b><br>';
                    summaryPanel.innerHTML += route.legs[i].start_address + ' to ';
                    summaryPanel.innerHTML += route.legs[i].end_address + '<br>';
                    summaryPanel.innerHTML += route.legs[i].distance.text + '<br><br>';
                }
            } else {
                window.alert('Directions request failed due to ' + status);
            }
    });
}

},{"aws-iot-device-sdk":"aws-iot-device-sdk"}]},{},[1]);
