import random
import time
import requests
import datetime
import pytz

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
		r = requests.post('https://ipneuji196.execute-api.ap-southeast-1.amazonaws.com/bls_training_put_data/bls-put', data = data)
		print(data)
		print(r)
		time.sleep(10)
	
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
	

