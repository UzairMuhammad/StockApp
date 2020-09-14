import requests
from bs4 import BeautifulSoup
import pandas as pd

import datetime
import numpy as np
import matplotlib.pyplot as plt


class ScrapeHistorical(object):
    def __init__(self, symbol):
        self.symbol = symbol

        self.stockDates = []
        self.stockOpens = []
        self.stockAdjCloses = []
        self.financeDataFrame = None

        self.temp = []
        self.csv = None

        self.getData()
        self.convertDate()
        self.makeDataFrame()
        self.printFrame()

    def getData(self):
        # Yahoo Finance website
        financeURL = "https://ca.finance.yahoo.com/quote/MFC/history?p=MFC"
        # financeURL = "https://ca.finance.yahoo.com/quote/" + self.symbol + "/history?p=" + self.symbol
        r = requests.get(financeURL)
        financeData = r.text
        soup = BeautifulSoup(financeData, features="html.parser")

        # get data from finance page
        for row in soup.find_all('tr', attrs={"class": "BdT"}):
            index = 0

            if row.text.find("Dividend") == -1:
                for col in row.find_all('td', attrs={"class": "Py(10px)"}):
                    if index == 0:
                        self.stockDates.append(col.text)
                    elif index == 1:
                        self.stockOpens.append(float(col.text))
                    elif index == 5:
                        self.stockAdjCloses.append(float(col.text))

                    index = index + 1

    def makeDataFrame(self):
        # correlate column titles to rows
        a = {
            "Date": self.temp,
            "Open": self.stockOpens,
            "Adj Close": self.stockAdjCloses
        }

        # create data frame
        self.financeDataFrame = pd.DataFrame.from_dict(a, 'index').transpose()

    def printFrame(self):
        # print data frame
        self.financeDataFrame.to_csv(r'historical.csv', index=False)
        self.csv = np.loadtxt(open("historical.csv", "rb"), delimiter=",")

    def convertDate(self):
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

        for i in self.stockDates:
            year = i[len(i)-4:len(i)]
            month = i[:3]
            day = i[len(i)-8:len(i)-6]
            self.temp.append(datetime.datetime(int(year), months.index(month) + 1, int(day)))


'''stockObject = MostActiveScraper()
plt.plot(stockObject.financeDataFrame["Date"], stockObject.financeDataFrame["Open"].values)
plt.yticks(np.arange(min(stockObject.financeDataFrame["Open"].values), max(stockObject.financeDataFrame["Open"].values) + 1.0, 5.0))
plt.yticks(np.arange(0.0, 40.0, 5.0))
plt.gcf().autofmt_xdate()
plt.title('Stocks')
plt.xlabel("Dates")
plt.ylabel("Opening")
plt.show()
'''

