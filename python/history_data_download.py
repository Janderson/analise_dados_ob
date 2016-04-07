#coding: utf8
import requests, io
import pandas as pd
from bs4 import BeautifulSoup

def download(str_date="mar.2015"):
	requests.get("http://www.forexfactory.com/calendar.php?month=%s" % str_date)
	s = str_html.split("<table class=\"arrayCheckbox  requireOneCheck\">")[1]
	print len(str_html)


def load_table(report_name, year):
    with io.open(report_name,'r') as f:
        html_doc = f.read()
	soup = BeautifulSoup(html_doc)
	#print "found:", len(soup.find_all("td"))

	# correct impact of news
	for td in soup.find_all("td"):
		if "class" in td.attrs and td["class"]== ["impact"] and td.span!=None:
			str_imp = td.span["class"][0]
			#print td,
			#print  "->", str_imp
			td.span.replaceWith(str_imp)
	
	#correct date
	for sp in soup.find_all("span"):
		if "class" in sp.attrs and sp["class"]== ["date"]:
			print sp.span
			sp.replaceWith(str(sp.span.get_text()) + " 2015")
	
    with io.open("cor_"+report_name,'w') as f:
       f.write(unicode(soup))

    t = pd.read_html(unicode(soup), index_col=0)
    return t




t = load_table("ffcalendar.html")
t[0].to_csv("calendar.csv",encoding='utf-8')

