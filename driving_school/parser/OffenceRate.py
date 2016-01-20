# coding=utf-8
from bs4 import BeautifulSoup

from cruise.src import db


def parse(table, dataTime):
    soup = BeautifulSoup(table)

    count = len(soup.find_all("tr")) + 1
    data = []
    for i in range(4, count):
        td = soup.select("tr:nth-of-type(" + str(i) + ") td")
        schoolName = BeautifulSoup(str(td[0])).get_text().strip()
        if schoolName.find("驾校".decode("utf-8", "ignore")) < 0 : 
            schoolName = schoolName + "驾校".decode("utf-8", "ignore")
        try:
            rate = BeautifulSoup(str(td[1])).get_text().strip()[:-1]
            try:
                float(rate)
            except:
                continue
            data.append("('"+schoolName+"','"+dataTime+"','"+rate+"')")
            print  schoolName + " : " + rate

        except:
            continue

    db.saveOffenceRate(data)

