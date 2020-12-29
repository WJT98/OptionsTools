import requests
from bs4 import BeautifulSoup
import re
from datetime import date, datetime
import os
import errno
import numpy
import pandas as pd
import time

DEBUG = False

def get_cnt():
	r = requests.get("https://www.optionseducation.org/toolsoptionquotes/optionsquotes")
	cnt = re.search("cnt=([A-F0-9]+)", r.text)
	return cnt.group().split("=")[1]

def get_html(ticker, vdate):
	try:
		cnt = get_cnt()
		url = "https://oic.ivolatility.com/oic_adv_options.j?cnt="+cnt+"&ticker="+ticker+"&exp_date=-1"
		print(url)
		exception = True
		while(exception):
			try:
				page = requests.get(url)
				soup = BeautifulSoup(page.content, 'html.parser')
				exception = False
			except requests.exceptions.RequestException as e:
				print(e)
				time.sleep(20)
				exception = True
		if not os.path.isdir("bs4_html"):
			os.makedirs("bs4_html")
		filename = os.path.join(os.getcwd(),"bs4_html/"+ticker+"/"+vdate+".html")
		os.makedirs(os.path.dirname(filename), exist_ok=True)
		with open(filename, "w", encoding='utf-8') as f:
			f.write(str(soup))
	except Exception as err:
		print(err)


def format_date(d):
	d = datetime.strptime(d, '%b %d, %Y')
	return d.strftime('%Y-%m-%d')

#returns dataframe and the associated ticker (needs to be passed on for multiprocessing)
def save_data(ticker, vdate):
	try:
		with open("bs4_html/"+ticker+"/"+vdate+".html", 'r') as f:
			contents = f.read()
			soup = BeautifulSoup(contents, 'lxml')
		table = soup.find_all('table')

		#return a list of dataframes made from the bs4 table query
		df = pd.read_html(str(table), flavor='bs4', header=[1])

		exp_dates = []
		start, end = 0, 0

		for i in range(len(df)):
			headers = ''.join([str(x) for x in list(df[i].columns.values)])
			if exp_dates is not None and re.search("Expiration", headers):
				exp_dates = re.findall("[A-Z][a-z]{2} [0-9]{2}, [0-9]{4}", headers)
				exp_dates = [format_date(d) for d in exp_dates]
			elif re.search("Expiry:", headers):
				if end == 0:
					end = start
				end += 1
				df[i] = df[i][1:]
				df[i].rename(columns=df[i].iloc[0])

			elif re.search("Rho", headers):
				if end == 0:
					end = start
				end +=1
			else:
				start +=1
		#Can store historical volatility from last 2 tables
		# print(df[-3])
		# print(df[-2])
		# print(df[-1])
		pd.set_option("display.max_rows", 10, "display.max_columns", None)
		directory = "csv/" + ticker
		if not os.path.isdir(directory):
			os.makedirs(directory)
		file_path = directory+"/"+vdate+".csv"
		if os.path.exists(file_path):
			os.remove(file_path)
		for i in range(start, end+1):
			df[i]['Implied Vola%'] = df[i]['Implied Vola%'].str.rstrip('%')
			df[i].drop(['Bid/Ask Mean', 'Change (%)'], axis=1, inplace=True)
			df[i]['exp_date'] = exp_dates[i-start]
			df[i]['val_date'] = vdate
			df[i].rename(columns={'Option Symbol': 'option', 'Option Symbol.1':'ticker', 
									'Implied Vola%':'iv', 'Strike':'strike',
									'Bid': 'bid', 'Ask':'ask','Volume':'volume', 
									'Delta':'delta', 'Gamma':'gamma', 'Alpha':'alpha', 
									'Vega':'vega', 'Rho':'rho', 
									'Open Interest':'open_interest'}, inplace=True)
			if i == start:
				df[i].to_csv(file_path, mode='a',index=False, header=True)
				if DEBUG:
					break
			else:
				df[i].to_csv(file_path, mode='a',index=False, header=False)
	except Exception as err:
		raise err


	
def main():
	today = date.today()
	d = today.strftime("%Y-%m-%d")
	filename = os.path.join(os.getcwd(),"SPY"+"/"+d+".html")
	if not os.path.exists(filename):
		get_html("SPY", d)
	save_data("SPY", d)
if __name__ == '__main__':
	main()
