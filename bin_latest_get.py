import requests
import time


while True:

	selection = int(raw_input("\n\nEnter 1 for getlatest  \n"))

	if (selection == 1):

		primarykey = raw_input("\nEnter the binid (1 to 5)\n\t")
		primarykey = str(primarykey)
		print(primarykey)
		'''aws db add starting'''
		#payload = "{\"timeStamp\":"+str(timeStamp)+",\"binId\":"+str(endPoint_dict[binIdValue][0])+",\"fillLevel\":"+str(trashValue)+",\"batteryLevel\":"+str(batteryValue)+"}"
		#print payload
		try:
			amazon_aws_api = requests.get('https://wqwaaboyr4.execute-api.ap-southeast-1.amazonaws.com/newStage/latest/'+primarykey)
		except Exception as e:
			print("AWS API call error ==> %s" %e)

		if amazon_aws_api.text != "{}":
			print("AWS resp ==> %s" %amazon_aws_api.text)						

		'''aws db add ending'''

	else:
		print("Wrong selection")

	time.sleep(10)			



##AWS TRAINING PUT DATA TO DYNAMO DB

# https://ipneuji196.execute-api.ap-southeast-1.amazonaws.com/bls_training_put_data
# https://wqwaaboyr4.execute-api.ap-southeast-1.amazonaws.com/training_get_latest
'''

{
    "binid":1,
    "time":"27/06 6:30",
    "binlevel":23,
    "binlocation":"00.0000,00.0000"
}

'''