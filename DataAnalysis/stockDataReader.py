import csv
from os import path
import pandas as pd
import datetime as dt

csvFilePath = path.join(path.dirname(__file__), 'stockDataRaw.csv')
outputPath = path.join(path.dirname(__file__), 'stockPrices.csv')

with open(csvFilePath) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    
    currentCompany = ""
    column_names = ["company", "date", "openprice", "closeprice"]
    df = pd.DataFrame(columns = column_names)

    for row in csv_reader:
        if row[0]=="":
            continue
        elif row[0]=="Date":
            continue
        elif row[1]=="":
            currentCompany = row[0]
        else:

            format = ""

            if(row[0].find("-")!=-1):
                format = "%m-%d-%Y"
            elif(row[0].find("/")!=-1):
                format = "%m/%d/%Y"

            date = dt.datetime.strptime(row[0], format)

            new_row = {"company":currentCompany, "date":str(date), "openprice":row[3].replace("$","").replace(",","").strip(), "closeprice":row[1].replace("$","").replace(",","").strip()}
            df = df.append(new_row, ignore_index=True)

df.to_csv(outputPath, index=False)