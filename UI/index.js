//
// Instantiate the AWS SDK and configuration objects.  The AWS SDK for 
// JavaScript (aws-sdk) is used for Cognito Identity/Authentication, and 
// the AWS IoT SDK for JavaScript (aws-iot-device-sdk) is used for the
// WebSocket connection to AWS IoT and device shadow APIs.
// 
var AWS = require('aws-sdk');
var AWSIoTData = require('aws-iot-device-sdk');
var ConfigData = awsConfig;

var AWSConfiguration = {
    poolId: ConfigData.Config.poolId, // 'YourCognitoIdentityPoolId'
    host: ConfigData.Config.host, // 'YourAWSIoTEndpoint', e.g. 'prefix.iot.us-east-1.amazonaws.com'
    region: ConfigData.Config.region // 'YourAwsRegion', e.g. 'us-east-1'
};

console.log('Loaded AWS SDK for JavaScript and AWS IoT SDK for Node.js');

// Remember our current subscription topic here.
var currentlySubscribedTopic = ConfigData.Config.subscribedTopic;

// Remember our message history here.
var messageHistory = '';

// Create a client id to use when connecting to AWS IoT.
var clientId = 'bls_demo' + (Math.floor((Math.random() * 100000) + 1));

// Initialize our configuration.
AWS.config.region = AWSConfiguration.region;

AWS.config.credentials = new AWS.CognitoIdentityCredentials({
    IdentityPoolId: AWSConfiguration.poolId
});

// Create the AWS IoT device object.  Note that the credentials must be 
// initialized with empty strings; when we successfully authenticate to
// the Cognito Identity Pool, the credentials will be dynamically updated.

const mqttClient = AWSIoTData.device({
   // Set the AWS region we will operate in.
    region: AWS.config.region,
   ////Set the AWS IoT Host Endpoint
    host:AWSConfiguration.host,
   // Use the clientId created earlier.
    clientId: clientId,
   // Connect via secure WebSocket
    protocol: 'wss',
   // Set the maximum reconnect time to 8 seconds; this is a browser application
   // so we don't want to leave the user waiting too long for reconnection after
   // re-connecting to the network/re-opening their laptop/etc...
    maximumReconnectTimeMs: 8000,
   // Enable console debugging information (optional)
    debug: true,
   // IMPORTANT: the AWS access key ID, secret key, and sesion token must be 
   // initialized with empty strings.
    accessKeyId: '',
    secretKey: '',
    sessionToken: ''
});

//
// Attempt to authenticate to the Cognito Identity Pool.  Note that this
// example only supports use of a pool which allows unauthenticated 
// identities.
//
var cognitoIdentity = new AWS.CognitoIdentity();
AWS.config.credentials.get(function(err, data) {
   if (!err) {
      console.log('retrieved identity: ' + AWS.config.credentials.identityId);
      var params = {
         IdentityId: AWS.config.credentials.identityId
      };
      cognitoIdentity.getCredentialsForIdentity(params, function(err, data) {
         if (!err) {
            //
            // Update our latest AWS credentials; the MQTT client will use these
            // during its next reconnect attempt.
            //
            mqttClient.updateWebSocketCredentials(data.Credentials.AccessKeyId,
               data.Credentials.SecretKey,
               data.Credentials.SessionToken);
         } else {
            console.log('error retrieving credentials: ' + err);
            alert('error retrieving credentials: ' + err);
         }
      });
   } else {
      console.log('error retrieving identity:' + err);
      alert('error retrieving identity: ' + err);
   }
});

//
// Connect handler; fetch latest shadow documents.
// Subscribe to lifecycle events on the first connect event.
//
window.mqttClientConnectHandler = function() {
   console.log('connect');
   // Subscribe to our current topic.
   mqttClient.subscribe(currentlySubscribedTopic);
};

//
// Reconnect handler; 
window.mqttClientReconnectHandler = function() {
   console.log('reconnect');
};

//
// Install connect/reconnect event handlers.
//
mqttClient.on('connect', window.mqttClientConnectHandler);
mqttClient.on('reconnect', window.mqttClientReconnectHandler);

// Create DynamoDB service object
var docClient = new AWS.DynamoDB.DocumentClient();
var waypts = [];
var map;
var wayptsOrder ;
var pickupBinsList =[];

