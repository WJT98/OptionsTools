import requests
from bs4 import BeautifulSoup
import re
from datetime import date
import os
import errno
import numpy
import pandas as pd


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
def process_df(df, ticker):
	#with open("RAWHTML2.html", "w", encoding='utf-8') as f:
	exp_dates = []
	start, end = 0,0
	for i in range(len(df)):
		#print(df[i].columns)
		#print(list(df[i].columns.values))
		headers = ''.join([str(x) for x in list(df[i].columns.values)])
		if exp_dates is not None and re.search("Expiration", headers):
			exp_dates = re.findall("[A-Z][a-z]{2} [0-9]{2}, [0-9]{4}", headers)
			print(exp_dates)
		elif re.search("Expiry:", headers):
			if end == 0:
				end = start
			end += 1
			new_header = df[i].iloc[0]
			df[i] = df[i][1:]
			df[i].columns = new_header
			df[i].rename(columns=df[i].iloc[0])
		elif re.search("Rho", headers):
			if end == 0:
				end = start
			end +=1
		else:
			start +=1
	df_processed = df[start:end+1]
	# for i in range(len(processed_df)):
	# 	print(processed_df[i].head())
	print(df[-3])
	print(df[-2])
	print(df[-1])
	print(len(exp_dates), len(df_processed))
	return df_processed, exp_dates, ticker


#returns dataframe and the associated ticker (needs to be passed on for multiprocessing)
def get_data(ticker, date):
	filename = os.path.join(os.getcwd(),"bs4_html/"+ticker+"/"+date+".html")
	if not os.path.exists(filename):
		get_html(ticker, date)
	with open("bs4_html/"+ticker+"/"+date+".html", 'r') as f:
		contents = f.read()
		soup = BeautifulSoup(contents, 'lxml')
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
	return df, ticker


	
def main():
	today = date.today()
	d = today.strftime("%Y-%m-%d")
	filename = os.path.join(os.getcwd(),"SPY"+"/"+d+".html")
	if not os.path.exists(filename):
		get_html("SPY", d)
	df = get_data("SPY", d)
	df_tuple = process_df(df)

main()
