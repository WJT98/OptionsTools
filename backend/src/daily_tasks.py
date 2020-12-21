import psycopg2
import scrape_oic as so
import logging
from datetime import date
import os
from os import isfile, isdir, join, listdir
from multiprocessing import Pool, cpu_count, Lock
from timeit import default_timer as timer
import pandas as pd
import db_config
import db_setup


def init_child(lock):
	global lock
	global conn
	conn = db_setup.db_connection()
	lock = lock
	

def insert_csv(csv, ticker, conn):
	try:
		f = open(csv, 'r')
		cursor = conn.cursor()
		cursor.copy_from(f, 'data_set', sep=',', columns= ['id', 'underlying_id'])
		f.close()
		cursor.close()
	except Exception as err:
		raise err

def get_csv_list(ticker, vdate):
	try:
		path = "csv/" + ticker
		directories = [d for d in listdir(path) if isdir(join(path, d))]
		all_files = []
		for d in directories:
			files = [f for f in listdir(d) if isfile(join(d,f))]
			all_files +=files
	except Exception as err:
		raise err
	return all_files

def mproc_job(ticker, vdate):
	try:
		conn = db_setup.db_connection()
		with lock:
			logging.info("DB connection established")
		df = so.get_data(ticker, vdate)
		with lock:
			logging.info(ticker+": EOD options data scraped into list of dataframes")
		df = so.process_df(df, ticker)
		logging.info(ticker+": dataframes processed")

		cursor = conn.cursor()
		csv_files = get_csv_list(ticker, vdate)
		for csv in csv_files:
			insert_csv(csv, ticker, conn)
		with lock:
			logging.info(ticker+": inserted into db + committed")
		conn.commit()
	except Exception as err:
		conn = None
		with lock:
			logging.error(db_setup.print_psycopg2_exception(err))
			logging.error(err)
		conn.rollback()
		raise err
	finally:
		if (conn):
			cursor.close()
			conn.close()





def main():
	if not os.path.isdir("logs"):
		os.makedirs("logs")
	logging.basicConfig(level=logging.DEBUG, 
						format= '[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
     					datefmt='%Y-%m-%d %H:%M:%S',
						handlers=[
							logging.FileHandler('logs/'+date.today().strftime("%Y-%m-%d") + '.log'),
							logging.StreamHandler()])	


	conn = db_setup.db_connection()
	cur = conn.cursor()
	try:
		cur.execute("""SELECT ticker, exchange FROM TICKERS""")
	except Exception as err:
		logging.error("SQL SELECT FAILED")
	tickers = cur.fetchall()


	vdate = date.today().strftime("%Y-%m-%d")
	
	print(f'starting computations on {cpu_count()} cores')
	start = timer()
	

	pool_size = cpu_count()
	lock = Lock()

	with Pool(pool_size, initializer=init_child,initargs=(lock)) as pool:
		try:
			args = [(t,vdate) for t in tickers]
			pool.starmap(mproc_job, args)
		except Exception as err:
			logging.error(err)
			return

		end = timer()
		print(f'elapsed time: {end - start}')
		
main()