window.customIcons = function(topic,payload){

    
    var dataPayload = JSON.parse(payload.toString())
    console.log(dataPayload)
    var iconBase = 'binIcons/';
    if(parseInt(dataPayload.binlevel) < 20){
        var icons = {
            url: iconBase + 'tcan_1.png',
            scaledSize: new google.maps.Size(30, 30)
        }
        markerColorMapping(icons)
    }
    else if(parseInt(dataPayload.binlevel) < 40){
        var icons = {
            url: iconBase + 'tcan_2.png',
            scaledSize: new google.maps.Size(30, 30)
        }
        markerColorMapping(icons)
    }
    else if(parseInt(dataPayload.binlevel) < 60){
        var icons = {
            url: iconBase + 'tcan_3.png',
            scaledSize: new google.maps.Size(30, 30)
        }
        markerColorMapping(icons)
    }
    else if(parseInt(dataPayload.binlevel) < 80){
        var icons = {
            url: iconBase + 'tcan_4.png',
            scaledSize: new google.maps.Size(30, 30)
        }
        markerColorMapping(icons)
    }
    else if(parseInt(dataPayload.binlevel) < 110){
        var icons = {
            url: iconBase + 'tcan_5.png',
            scaledSize: new google.maps.Size(30, 30)
        }
        markerColorMapping(icons)
    }
    function markerColorMapping(icons){
        var binData = {
            "1":{
                position: new google.maps.LatLng(12.905911, 77.612603),
                title: "BTM Layout"
            },
            "2":{
                position: new google.maps.LatLng(12.916868, 77.583318),
                title: "Jayanagar East"
            },
            "3":{
                position: new google.maps.LatLng(12.936500,77.585078),
                title: "Tilak Nagar"
            },
            "4":{
                position: new google.maps.LatLng(12.9384362,77.6303143),
                title: "Eijpura"
            },
            "5":{
                position: new google.maps.LatLng(12.965902,77.604776),
                title: "Richmond Town"
            }

        }
        var marker = new google.maps.Marker({
            position: binData[dataPayload.binid].position,
            title: binData[dataPayload.binid].title,
            icon: icons,
            draggable: false,
            map: map
        });
        var infowindow = new google.maps.InfoWindow({
            content: 'fill level :'+dataPayload.binlevel+' %'
        });

        marker.addListener('click', function() {
            infowindow.open(map, marker);
        });
    }
}
   

window.initMap = function(){

    var directionsService = new google.maps.DirectionsService;
    var directionsDisplay = new google.maps.DirectionsRenderer;

    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 14,
        center: {lat: 12.9727151, lng: 77.6009235},
        mapTypeId: google.maps.MapTypeId.ROADMAP,
    });

    directionsDisplay.setMap(map);
    
    document.getElementById('submit').addEventListener('click', function() {
        calculateAndDisplayRoute(map,directionsService, directionsDisplay);
    });
}

mqttClient.on('message', window.customIcons);

function calculateAndDisplayRoute(map,directionsService, directionsDisplay) {
    var geocoder = new google.maps.Geocoder;
    for(var i = 1 ; i <= 5 ; i++){
        var params = {
            TableName: ConfigData.Config.dynamoDBTable,
            KeyConditionExpression: 'binid = :v1',
            ExpressionAttributeValues: {
                ':v1': i
            },
            Limit:1,
            ScanIndexForward:false
        }

        docClient.query(params, function(err, data) {
            // console.log(data)
            if (err) {
                console.log("Error", err);
            } else {
                if(data.Items[0].binlevel > ConfigData.Config.binpickupThreshold){
                    var loc = data.Items[0].binlocation
                    latlong = loc.split(",",2);
                    var l = {lat:parseFloat(latlong[0]),lng:parseFloat(latlong[1])}
                    geocoder.geocode({'location': l}, function(results, status) {
                        if (status === 'OK') {
                            if (results[1]) {
                                pickupBinsList.push({binid : data.Items[0].binid,time : data.Items[0].time,binlevel : data.Items[0].binlevel ,binlocation : data.Items[0].binlocation})
                                waypts.push({location:results[1].formatted_address,stopover:true})
                                // console.log(waypts)
                            } else {
                                window.alert('No results found');
                            }
                        } else {
                            window.alert('Geocoder failed due to: ' + status);
                        }
                    });
                }
            }
           
        });
    }
    setTimeout(
        function(){ 
            // console.log(waypts,i)
            var startpt = document.getElementById('start').value;
            var stoppt = document.getElementById('end').value;
            directionsService.route({
                origin: startpt,
                destination: stoppt,
                waypoints: waypts,
                optimizeWaypoints: true,
                travelMode: 'DRIVING'
            }, function(response, status) {
                console.log(status,response)
                    if (status === 'OK') {
                        directionsDisplay.setDirections(response);
                        var route = response.routes[0];
                        wayptsOrder = route.waypoint_order
                        // console.log(wayptsOrder)
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
                        console.log("error response : ",response)
                        window.alert('Directions request failed due to ' + status);
                    }
            }); 
        }, 3000);
}

function pickupOperation() {
    publishTopic = ConfigData.Config.subscribedTopic
    // console.log(pickupBinsList,wayptsOrder)   
   
    var i = 0
    pickupPublish(i)
    function pickupPublish(i){
        setTimeout(function(){
            if(i < wayptsOrder.length){
                publishMessage = '{"requestType":"1","binid":"'+pickupBinsList[wayptsOrder[i]].binid+'","time":"'+pickupBinsList[wayptsOrder[i]].time+'","binlevel":"0","binlocation":"'+pickupBinsList[wayptsOrder[i]].binlocation+'"}'
                console.log("to publish :",publishMessage)
                mqttClient.publish(publishTopic, publishMessage);
                i++;
                console.log("i :",i)
                pickupPublish(i)
            }else{
                pickupBinsList = [];
                wayptsOrder = [];
                waypts = [];
            }
        },5000)
    }
}