# WCSearchAPIMARCHarvester


<h2>This documentation is out of date and I am working on providing updated documentation</h2>



<h2>Introduction to PQMarcDownload.py</h2>
PQMarcDownload is a little Python script that uses the <a href= "http://docs.python-requests.org/en/master/">Requests library</a> with the <a href="https://www.oclc.org/developer/develop/web-services/worldcat-search-api.en.html">OCLC WorldCat Search API</a> to query OCLC master records and download matching records. This query, designed to find records for ProQuest Dissertations and Theses Global,searches OCLC indexes for items whose material type (mt) matches "deg", and matches the url and year the user inputs.

The API returns records in MARC21XML, and the script iterates through the results (100 titles at a time up through the 10,000th result which is the API's limit) and writes the results to a file. One drawback of the script is that it doesn't know it has iterated through the results, so if you query returns 1,000 titles, it will keep querying the API until its internal counter hits 10,000. However, each time the script starts a new loop, it prints out the number for the top result on that page (ex. 101, 201, 301, 401, etc). If the script starts printing that information out rapidly it is a sign that it has downloaded everything and you can close the program. There is minimal harm in letting the script run to 10,000; it just means a little extra to clean up later on but also keep in mind OCLC limits the number of queries you can run a day.

I'm not much of a programmer, so if anyone has any ideas or suggestions, I'm very open to learning!

<h2>Using the Harvester</h2>

<h3>Getting set up</h3>
After downloading the script:
<ol>
  <li>You'll need to <a href="https://platform.worldcat.org/wskey/">request a wskey from OCLC</a>, if you haven't already.</li>
  <li>Install Python, if you haven't already.</li>
  <li>Install the Requests library</li>
</ol>

<h3>Running the Harvester</h3>
<ul>
  <li>I recommend sticking the script in its own folder.</li>
  <li>You can now open your terminal/shell to navigate to the folder and run the script</li>
  <li>Input the necessary data: the year for your query, your wskey, and the url you're searching for (note that the script is searching for a truncated script, so simply input the past of the URL, for example: search.proquest.com/ which will search for search.proquest.com/).</li>
  <li>Keep an eye on the script. If it begins to run really quickly, close the terminal because the query has pulled all the results and is writing empty results to the file.</li>
</ul>

<h2>Clean up and Transformation</h2>
<ul>
  <li>After running a few batches of the query for the same KB collection, I copy all the MARCXML into a single text file and begin to remove the 856 fields I don't want. Regular expressions can be pretty powerful to remove the urls you don't want and keep the ones you do behind.</li>
  <li>You'll also need to get rid of any other XML that isn't part of the MARC records to make sure MarcEdit can read the file. For example:</li>
This will appear before each loop so you can get rid of this with replace all:
  
  ```
<searchRetrieveResponse xmlns="http://www.loc.gov/zing/srw/" xmlns:oclcterms="http://purl.org/oclc/terms/"                      xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:diag="http://www.loc.gov/zing/srw/diagnostic/"              xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<version>1.1</version>
<numberOfRecords>3128</numberOfRecords>
 ```
 
 This will be at the end of each loop and needs to be deleted:
 
 ```
 <nextRecordPosition>401</nextRecordPosition>
<resultSetIdleTime/>
<echoedSearchRetrieveRequest xmlns:srw="http://www.loc.gov/zing/srw/">
<version>1.1</version>
<query>srw.am="gateway.proquest.com/*" and srw.mt=deg and srw.yr=2017</query>
<maximumRecords>100</maximumRecords>
<recordPacking>xml</recordPacking>
<startRecord>301</startRecord>
<sortKeys>relevance</sortKeys>
<wskey>tJNbzAmM1rK5dzXShgp2DEamIZnAdYMVk0vK2deNmsexsySV79Mn3u3Pu8cNaQCKdjkqibt6XgVmeglQ</wskey>
<servicelevel>full</servicelevel>
</echoedSearchRetrieveRequest>
</searchRetrieveResponse>
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<?xml-stylesheet type='text/xsl' href='/webservices/catalog/xsl/searchRetrieveResponse.xsl'?>
```
 
 Lastly, something like this will appear at the end of your query file. This is mostly what is generated when the script is looping after downloading everything your query returned:
 
 ```
 <searchRetrieveResponse xmlns="http://www.loc.gov/zing/srw/" xmlns:oclcterms="http://purl.org/oclc/terms/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:diag="http://www.loc.gov/zing/srw/diagnostic/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<version>1.1</version>
<numberOfRecords>836</numberOfRecords>
<records/>
<nextRecordPosition/>
<resultSetIdleTime/>
<diagnostics xmlns:srw="http://www.loc.gov/zing/srw/" xmlns:srw8="info:srw/extension/8/spelling" xmlns:srw2="http://www.loc.gov/zing/srw/update/" xmlns:srw3="http://www.loc.gov/zing/srw/diagnostic/" xmlns:srw6="info:srw/extension/6/facetSummary" xmlns:srw7="info:srw/extension/7/componentpostings" xmlns:srw4="http://www.loc.gov/zing/cql/xcql/" xmlns:srw5="info:srw/extension/5/restrictorSummary">
<srw3:diagnostic>
<srw3:uri>info:srw/diagnostic/1/13</srw3:uri>
<srw3:details>1</srw3:details>
<srw3:message> Present request out of range</srw3:message>
</srw3:diagnostic>
</diagnostics>
<echoedSearchRetrieveRequest xmlns:srw="http://www.loc.gov/zing/srw/">
<version>1.1</version>
<query></query>
<maximumRecords></maximumRecords>
<recordPacking>xml</recordPacking>
<startRecord></startRecord>
<sortKeys>relevance</sortKeys>
<wskey></wskey>
<servicelevel>full</servicelevel>
</echoedSearchRetrieveRequest>
</searchRetrieveResponse>
```
<li>You also need to delete all instances of all "records" elements (note: do not delate any "record" elements"). After removing all "records" elements, you should use records as your root element and add it to the beginning and end of your file.</li>
  <li>Once I'm satisfied with the 856s, I run MarcEdit's MarcBreaker (MARC21XML=>MARC) to convert the MARCXML into MARC. (I recommend setting the "Default Character Encoding" to UTF-8).</li>
  <li>Then I use the MARC2KBART plugin to transform the MARC records into a KBART file. The OCNs are are likely to not be carried over, so I recommend using the tab delimited export feature to export the 001 fields. I've also noticed that many dates aren't carried over so I also recommend exporting the 260$c and the 264$c just in case (you may also wish to export additional fields for identification purposes such as 245$a or 856$c).</li>
  <li>Once you've copied over the OCLC Numbers from the second file, eyeball the url field in the KBART. You may want to check the filter for that column in Excel too; you're likely to find that there are urls you missed cleaning up or there are incomplete urls (for example a url just to search.proquest.com and not a url to a specific item). My personal preference is to cut those rows and past them into a seperate file to work on after I upload all the data ready to be uploaded.</li>
  <li>Add the Collection name and Collection id to the correct fields in the KBART file, and you should now be able to upload it to the KB collection</li>
 </ul>
