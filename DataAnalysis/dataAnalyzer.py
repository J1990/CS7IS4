from os import path
from os import listdir
from os.path import isfile, join
import json
import datetime as dt
import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
import pytz

def nearest(items, pivot):
    return min(items, key=lambda x: abs(x - pivot))

def nearest_ind(items, pivot):
    time_diff = np.abs([date - pivot for date in items])
    return time_diff.argmin(0)

basePath = path.dirname(__file__)
jsonFilesPath = path.join(basePath, 'releases2')
stockPricesPath = path.join(basePath, 'stockPrices.csv')
#graphForCompany = "PEP"

oneCompanyIncreaseCount = 0
oneCompanyDecreaseCount = 0
allCompanyIncreaseCount = 0
allCompanyDecreaseCount = 0

positivePressContent = ''
negativePressContent = ''

positiveFile = open("D:\\OneDrive - TCDUD.onmicrosoft.com\\MSc\\Sem 2\\TextAnalytics\\positive.txt","a", encoding="utf-8")#append mode 
negativeFile = open("D:\\OneDrive - TCDUD.onmicrosoft.com\\MSc\\Sem 2\\TextAnalytics\\negative.txt","a", encoding="utf-8")#append mode
 

pressPublishDates = dict()
pressPublishContent = dict()

for file in listdir(jsonFilesPath):

    filePath = join(jsonFilesPath, file)

    if isfile(filePath):
        companyCode = file.split("_")[0]

        with open(filePath, encoding="utf8") as jsonFile:
            data = json.load(jsonFile)

            for js in data:
                dateStr = js['date']
                content = js['content'].strip().replace(' ', ',').replace('#', ',')

                if(companyCode not in pressPublishDates):
                    pressPublishDates[companyCode] = dateStr
                    pressPublishContent[companyCode] = content
                else:
                    pressPublishDates[companyCode] = pressPublishDates[companyCode]+ "#" + dateStr
                    pressPublishContent[companyCode] = pressPublishContent[companyCode]+ "#" + content

for comp in pressPublishDates:

    if(comp!="PEP"):
        continue

    stockPrices = pd.read_csv(stockPricesPath)

    oneCompanyPricesData = pd.DataFrame(stockPrices[stockPrices["company"]==comp])

    oneCompanyPricesData.date = pd.to_datetime(oneCompanyPricesData['date'], format='%Y-%m-%d %H:%M:%S')
    oneCompanyPricesData.openprice = pd.to_numeric(oneCompanyPricesData['openprice'])
    oneCompanyPricesData.closeprice = pd.to_numeric(oneCompanyPricesData['closeprice'])
    oneCompanyPricesData = oneCompanyPricesData.sort_values('date', ascending=True)

    oneCompanyPressDateTexts = pressPublishDates[comp].split("#")
    oneCompanyPressContent = pressPublishContent[comp].split("#")
    pressDates = pd.DataFrame(columns = ["date", "value"])

    index = 0
    
    for dateStr in oneCompanyPressDateTexts:

        date = dt.datetime.today()
        eastern = pytz.timezone('US/Eastern')

        if(dateStr[-3:]=="EST"):        
            date = dt.datetime.strptime(dateStr, "%b %d, %Y %H:%M%p EST")
            date = date.replace(hour=0, minute=0, second=0, microsecond=0)
        elif(dateStr[-3:]=="EDT"):
            date = dt.datetime.strptime(dateStr, "%b %d, %Y %H:%M%p EDT")
            date = date.replace(hour=0, minute=0, second=0, microsecond=0)

        nearestInd = nearest_ind(oneCompanyPricesData.date, date)
        openVal = oneCompanyPricesData.iloc[nearestInd]['openprice']
        closeVal = oneCompanyPricesData.iloc[nearestInd]['closeprice']

        if(closeVal>openVal):
            allCompanyIncreaseCount+=1
            positiveFile.write(oneCompanyPressContent[index])
        else:
            allCompanyDecreaseCount+=1 
            negativeFile.write(oneCompanyPressContent[index])

        val = max({openVal, closeVal})

        new_row = {"date":date, "value":val}
        pressDates = pressDates.append(new_row, ignore_index=True)

        index+=1

    pressDates.sort_values('date', ascending=True)

    maxPrice = max({oneCompanyPricesData['openprice'].astype(float).max(),oneCompanyPricesData['closeprice'].astype(float).max()})

    
    plt.figure(figsize=(35.0, 6.0))
    plt.yticks(np.arange(0.0, maxPrice, step=(maxPrice/10)))
    plt.plot('date','openprice', data=oneCompanyPricesData, marker='o', markersize=3, label="Open Price $")
    plt.plot('date','closeprice', data=oneCompanyPricesData, marker='o', markersize=3, label="Close Price $")
    plt.vlines(pressDates['date'], 0, pressDates['value'], linestyle="dotted")
    plt.scatter(pressDates['date'], pressDates['value'], s=50, c='r', label="Press Release Date", zorder = 2)
    plt.ylim(ymin=0)
    plt.legend(loc="upper right")
    plt.title("Price Chart for " + comp)
    plt.xlabel("Date")
    plt.ylabel("Stock Price $")
    plt.show()
    
print(len(pressPublishDates))
labels = 'Rise: ' + str(allCompanyIncreaseCount), 'Dip: ' + str(allCompanyDecreaseCount),
sizes = [allCompanyIncreaseCount, allCompanyDecreaseCount]
fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.show()

positiveFile.close()
negativeFile.close()

#plt.savefig(path.join(basePath, graphForCompany+".jpg"), quality=70, dpi=500)