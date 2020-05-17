import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys
import numpy as np
import math

headers = requests.utils.default_headers()
headers.update({ 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'})

baseURL = "https://www.prop.pk/islamabad/flats-apartments-to-rent-in-e-11-329/"
filterURL = "/"

l = []
x = 0
resultsScraped = 0

while True:
    x = x + 1
    url = baseURL + str(x) + filterURL

    mainRequest = requests.get(url, headers)
    print("\nCrawling: " + url + "\tResponse: " + str(mainRequest.status_code))

    if mainRequest.status_code != 200:
        print("\nFinished crawling.")
        break
    else:
        mainPage = BeautifulSoup(mainRequest.content, "html.parser")

        results = mainPage.find("div", {"class":"search-result"}).find("span").text.replace("\n","").lstrip().rstrip()
        print(results)
        
        totalResults = mainPage.find("h1", {"class":"title"}).find("span").text

        allCards = mainPage.find_all("li", {"class": "prop-card"})
        
        for item in allCards:
            dict = {}

            try:
                dict["Posted"] = item.find("div",{"class":"potedt-date"}).text.replace("Added ","").replace(" ago","")
            except:
                pass
            try:
                dict["Price"] = item.find("span",{"class":"price-range"}).text
            except:
                pass

            try:
                dict["Pictures"] = item.find("div",{"class":"prop-img"}).find("li").text.replace(" ","").replace("\n","")
            except:
                pass

            try:
                dict["Type"] = item.find("li",{"class":"portion"}).text
            except:
                pass

            try:
                dict["Location"] = item.find("li",{"class":"location"}).text
            except:
                pass

            propMeta = item.find("ul", {"class": "prop-meta"})

            try:
                dict["Sq. Ft."] = propMeta.find("li",{"class":"area"}).find("span",{"class":"count"}).text.replace("\n","")
            except:
                pass

            try:
                dict["Beds"] = propMeta.find("li",{"class":"bed"}).find("span",{"class":"count"}).text.replace("\n","")
            except:
                pass

            for i in range(0,3,1):
                    try:
                        text = propMeta.find_all("li")[i].text
                        if "Bath" in text:
                            dict["Baths"] = propMeta.find_all("li")[i].find("span",{"class":"count"}).text.replace("\n","")
                    except:
                        pass

            dict["Link"] = item.find('a').get('href')

            l.append(dict)

df = pd.DataFrame(l)

df.to_csv("Apartment-Listings.csv")