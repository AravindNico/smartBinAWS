from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import sys
import logging
import time
import argparse
import random
import requests
import datetime


bin1 = 0
bin2 = 0
bin3 = 0
bin4 = 0
bin5 = 0

bin1location = '12.901060,77.614589'
bin2location = '12.926712,77.600398'
bin3location = '12.936500,77.585078'
bin4location = '12.951515,77.590399'
bin5location = '12.965902,77.604776'

binLocationArray = [bin1location,bin2location,bin3location,bin4location,bin5location]

count = 1 

# Custom MQTT message callback
def customCallback(client, userdata, message):
	print("Received a new message: ")
	print(message.payload)
	print("from topic: ")
	print(message.topic)
	print("--------------\n\n")

# Read in command-line parameters
parser = argparse.ArgumentParser()
parser.add_argument("-e", "--endpoint", action="store", required=True, dest="host", help="Your AWS IoT custom endpoint")
parser.add_argument("-r", "--rootCA", action="store", required=True, dest="rootCAPath", help="Root CA file path")
parser.add_argument("-c", "--cert", action="store", dest="certificatePath", help="Certificate file path")
parser.add_argument("-k", "--key", action="store", dest="privateKeyPath", help="Private key file path")
parser.add_argument("-w", "--websocket", action="store_true", dest="useWebsocket", default=False,
                    help="Use MQTT over WebSocket")
parser.add_argument("-id", "--clientId", action="store", dest="clientId", default="bls_demo", help="Targeted client id")
parser.add_argument("-t", "--topic", action="store", dest="topic", default="test/topic", help="Targeted topic")

args = parser.parse_args()
host = args.host
rootCAPath = args.rootCAPath
certificatePath = args.certificatePath
privateKeyPath = args.privateKeyPath
useWebsocket = args.useWebsocket
clientId = args.clientId
topic = args.topic

if args.useWebsocket and args.certificatePath and args.privateKeyPath:
	parser.error("X.509 cert authentication and WebSocket are mutual exclusive. Please pick one.")
	exit(2)

if not args.useWebsocket and (not args.certificatePath or not args.privateKeyPath):
	parser.error("Missing credentials for authentication.")
	exit(2)

# Configure logging
# logger = logging.getLogger("AWSIoTPythonSDK.core")
# logger.setLevel(logging.DEBUG)
# streamHandler = logging.StreamHandler()
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# streamHandler.setFormatter(formatter)
# logger.addHandler(streamHandler)

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None
if useWebsocket:
	myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId, useWebsocket=True)
	myAWSIoTMQTTClient.configureEndpoint(host, 443)
	myAWSIoTMQTTClient.configureCredentials(rootCAPath)
else:
	myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
	myAWSIoTMQTTClient.configureEndpoint(host, 8883)
	myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()
# myAWSIoTMQTTClient.subscribe(topic, 1, customCallback)
time.sleep(2)

# Publish to the same topic in a loop forever

while True:
	bin1 = bin1 + random.randint(1,3)
	bin2 = bin2 + random.randint(3,6)
	bin3 = bin3 + random.randint(1,3)
	bin4 = bin4 + random.randint(1,3)
	bin5 = bin5 + random.randint(3,6)
	
	binLevelArray = [bin1,bin2,bin3,bin4,bin5]

	for x in range(1,6):

		currentBin = binLevelArray[x-1]
		currentBinLocation = binLocationArray[x-1]
		
		data = str({'binid':str(x),'time':str('{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())),'binlevel':str(currentBin),'binlocation':str(currentBinLocation)})
		print(data)

		myAWSIoTMQTTClient.publish(topic, str(data), 1)
		time.sleep(5)

	print (count, ". bin1 value is", bin1, " bin2 value is", bin2," bin3 value is", bin3, " bin4 value is", bin4," bin5 value is", bin5)
	if bin1 >= 90 or bin2 >= 90 or bin3 >= 90 or bin4 >= 90 or bin5 >= 90:
		if bin1 >= 90:
			bin1 = 0
		elif bin2 >= 90:
			bin2 = 0
		elif bin3 >= 90:
			bin3 = 0
		elif bin4 >= 90:
			bin4 = 0
		elif bin5 >= 90:
			bin5 = 0
	count += 1

