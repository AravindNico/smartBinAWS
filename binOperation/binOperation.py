from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import sys
import logging
import time
import argparse
import random
import requests
import datetime
import demjson
import json
import uuid

binLevelDB = {
	"bin1":{
		"id":1,
		"level": 0,
		"fillFrequency": 0,
		"binLocation": '12.901060,77.614589'
	},
	"bin2":{
		"id":2,
		"level": 0,
		"fillFrequency": 1,
		"binLocation": '12.926712,77.600398'
	},
	"bin3":{
		"id":3,
		"level": 0,
		"fillFrequency": 0,
		"binLocation": '12.936500,77.585078'
	},
	"bin4":{
		"id":4,
		"level": 0,
		"fillFrequency": 1,
		"binLocation": '12.9384362,77.6303143'
	},
	"bin5":{
		"id":5,
		"level": 0,
		"fillFrequency": 0,
		"binLocation": '12.965902,77.604776'
	}
}

smartBinAWSIoTMQTTClient = None

BINFILLING_THRESHOLD = 95;
BINPICKUP_THRESHOLD = 60;

SLOW_FILLING_RATE = 2;
FAST_FILLING_RATE = 5;

def generateClientId(string_length=10):
    """Returns a random string of length string_length."""
    random = str(uuid.uuid4()) # Convert UUID format to a Python string.
    # random = random.upper() # Make all characters uppercase.
    random = random.replace("-","") # Remove the UUID '-'.
    return random[0:string_length] # Return the random string.

# Custom MQTT message callback
def pickupResetCallback(client, userdata, message):
	print("Received a new message: ")
	print(message.topic)
	binClearUpMessage = json.loads(message.payload.decode("utf-8"))
	print(binClearUpMessage)
	print("--------------\n\n")

	if(binClearUpMessage["requestType"] == '1'):
		binLevelDB["bin"+binClearUpMessage["binid"]]["level"] = 0
	else:
		pass

def AWSInitialization():
	global smartBinAWSIoTMQTTClient,topic
	parser = argparse.ArgumentParser()
	parser.add_argument("-e", "--endpoint", action="store", required=True, dest="host", help="Your AWS IoT custom endpoint")
	parser.add_argument("-r", "--rootCA", action="store", required=True, dest="rootCAPath", help="Root CA file path")
	parser.add_argument("-c", "--cert", action="store", dest="certificatePath", help="Certificate file path")
	parser.add_argument("-k", "--key", action="store", dest="privateKeyPath", help="Private key file path")
	parser.add_argument("-w", "--websocket", action="store_true", dest="useWebsocket", default=False,
	                    help="Use MQTT over WebSocket")
	parser.add_argument("-id", "--clientId", action="store", dest="clientId", default="bls_demo", help="Targeted client id")
	parser.add_argument("-t", "--topic", action="store", dest="topic", default="binoperation", help="Targeted topic")

	args = parser.parse_args()
	host = args.host
	rootCAPath = args.rootCAPath
	certificatePath = args.certificatePath
	privateKeyPath = args.privateKeyPath
	useWebsocket = args.useWebsocket
	clientId = args.clientId.join(generateClientId(6))
	topic = args.topic

	if args.useWebsocket and args.certificatePath and args.privateKeyPath:
		parser.error("X.509 cert authentication and WebSocket are mutual exclusive. Please pick one.")
		exit(2)

	if not args.useWebsocket and (not args.certificatePath or not args.privateKeyPath):
		parser.error("Missing credentials for authentication.")
		exit(2)


	if useWebsocket:
		smartBinAWSIoTMQTTClient = AWSIoTMQTTClient(clientId, useWebsocket=True)
		smartBinAWSIoTMQTTClient.configureEndpoint(host, 443)
		smartBinAWSIoTMQTTClient.configureCredentials(rootCAPath)
	else:
		smartBinAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
		smartBinAWSIoTMQTTClient.configureEndpoint(host, 8883)
		smartBinAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

	# AWSIoTMQTTClient connection configuration
	smartBinAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
	smartBinAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
	smartBinAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
	smartBinAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
	smartBinAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

	# Connect and subscribe to AWS IoT
	smartBinAWSIoTMQTTClient.connect()
	smartBinAWSIoTMQTTClient.subscribe(topic, 1, pickupResetCallback)

	# Configure logging
	logger = logging.getLogger("AWSIoTPythonSDK.core")
	logger.setLevel(logging.DEBUG)
	streamHandler = logging.StreamHandler()
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	streamHandler.setFormatter(formatter)
	logger.addHandler(streamHandler)

def binOperation():
	global smartBinAWSIoTMQTTClient,topic, binLevelDB

	for key in binLevelDB:
		if binLevelDB[key]["level"] <= BINFILLING_THRESHOLD:
			
			if binLevelDB[key]["fillFrequency"] == 0:
				binLevelDB[key]["level"] = binLevelDB[key]["level"] + random.randint(1,SLOW_FILLING_RATE)
			else:
				binLevelDB[key]["level"] = binLevelDB[key]["level"] + random.randint(FAST_FILLING_RATE,FAST_FILLING_RATE+3)
			
			data = '{"requestType":"0","binid":"'+str(binLevelDB[key]["id"])+'","time":"'+"{:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now())+'","binlevel":"'+str(binLevelDB[key]["level"])+'","binlocation":"'+str(binLevelDB[key]["binLocation"])+'"}'	
			smartBinAWSIoTMQTTClient.publish(topic, data, 1)
		else:
			data = '{"requestType":"0","binid":"'+str(binLevelDB[key]["id"])+'","time":"'+"{:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now())+'","binlevel":"'+str(binLevelDB[key]["level"])+'","binlocation":"'+str(binLevelDB[key]["binLocation"])+'"}'
			smartBinAWSIoTMQTTClient.publish(topic, data, 1)	
		time.sleep(3)

if __name__ == '__main__':
	AWSInitialization()
	while True:
		binOperation()
		
