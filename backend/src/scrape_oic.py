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
	url = "https://oic.ivolatility.com/oic_adv_options.j?cnt="+cnt+"&ticker="+ticker+"&exp_date=-1"
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	if not os.path.isdir("bs4_html"):
		os.makedirs("bs4_html")
	filename = os.path.join(os.getcwd(),"bs4_html/"+ticker+"/"+date+".html")
	os.makedirs(os.path.dirname(filename), exist_ok=True)
	with open(filename, "w", encoding='utf-8') as f:
		f.write(str(soup))


#returns a tuple (df containing all options data, list of expiry dates)
def process_df(df):
	#with open("RAWHTML2.html", "w", encoding='utf-8') as f:
	for i in range(len(df)):
		#print(df[i].columns)
		print(list(df[i].columns.values))
		headers = ''.join([str(x) for x in list(df[i].columns.values)])
		if re.search("Expiration", headers):
			exp_dates = re.findall("^[A-Z][a-z]{2} [0-9]{2}, [0-9]{4}", headers)
			print(exp_dates)
		#f.write(str(df[i].head()))
	processed_df=[]
	return processed_df, exp_dates



def get_data(ticker, date):

	filename = os.path.join(os.getcwd(),"bs4_html/"+ticker+"/"+date+".html")
	if not os.path.exists(filename):
		get_html(ticker, date)
	with open("bs4_html/"+ticker+"/"+date+".html", 'r') as f:
		contents = f.read()
		soup = BeautifulSoup(contents, 'lxml')
	#table = soup.find_all('table')[10:-1]

	table = soup.find_all('table')
	#return a list of dataframes
	df = pd.read_html(str(table), flavor='bs4', header=[1])
	#with open("RAWHTML2.html", "w", encoding='utf-8') as f:
		#f.write(str(table))
		#pd.set_option("display.max_rows", None, "display.max_columns", None)
		#f.write(str(pd.read_html(str(table), flavor='bs4', header=[0])))
		#for i in range(len(df)):
			#print(df[i].columns)
		#	f.write(str(df[i].head()))
	return df


	
def main():
	today = date.today()
	d = today.strftime("%Y-%m-%d")
	filename = os.path.join(os.getcwd(),"SPY"+"/"+d+".html")
	if not os.path.exists(filename):
		get_html("SPY", d)
	df = get_data("SPY", d)
	df_tuple = process_df(df)

main()
