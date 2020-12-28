import psycopg2
import logging
from datetime import date
import os
from multiprocessing import Pool, cpu_count, Lock
from timeit import default_timer as timer
import pandas as pd
import db_config
import db_setup
import csv
from psycopg2 import OperationalError, errorcodes, errors
import traceback
import sys
import time
import scrape_oic as so

DEBUG = False


def init_child(lock_):
	global lock
	global conn
	conn = db_setup.get_conn()
	lock = lock_


def update_options_chain(conn):
	try:
		cur = conn.cursor()
		q = '''INSERT INTO options_chain (underlying_id, exp_date, strike, option) 
				SELECT DISTINCT t.id, im.exp_date, 
					im.strike, im.option
				FROM tickers AS t, imports AS im
				WHERE im.ticker = t.ticker 
					AND NOT EXISTS (SELECT * 
									FROM options_chain AS oc, imports AS im
									WHERE t.ticker = im.ticker
										AND oc.underlying_id = t.id 
										AND oc.exp_date = im.exp_date
										AND oc.strike = im.strike
										AND oc.option = im.option);'''
		cur.execute(q)
		conn.commit()
	except Exception as err:
		raise err
	finally:
		if cur: 
			cur.close()

def update_options_metrics(conn):
	try:
		cur = conn.cursor()
		q = '''INSERT INTO options_metrics (option_id, val_date, bid, ask,
					volume, open_interest, iv, delta, gamma, theta, alpha,
					 vega, rho) 
				SELECT oc.id, im.val_date, im.bid, im.ask, im.volume, 
					im.open_interest, im.iv, im.delta, im.gamma, im.theta,
					im.alpha, im.vega, im.rho
				FROM options_chain AS oc, imports AS im, tickers AS t
				WHERE t.id = oc.underlying_id
					AND im.exp_date = oc.exp_date
					AND im.strike = oc.strike
					AND im.option = oc.option
					AND im.ticker = t.ticker
					AND NOT EXISTS (SELECT * 
									FROM options_metrics AS om, 
										options_chain AS oc, imports AS im, tickers AS t
									WHERE t.id = oc.underlying_id
										AND om.option_id = oc.id
										AND om.val_date = im.val_date
										AND im.exp_date = oc.exp_date);'''
		cur.execute(q)
		conn.commit()
	except Exception as err:
		raise err
	finally:
		if cur: 
			cur.close()
		

def truncate_imports(conn):
	try:
		cur = conn.cursor()
		cur.execute('TRUNCATE TABLE imports;')
		cur.close()
	except Exception as err:
		raise err

def import_table(csv_file, ticker, cur):
	try:
		headers = ['strike', 'option', 'ticker', 'bid', 'ask', 'volume', 
		'open_interest', 'iv', 'delta', 'gamma', 'Theta', 'alpha', 'vega', 
		'rho', 'exp_date', 'val_date']
		with open(csv_file, 'r') as f: 
			next(f)
			cur.copy_from(f, 'imports', columns=headers,sep=',')
	except Exception as err:
		raise err

def get_csv_list(ticker, vdate):
	try:
		path = "csv/" + ticker
		#directories = [path+'/'+d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
		all_files = []
		#for d in directories:
		files = [path+"/"+f for f in os.listdir(path) 
					if (os.path.isfile(os.path.join(path,f)) and f == vdate+'.csv')]
		all_files +=files
	except Exception as err:
		raise err
	return all_files

def mproc_job(ticker, vdate):
	try:
		conn = None
		conn = db_setup.get_conn()
		#with lock:
		logging.info("DB connection established")
		so.save_data(ticker, vdate)
		#with lock:
		logging.info(ticker+": EOD options data saved into csv's")

		cursor = conn.cursor()
		csv_files = get_csv_list(ticker, vdate)
		logging.info("Csv's gathered")
		for csv in csv_files:
			import_table(csv, ticker, cursor)
			logging.info(csv + " inserted")
		#with lock:
		logging.info(ticker+": inserted into db + committed")
		conn.commit()
		
	except Exception as err:
		if conn is not None:
			conn.rollback()
		cursor = None
		raise err
	finally:
		if conn:
			conn.close()
		print(ticker, " ended")

def scrape_htmls(tickers,vdate):
	for ticker in tickers:
		filename = os.path.join(os.getcwd(),"bs4_html/"+ticker[0]+"/"+vdate+".html")
		if not os.path.exists(filename):
			so.get_html(ticker[0], vdate)
			time.sleep(30)
	


def main():
	if not os.path.isdir("logs"):
		os.makedirs("logs")
	logging.basicConfig(level=logging.DEBUG, 
						format= '[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
     					datefmt='%Y-%m-%d %H:%M:%S',
						handlers=[
							logging.FileHandler('logs/'+date.today().strftime("%Y-%m-%d") + '.log'),
							logging.StreamHandler()])	

	try:
		#cur.execute("""SELECT ticker, exchange FROM TICKERS""")
		conn = db_setup.get_conn()
		cur = conn.cursor()
		cur.execute("""SELECT ticker FROM TICKERS""")
		tickers = cur.fetchall()
		truncate_imports(conn)
		cur.close()
		conn.close()
		if DEBUG:
			tickers = [("TSLA",)]
		vdate = date.today().strftime("%Y-%m-%d")
		pool_size = 5
		lock = Lock()
		start = timer()
		

		#pool_size = cpu_count()
		scrape_htmls(tickers, vdate)
		print(f'starting computations on {pool_size} cores')
		with Pool(pool_size, initializer=init_child,initargs=(lock,)) as pool:
			args = [(t[0],vdate) for t in tickers]
			pool.starmap(mproc_job, args)
		
		conn = db_setup.get_conn()
		cur = conn.cursor()
		update_options_chain(conn)
		update_options_metrics(conn)
		end = timer()
		print(f'elapsed time: {end - start}')
	except Exception as err:
		#logging.error(db_setup.print_psycopg2_exception(err))
		exc_info = sys.exc_info()
		logging.error(err, traceback.print_exception(*exc_info))
		sys.exit()
	finally:
		if conn:
			conn.close()
			
if __name__ == '__main__':
	main()





