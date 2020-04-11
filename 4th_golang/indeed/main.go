package main

import (
	"encoding/csv"
	"fmt"
	"log"
	"net/http"
	"os"
	"strconv"
	"strings"

	"github.com/PuerkitoBio/goquery"
)

var indeed string = "https://kr.indeed.com/jobs?q=python&limit=50"

type jobs struct {
	id       string
	title    string
	location string
	salary   string
}

func main() {
	var j []jobs
	jc := make(chan []jobs)

	totalPage := getPagesCnt(indeed)

	for i := 0; i < totalPage; i++ {
		go getContent(i, jc)
	}
	for i := 0; i < totalPage; i++ {
		temp := <-jc
		j = append(j, temp...)
	}

	writeCSV(j)
}

func getContent(cnt int, jc chan<- []jobs) {
	c := make(chan jobs)

	pageURL := indeed + "&start=" + strconv.Itoa(cnt*50)
	resp, err := http.Get(pageURL)
	checkErr(err)
	checkCode(resp)

	fmt.Println(pageURL)

	doc, err := goquery.NewDocumentFromReader(resp.Body)
	checkErr(err)

	var jobs []jobs
	doc.Find(".jobsearch-SerpJobCard").Each(func(i int, s *goquery.Selection) {
		go jobsStruct(s, c)
	})

	for i := 0; i < doc.Find(".jobsearch-SerpJobCard").Length(); i++ {
		job := <-c
		jobs = append(jobs, job)
	}
	jc <- jobs
}

func jobsStruct(s *goquery.Selection, c chan<- jobs) {
	id, _ := s.Attr("data-jk")
	title := cleanStr(s.Find(".title>a").Text())
	location := cleanStr(s.Find(".location").Text())
	salary := cleanStr(s.Find(".salarySnippet").Text())
	c <- jobs{
		id:       id,
		title:    title,
		location: location,
		salary:   salary,
	}
}

func writeCSV(j []jobs) {
	file, err := os.Create("jobs.csv")
	checkErr(err)

	w := csv.NewWriter(file)
	defer w.Flush()

	header := []string{"Link", "Title", "Location", "Salary"}
	wErr := w.Write(header)
	checkErr(wErr)

	for _, job := range j {
		jobString := []string{"https://kr.indeed.com/viewjob?jk=" + job.id, job.title, job.location, job.salary}
		jwErr := w.Write(jobString)
		checkErr(jwErr)
	}
}

func getPagesCnt(url string) int {
	resp, err := http.Get(url)
	checkErr(err)
	checkCode(resp)
	defer resp.Body.Close()

	doc, err := goquery.NewDocumentFromReader(resp.Body)
	checkErr(err)

	pages := 0
	doc.Find(".pagination").Each(func(i int, s *goquery.Selection) {
		pages = s.Find("a").Length()
	})

	return pages
}

func cleanStr(str string) string {
	return strings.Join(strings.Fields(strings.TrimSpace(str)), " ")
}

func checkErr(err error) {
	if err != nil {
		fmt.Println(err)
	}
}

func checkCode(resp *http.Response) {
	if resp.StatusCode != 200 {
		log.Fatalf("staus code error : %d, %s", resp.StatusCode, resp.Status)
	}
}
