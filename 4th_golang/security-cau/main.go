package main

import (
	"fmt"
	"net/http"
	"strconv"
	"strings"

	"github.com/PuerkitoBio/goquery"
	"github.com/djimenez/iconv-go"
)

type result struct {
	link  string
	title string
}

func main() {
	c := make(chan []result)
	result := []result{}
	page, err := strconv.Atoi(getPages())
	checkErr(err)
	for i := 0; i < page; i++ {
		go getContents(i+1, c)
	}
	for i := 0; i < page; i++ {
		r := <-c
		result = append(result, r...)
	}
	fmt.Println(result)

}

// pages
func getPages() string {
	resp, err := http.Get("http://security.cau.ac.kr/board.htm?bbsid=notice")
	checkErr(err)
	checkStatusCode(resp)

	doc, err := goquery.NewDocumentFromReader(resp.Body)
	checkErr(err)

	page, _ := doc.Find(".paging>a").Last().Attr("href")

	lastPage := []string{}
	lastPage = strings.Split(page, "page=")
	return lastPage[1]

}

// page contents
func getContents(page int, contentsChan chan []result) {
	url := "http://security.cau.ac.kr/board.htm?bbsid=notice&ctg_cd=&skey=&keyword=&mode=list&page="
	resp, err := http.Get(url + strconv.Itoa(page))
	checkErr(err)
	checkStatusCode(resp)

	doc, err := goquery.NewDocumentFromReader(resp.Body)
	checkErr(err)

	c := make(chan result)

	result := []result{}

	doc.Find(".al").Each(func(i int, contents *goquery.Selection) {
		go inputValue(contents, c)
	})
	for i := 0; i < doc.Find(".al").Length(); i++ {
		r := <-c
		result = append(result, r)
	}
	fmt.Println(page, "Done")
	contentsChan <- result
}

func inputValue(cont *goquery.Selection, c chan<- result) {
	result := result{}
	result.link, _ = cont.Find("a").Attr("href")
	result.title, _ = iconv.ConvertString(cont.Find("a").Text(), "euc-kr", "utf-8")

	c <- result
}

func checkErr(err error) {
	if err != nil {
		fmt.Println(err)
	}
}

func checkStatusCode(resp *http.Response) {
	if resp.StatusCode != 200 {
		fmt.Println("Failed : ", resp.StatusCode)
	}
}
