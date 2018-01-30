#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests

year = str(raw_input('Please input the year for your query: '))
wskey = str(raw_input('Please provide your wskey: '))
print("If you are want to search for search.proquest.com, enter PQ1. If you want to search for gateway.proquest.com enter PQ2. Otherwise, input a custom URL.")
urlInput = str(raw_input('Please provide url for query: '))
beginPoint = 1

if urlInput == "PQ1":
      queryUrl= "search.proquest.com/"
elif urlInput == "PQ2":
      queryUrl = "gateway.proquest.com/"
else:
      queryUrl = urlInput

while beginPoint <= 10001:
	with open("PQDTMarcRecords" + year + ".txt", "a+") as f:
#Creates and opens a text file and gives it the name PQDTMarcRecords and then the year given for the query (ex. PQDTMarcRecords2018)
		print("New value of beginPoint is: " + str(beginPoint))
		url = 'http://www.worldcat.org/webservices/catalog/search/worldcat/sru?query=srw.am%3D%22'+queryUrl+'%2a%22+and+srw.mt%3Ddeg+and+srw.yr%3D'+year+'&wskey='+wskey+'&servicelevel=full&maximumRecords=100&startRecord=' + str(beginPoint)
	#url variable includes the url that is being searched for, the material type for dissertation, the input year, the wskey that you MUST provide, and the variable for the beginning point for the page
 		r = requests.get(url).text
 		marcRecords = r.encode('utf-8')
 		f.write(marcRecords)
	#sends the request and writes the MARCXML to the file
 		beginPoint += 100
 	#100 is added to the beginPoint, and the loop runs again
else:
	f.close()
	print('done')
