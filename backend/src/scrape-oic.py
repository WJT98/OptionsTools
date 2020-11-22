import requests
from bs4 import BeautifulSoup
import re
from datetime import date
import os
import errno
import numpy
import pandas as pd


ticker = "SPY"
def get_cnt():
	r = requests.get("https://www.optionseducation.org/toolsoptionquotes/optionsquotes")
	cnt = re.search("cnt=([A-F0-9]+)", r.text)
	return cnt.group().split("=")[1]

def get_html(ticker, date):
	cnt = get_cnt()
	url = "https://oic.ivolatility.com/oic_adv_options.j?cnt="+cnt+"&ticker="+ticker+"&exp_date=1"
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	filename = os.path.join(os.getcwd(),ticker+"/"+date+".html")
	os.makedirs(os.path.dirname(filename), exist_ok=True)
	with open(filename, "w", encoding='utf-8') as f:
		f.write(str(soup))

def store_data(ticker, date):
	with open(ticker+"/"+date+".html", 'r') as f:
		contents = f.read()
		soup = BeautifulSoup(contents, 'lxml')
	table = soup.find_all('table')[11]
	return pd.read_html(str(table), flavor='bs4', header=[0])[0]
	# with open("RAWHTML.html", "w", encoding='utf-8') as f:
	# 	f.write(str(table))
	# 	pd.set_option("display.max_rows", None, "display.max_columns", None)
	# 	f.write(str(df))

	
def main():
	today = date.today()
	d = today.strftime("%Y-%m-%d")
	filename = os.path.join(os.getcwd(),ticker+"/"+d+".html")
	if not os.path.exists(filename):
		get_html("SPY", d)
	df = store_data("SPY", d)

main()