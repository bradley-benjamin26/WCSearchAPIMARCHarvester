#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import re
import string

year = str(raw_input('Please input the year for your query: '))
wskey = str(raw_input('Please provide your wskey: '))
urlInput = str(raw_input('PQ1 = search.proquest.com; PQ2 = gateway.proquest.com; PQ3 = wwwlib.umi.com; or input a custom url: '))
ebkCheck = raw_input("Check for ebooks?(yes/no): ")
langCheck = raw_input("Checked for English items only?: ")
degChecker = raw_input("search for dissertations? ")
title = str(raw_input("File name for output: "))
alpha = list(string.ascii_uppercase)
max = ''



if ebkCheck == 'yes':
	ebk = '+and+srw.mt%3Dweb'
else:
	ebk = ''

if langCheck == 'yes':
	lang = '+and+srw.la%3Deng'
else:
	lang = ''

if degChecker == 'yes':
	deg = '+and+srw.mt%3Ddeg'
else:
	deg = ''

if urlInput == "PQ1":
      queryUrl= "search.proquest.com/"
elif urlInput == "PQ2":
      queryUrl = "gateway.proquest.com/"
elif urlInput == "PQ3":
	queryUrl = "wwwlib.umi.com/"
else:
      queryUrl = urlInput
      
url = 'http://www.worldcat.org/webservices/catalog/search/worldcat/sru?query=srw.am%3D%22'+queryUrl+'%2a%22'+deg+ebk+lang+'+and+srw.yr%3D'+year+'&wskey='+wskey+'&servicelevel=full'
	
#sends initial request to find the number of results to determine course of action
r = requests.get(url).text
records = r.encode('utf-8')
marcRecords = str(records)
m = re.search(r'<numberOfRecords>(\d+)</numberOfRecords>', marcRecords)
beginpointMax = int(m.group(1))

#if the query returns more than 10,000 results which is greater than can be downloaded, the script performs a search through the alphabet for titles otherwise it will iterate through results by pages only

if beginpointMax > 10000:
	print('Results greater than 10,000. Performing title searches ' + str(beginpointMax))
	with open(title + ".txt", "a+") as f:	
		for letter in alpha:
			url = 'http://www.worldcat.org/webservices/catalog/search/worldcat/sru?query=srw.am%3D%22'+queryUrl+'%2a%22+and+srw.ti%3D%22'+letter+'%22'+deg+ebk+lang+'+and+srw.yr%3D'+year+'&wskey='+wskey+'&servicelevel=full&maximumRecords=100&startRecord='
			search = requests.get(url).text
			results = search.encode('utf-8')									
			data = str(results)
			m = re.search(r'<numberOfRecords>(\d+)</numberOfRecords>', data)
			max = int(m.group(1))
			print("Performing author search, title search returned too many hits: ", max)
			if max > 10000:
				authorAlpha = alpha
				for authorLetter in authorAlpha:
					beginPoint = 1
					while beginPoint <= max:
						print(letter, authorLetter, beginPoint, max)
						url = 'http://www.worldcat.org/webservices/catalog/search/worldcat/sru?query=srw.am%3D%22'+queryUrl+'%22+and+srw.ti%3D%22'+letter+'%22+and+srw.au%3D%22'+authorLetter+'%22'+deg+ebk+lang+'+and+srw.yr%3D'+year+'&wskey='+wskey+'&servicelevel=full&maximumRecords=100&startRecord=' + str(beginPoint)
						search = requests.get(url).text
						results = search.encode('utf-8')					
						data = str(results)
						beginPoint += 100
						f.write(data)
						m = re.search(r'<numberOfRecords>(\d+)</numberOfRecords>', data)
						max = int(m.group(1))
			else:
				beginPoint = 1			
				while beginPoint <= max + 1:
					print(letter, beginPoint, max)
					url = 'http://www.worldcat.org/webservices/catalog/search/worldcat/sru?query=srw.am%3D%22'+queryUrl+'%22+and+srw.ti%3D%22'+letter+'%22'+deg+ebk+lang+'+and+srw.yr%3D'+year+'&wskey='+wskey+'&servicelevel=full&maximumRecords=100&startRecord=' + str(beginPoint)
					search = requests.get(url).text
					results = search.encode('utf-8')					
					data = str(results)
					beginPoint += 100
					f.write(data)
					m = re.search(r'<numberOfRecords>(\d+)</numberOfRecords>', data)
					max = int(m.group(1))
		else:
			print('done')
		
else:	
	beginPoint = 1
	while beginPoint <= beginpointMax + 1:
		with open(title + ".txt", "a+") as f:
			print(beginPoint, beginpointMax)
			print("New value of beginPoint is: " + str(beginPoint))
			url = 'http://www.worldcat.org/webservices/catalog/search/worldcat/sru?query=srw.am%3D%22'+queryUrl+'%22'+deg+ebk+lang+'+and+srw.yr%3D'+year+'&wskey='+wskey+'&servicelevel=full&maximumRecords=100&startRecord=' + str(beginPoint)
			r = requests.get(url).text
			records = r.encode('utf-8')			
			marcRecords = str(records)
			beginPoint += 100
			f.write(marcRecords)
			if beginPoint == 1:
				m = re.search(r'<numberOfRecords>(\d+)</numberOfRecords>', marcRecords)
				beginpointMax = int(m.group(1))
				beginPoint += 100
				
			else:
				beginPoint += 100
	else:
		print('done')
