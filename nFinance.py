import requests
from bs4 import BeautifulSoup

class naverScraper() :
    
    def __init__(self) :
        self.url = ""

    def getHTML(self) :
        res = requests.get(self.url)
        if res.status_code != 200 :
            print("err", res.status_code)

        soup = BeautifulSoup(res.text, "html.parser")

        return soup

    def getContent(self, soup) :
        table = soup.select(".box_type_l")

        for t in table :
            tr = t.find_all("tr")

        name = []
        val = []
        for td in tr :
            if td.find("a") != None :
                name.append(td.find("a").text)
                for num in td.find_all("td", class_ = "number") :
                    if num != None :
                        val.append(num.text.replace("\n", "").replace("\t", ""))
        
        return name, val

    def divide_list(self, l, n): 
        for i in range(0, len(l), n): 
            yield l[i:i + n] 

    def scrap(self) :
        cnt = 10

        soup = self.getHTML()
        name, val = self.getContent(soup)

        result = list(self.divide_list(val, cnt))

        for i in range(len(result)) :
            result[i].insert(0, name[i])

        for j in range(len(result)) :
            print(result[j])

if __name__ == "__main__":
    s = naverScraper()
    s.scrap()