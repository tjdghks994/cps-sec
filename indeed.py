import requests
from bs4 import BeautifulSoup
import csv

class scraper :

    def __init__(self) : 
        self.baseURL = ""

    def allPages(self, pages) :
        res = requests.get(self.baseURL + "&start=" + str(pages))

        if res.status_code != 200 :
            print("bad request", res.status_code)

        html = res.text
        soup = BeautifulSoup(html, "html.parser")

        return soup

    def totalPage(self) :
        res = requests.get(self.baseURL)

        if res.status_code != 200 :
            print("bad request", res.status_code)

        html = res.text
        soup = BeautifulSoup(html, "html.parser")

        pages = soup.select(".pagination > a")

        return len(pages)

    def getContent(self, page) :
        soup = self.allPages(page)
        contents = soup.select("div.jobsearch-SerpJobCard")

        cnt = 0
        jobId = []
        title = []

        for c in contents :
            jobId.append("" + c.attrs["data-jk"])
            title.append(c.find("div", class_ = "title").find("a").text.replace("\n", ""))
            cnt += 1

        self.writeCSV(jobId, title)
        
    def writeCSV(self, jobId, title) :
        file = open('indeed.csv','a', newline='')
        wr = csv.writer(file)

        for i in range(len(jobId)) : 
            wr.writerow([str(i), jobId[i], title[i]])
        
        file.close()

    def scrap(self) :
        file = open('indeed.csv','w', newline='')
        wr = csv.writer(file)
        wr.writerow(["No", "Link","title"])
        file.close()

        page = self.totalPage()
        
        for i in range(page) :   
            self.getContent(i * 50)

if __name__ == "__main__":
    scraper = scraper()
    scraper.scrap()
