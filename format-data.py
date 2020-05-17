import pandas as pd
import numpy as np
import math

data = pd.read_csv('Apartment-Listings.csv', index_col=0) 
data = data.dropna()

def cleanDataFrame(targetColumn, targetString, replacement=None):
    global data
    indexes = data[data[targetColumn].str.contains(targetString)].index
    if replacement != None:
        for a in indexes: 
            data.loc[a, targetColumn] = data.loc[a, targetColumn].replace(targetString, replacement)
    else:
        data = data.drop(indexes)

def categorizeNumericData(noOfCategories, targetColumn, columnName):
    data[targetColumn] = pd.to_numeric(data[targetColumn], errors='coerce', downcast='float')

    minAndMax = data[targetColumn].describe().loc[['min','max']].tolist()
    
    categoriesCutoffs = []
    for i in range(0, noOfCategories+1):
        categoriesCutoffs.insert(i, minAndMax[0]-1 + (minAndMax[1]/noOfCategories)*i)

    categoriesLabels = []
    categoriesCutoffsRounded = [math.floor(n+1)  for n in categoriesCutoffs] 
    for i in range(noOfCategories):
        categoriesLabels.insert(i, str(categoriesCutoffsRounded[i])+'-'+str(categoriesCutoffsRounded[i+1]))

    sqftCategories = pd.cut(data[targetColumn], bins = categoriesCutoffs, labels = categoriesLabels)
    data.insert(len(data.columns), columnName, sqftCategories, True)

    return categoriesLabels

cleanDataFrame('Price', 'Lakh', None)
cleanDataFrame('Price', ' Thousand', '')
cleanDataFrame('Location', ', Islamabad', '')
cleanDataFrame('Sq. Ft.', ',', '')

sizes = categorizeNumericData(4, 'Sq. Ft.', 'Size')
rents = categorizeNumericData(8, 'Price', 'Rent')

data.to_csv("Apartment-Listings-Formatted.csv")