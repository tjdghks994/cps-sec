import requests
from bs4 import BeautifulSoup
import csv

# import 해주기
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtGui, uic

# form_class 정해주기
form_class = uic.loadUiType("indeed.ui")[0]

#QObject 추가
class Scraper(QObject) :
    
    # Signal 발생 시 추가
    updated = pyqtSignal(int)

    def __init__(self, textBrowser) :
        # QObject 클래스 사용
        super().__init__()

        self.url = "https://kr.indeed.com/jobs?q=python&limit=50"
        self.textBrowser = textBrowser

    def getHTML(self, cnt) :
        res = requests.get(self.url + "&start=" + str(cnt * 50))

        if res.status_code != 200 :
            print("request error : ", res.status_code)

        html = res.text

        soup = BeautifulSoup(html, "html.parser")

        return soup
    
    def getPages(self, soup) :
        pages = soup.select(".pagination > a")

        return len(pages)

    def getCards(self, soup, cnt) :
        jobCards = soup.find_all("div", class_ = "jobsearch-SerpJobCard")

        jobID = []
        jobTitle = []
        jobLocation = []

        for j in jobCards :
            jobID.append("http://kr.indeed.com/viewjob?jk=" + j["data-jk"])

            jobTitle.append(j.find("a").text.replace("\n", ""))
            if j.find("div", class_ = "location") != None :
                jobLocation.append(j.find("div", class_ = "location").text)
            elif j.find("span", class_ = "location") != None :
                jobLocation.append(j.find("span", class_ = "location").text)

        self.writeCSV(jobID, jobTitle, jobLocation, cnt)

    def writeCSV(self, jobID, jobTitle, jobLocation, cnt) :
        file = open("indeed.csv", "a", newline="")

        wr = csv.writer(file)

        for i in range(len(jobID)) :
            wr.writerow([str((i + 1) + (cnt * 50)), jobID[i], jobTitle[i], jobLocation[i]])

        file.close()

    def run(self) :
        file = open("indeed.csv", "w", newline="")
        wr = csv.writer(file)
        wr.writerow(["No.", "Link", "Title", "Location"])
        
        file.close()

        soupPage = self.getHTML(0)
        pages = self.getPages(soupPage)

        for i in range(pages) :
            soupCard = self.getHTML(i)
            self.getCards(soupCard, i)

            # 추가 및 변경
            self.textBrowser.append("%d번째 페이지 Done" % (i + 1))
            self.updated.emit(int(((i+1) / pages) * 100))


class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        #Scraper 가져오기
        self.crawler = Scraper(self.textBrowser)

        # Thread를 이용해서 동적으로
        self.thread = QThread()
        self.crawler.moveToThread(self.thread)
        self.thread.start()

        #버튼 클릭 시 무엇으로 연결 할 것인지
        self.pb1.clicked.connect(self.crawler.run)

        #setWindowTitle
        self.setWindowTitle("indeed crawler")

        #progressBar를 위한 시그널 발생할 때 update 변수 추가
        self.crawler.updated.connect(self.progressBarValue)

        #progressBarvalue 초기화
        self.progressBarValue(0)

        
    def progressBarValue(self, value) :
        self.progressBar.setValue(value)

 
if __name__ == '__main__' :

    app = QApplication(sys.argv) 
    myWindow = WindowClass() 
    myWindow.show()
    app.exec_()
