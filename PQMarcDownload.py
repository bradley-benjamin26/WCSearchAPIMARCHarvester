#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests

beginYear = int(raw_input('Please input year query to begin:'))
endYear = int(raw_input('And when would you like this query to end?'))
queryYear = beginYear
beginPoint = 1

while queryYear <= endYear:
	#user inputs which record the query should begin, startPoint. This value is passed into the variable beginPoint which is then iterated through with a while loop.
	with open("PQTD" + str(queryYear) + ".txt", "a+") as f:
	#creates a textfile which includes the year of the query in the file name for the sake of clarity.
		if beginPoint <= 10001:
			with open("PQTD" + str(queryYear) + ".txt", "a+") as f:
				print("New value of beginPoint is: ", beginPoint)
				urlYear = str(queryYear)
				url = 'http://www.worldcat.org/webservices/catalog/search/worldcat/sru?query=srw.am%3D%22search.proquest.com%2a%22+and+srw.mt%3Ddeg+and+srw.yr%3D'+urlYear+'&wskey=tJNbzAmM1rK5dzXShgp2DEamIZnAdYMVk0vK2deNmsexsySV79Mn3u3Pu8cNaQCKdjkqibt6XgVmeglQ&servicelevel=full&maximumRecords=100&startRecord='
	#once the beginPoint has surpassed 10,000 records, the script ends and closes the file.
 				requestingURL = url + str(beginPoint)
 				print(requestingURL)
 				r = requests.get(requestingURL).text
 				marcRecords = r.encode('utf-8')
 				f.write(marcRecords)
 				f.close()
 				beginPoint += 100
 			#writes the results of the api query to the file
			#adds 100 to the beginPoint and the loop starts again.
		else:
			f.close()
			queryYear += 1
			print('Completed: ', queryYear, "Records retrieved: ", beginPoint)
else:
	print("Completed query")