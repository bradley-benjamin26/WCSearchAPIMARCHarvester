# WCSearchAPIMARCHarvester
<h2>Introduction to ProQuest Dissertations and Theses Harvester</h2>
The WCSearchAPIMARCHarvester is a little Python script that uses the <a href= "http://docs.python-requests.org/en/master/">Requests library</a> with the <a href="https://www.oclc.org/developer/develop/web-services/worldcat-search-api.en.html">OCLC WorldCat Search API</a> to query OCLC master records and download matching records. For folks like me at libraries using WorldCat Discovery, you can then transform these records into a KBART file, upload it to collection manager to create a new KB collection or enhance the metadata of an existing collection.

<h2>Using the Harvester</h2>
<h3>Getting set up</h3>
After downloading the script:
<ol>
  <li>You'll need to <a href="https://platform.worldcat.org/wskey/">request a wskey from OCLC</a>, if you haven't already.</li>
  <li>Install Python, if you haven't already.</li>
  <li>Install the Requests library</li>
<ol>

<h3>Running the Harvester</h3>
<ul>
  <li>I recommend sticking the script in its own folder.</li>
  <li>You can now open your terminal/shell to navigate to the folder and run the script</li>
  <li>Input the necessary data: your the year you're searching, your wskey, and the url you're searching for (note that the script searches
