console.log('Loading function');
var AWS = require('aws-sdk');
var dynamo = new AWS.DynamoDB.DocumentClient();
var table = "bls_demo_data";

exports.handler = function(event, context) {
    //console.log('Received event:', JSON.stringify(event, null, 2));
   var params = {
    TableName:table,
    Item:{
        "binid": parseInt(event.binid),
        "time": event.time,
        "binlocation": event.binlocation,
        "binlevel": parseInt(event.binlevel)
        }
    };

    console.log("Adding a new device data...",params);
    dynamo.put(params, function(err, data) {
        if (err) {
            console.error("Unable to add device. Error JSON:", JSON.stringify(err, null, 2));
            context.fail();
        } else {
            console.log("Added device:", JSON.stringify(data, null, 2));
            context.succeed();
        }
    });
}