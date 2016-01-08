# encoding=utf-8
import urllib2
import urllib
import re
from bs4 import BeautifulSoup


from parser import *

class Crawl:

    def __init__(self):
        self.host = "http://www.cdcgs.cn"
        self.url = self.host + '/WebService/Jgxx/JgxxList.aspx?xxlx=13'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 Safari/537.36',
            'Accept': 'text/html;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'utf-8,gbk;q=0.7,*;q=0.3',
            'Connection': 'close',
            'Referer': self.url}


    def getListPage(self):
        req = urllib2.Request(self.url, headers=self.headers)
        content = urllib2.urlopen(req).read()

        pattern = re.compile(r'<a .* href="(.*)">.*(\d{4})年(\d{1,2})月全市(机动车)?驾驶人培训机构.*</a>')
        matches = pattern.findall(content)

        #link = "/Html/News/20140613/content_13_1100003077.html"

        for i in range(0, len(matches)):
            print matches[i]
            link = matches[i][0]
            year = matches[i][1]
            month = str("{:0>2d}".format(int(matches[i][2])))
            self.getDetailPage(link, year+"-"+month);


    def getDetailPage(self, url, dataTime):
        req = urllib2.Request(self.host + url, headers=self.headers)
        content = urllib2.urlopen(req).read()
        pattern = re.compile(r'<table .*>[\w|\W]+?</table>')
        matches = pattern.findall(content)

        for table in matches :
            soup = BeautifulSoup(table)
            tbodyStr = soup.find("tbody").get_text().strip()
            if tbodyStr.find("驾校名称".decode("utf-8", "ignore")) > 0 and tbodyStr.find("违法率".decode("utf-8", "ignore")) > 0 :
                OffenceRate.parse(table, dataTime) 

