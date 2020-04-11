package main

import (
	"fmt"
	"net/http"
	"strings"

	"github.com/PuerkitoBio/goquery"
	"github.com/djimenez/iconv-go"
)

var naverURL string = "https://finance.naver.com/sise/lastsearch2.nhn"

func main() {
	// url 을 읽어옴
	// url 내의 html 데이터를 읽음
	// 읽은 html 데이터를 저장할 구조체 생성
	// 데이터 출력

	scraper(naverURL)

}

func scraper(url string) {
	resp, err := http.Get(url)
	checkErr(err)
	checkStaus(resp)

	defer resp.Body.Close()

	doc, err := goquery.NewDocumentFromReader(resp.Body)
	checkErr(err)

	searchBox := doc.Find(".box_type_l")
	searchName := searchBox.Find("tr")
	searchName.Each(func(i int, s *goquery.Selection) {
		if s.Find("a").Text() != "" {
			title := s.Find("a").Text()
			convTitle, _ := iconv.ConvertString(title, "euc-kr", "utf-8")
			num := strings.Fields(strings.TrimSpace(s.Find(".number").Text()))
			fmt.Println(convTitle, num)
		}
	})

}

func checkErr(err error) {
	if err != nil {
		fmt.Println(err)
	}
}

func checkStaus(res *http.Response) {
	if res.StatusCode != 200 {
		fmt.Printf("staus code error : %d, %s", res.StatusCode, res.Status)
	}
}
