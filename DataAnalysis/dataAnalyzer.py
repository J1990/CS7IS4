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
graphForCompany = "AAL"

pressPublishDates = dict()

for file in listdir(jsonFilesPath):

    filePath = join(jsonFilesPath, file)

    if isfile(filePath):
        companyCode = file.split("_")[0]

        with open(filePath, encoding="utf8") as jsonFile:
            data = json.load(jsonFile)

            for js in data:
                dateStr = js['date']

                if(companyCode not in pressPublishDates):
                    pressPublishDates[companyCode] = dateStr
                else:
                    pressPublishDates[companyCode] = pressPublishDates[companyCode]+ "#" + dateStr

stockPrices = pd.read_csv(stockPricesPath)


oneCompanyPricesData = pd.DataFrame(stockPrices[stockPrices["company"]==graphForCompany])

oneCompanyPricesData.date = pd.to_datetime(oneCompanyPricesData['date'], format='%Y-%m-%d %H:%M:%S')
oneCompanyPricesData.openprice = pd.to_numeric(oneCompanyPricesData['openprice'])
oneCompanyPricesData.closeprice = pd.to_numeric(oneCompanyPricesData['closeprice'])
oneCompanyPricesData = oneCompanyPricesData.sort_values('date', ascending=True)

oneCompanyPressDateTexts = pressPublishDates[graphForCompany].split("#")
pressDates = pd.DataFrame(columns = ["date", "value"])

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
    val = oneCompanyPricesData.iloc[nearestInd]['openprice']
    val = max({val, oneCompanyPricesData.iloc[nearestInd]['closeprice']})

    new_row = {"date":date, "value":val}
    pressDates = pressDates.append(new_row, ignore_index=True)

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
plt.title("Price Chart for " + graphForCompany)
plt.xlabel("Date")
plt.ylabel("Stock Price $")
plt.show()

#plt.savefig(path.join(basePath, graphForCompany+".jpg"), quality=70, dpi=500)