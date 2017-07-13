from __future__ import print_function # Python 2/3 compatibility
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import sys
import logging
import time
import argparse
import random
import requests
import datetime
import json
import demjson
import uuid

smartBinAWSIoTMQTTClient = None

BINPICKUP_THRESHOLD = 60;

def generateClientId(string_length=10):
    """Returns a random string of length string_length."""
    random = str(uuid.uuid4()) # Convert UUID format to a Python string.
    # random = random.upper() # Make all characters uppercase.
    random = random.replace("-","") # Remove the UUID '-'.
    return random[0:string_length] # Return the random string.

# Custom MQTT message callback
def debugCallback(client, userdata, message):
	print("Received a new message: ")
	print(message.payload)
	print("from topic: ")
	print(message.topic)
	print("--------------\n\n")


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
	smartBinAWSIoTMQTTClient.subscribe(topic, 1, debugCallback)

	# Configure logging
	logger = logging.getLogger("AWSIoTPythonSDK.core")
	logger.setLevel(logging.DEBUG)
	streamHandler = logging.StreamHandler()
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	streamHandler.setFormatter(formatter)
	logger.addHandler(streamHandler)

def binpickupOperation():
	global smartBinAWSIoTMQTTClient,topic
	
	for x in range(1,6):
		binid = str(x)
		api_get_latest = requests.get('https://e4vxf5szne.execute-api.us-east-1.amazonaws.com/version1/getlatest/'+binid+'')
		data =  api_get_latest.text
		data_dict = demjson.decode(data)
		print(data_dict)
		print(data_dict["Items"][0]["binlevel"]["N"])
		if (int(data_dict["Items"][0]["binlevel"]["N"]) >= BINPICKUP_THRESHOLD):
			currentBin = 0
			currentBinLocation = data_dict["Items"][0]["binlocation"]["S"]
			data = '{"requestType":"1","binid":"'+str(x)+'","time":"'+"{:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now())+'","binlevel":"'+str(currentBin)+'","binlocation":"'+str(currentBinLocation)+'"}'
			print (data)
			smartBinAWSIoTMQTTClient.publish(topic, data, 1)
			time.sleep(3)
		else:
			time.sleep(3)

if __name__ == '__main__':
	AWSInitialization()
	binpickupOperation()
		
