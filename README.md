**Webscraper for a real-estate listings website.**

`scrap-data.py` crawls through all the pages containing search results/property listings, parses the HTML for property data i.e. *rent, sq. ft., date posted, type of property , location, no. of beds & baths, link to the listing and no. of attached images*, and then saves the data in a `.csv` file. 

`format-data.py` filters and categorizes the data.

#### Requirements
* BeautifulSoup
* requests
* pandas
* numpy
