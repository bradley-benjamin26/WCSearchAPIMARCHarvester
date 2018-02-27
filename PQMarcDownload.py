#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import re

year = str(input('Please input the year for your query: '))
wskey = str(input('Please provide your wskey: '))
urlInput = str(input('PQ1 = search.proquest.com; PQ2 = gateway.proquest.com; PQ3 = wwwlib.umi.com; or input a custom url: '))
beginPoint = 1
beginpointMax = 10001
loopCounter = 1

if urlInput == "PQ1":
      queryUrl= "search.proquest.com/"
elif urlInput == "PQ2":
      queryUrl = "gateway.proquest.com/"
elif urlInput == "PQ3":
	queryUrl = "wwwlib.umi.com/"
else:
      queryUrl = urlInput
	
while beginPoint <= beginpointMax:
	with open("PQDTMarcRecords" + year + ".txt", "a+") as f:
		print("loop number: " + str(loopCounter) + " and max number of records: " + str(beginpointMax))
#Creates and opens a text file and gives it the name PQDTMarcRecords and then the year given for the query (ex. PQDTMarcRecords2018)
		print("New value of beginPoint is: " + str(beginPoint))
		url = 'http://www.worldcat.org/webservices/catalog/search/worldcat/sru?query=srw.am%3D%22'+queryUrl+'%2a%22+and+srw.mt%3Ddeg+and+srw.mt%3Debk+and+srw.yr%3D'+year+'&wskey='+wskey+'&servicelevel=full&maximumRecords=100&startRecord=' + str(beginPoint)
#url variable includes the url that is being searched for, the material type for dissertation, the input year, the wskey that you MUST provide, and the variable for the beginning point for the page
		r = requests.get(url).text
		records = r.encode('utf-8')
		marcRecords = str(records)
		beginPoint += 100
		f.write(marcRecords)
		if loopCounter == 1:
			m = re.search(r'<numberOfRecords>(\d+)</numberOfRecords>', marcRecords)
			beginpointMax = int(m.group(1))
			loopCounter += 1
		else:
			loopCounter += 1
			
 	#100 is added to the beginPoint, and the loop runs again
else:
	print('done')
