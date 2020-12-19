import psycopg2
import scrape_oic as so
import logging
from datetime import date
import os
from multiprocessing import Pool, cpu_count, Lock
from timeit import default_timer as timer
import pandas as pd
import db_config
import db_setup

mutex = Lock()

def insert_df(df, tablename, conn):
	
	return None



def mproc_job(ticker, vdate):
	try:
		conn = db_setup.db_connection()
		logging.info("DB connection established")
		df = so.get_data(ticker, vdate)

		logging.info(ticker+": EOD options data scraped into list of dataframes")
		df = so.process_df(df)
		logging.info(ticker+": dataframes processed")

		cursor = conn.cursor()
		for i in range(len(df[0])):
			insert_df(df[i], '')
		logging.info(ticker+": inserted into db + committed")
		conn.commit()
	except Exception as err:
		conn = None
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
		cur.execute("""SELECT ticker FROM TICKERS""")
	except Exception as err:
		logging.error("SQL SELECT FAILED")
	tickers = cur.fetchall()


	vdate = date.today().strftime("%Y-%m-%d")
	
	print(f'starting computations on {cpu_count()} cores')
	start = timer()
	
	with Pool() as pool:
		try:
			args = [(t,vdate) for t in tickers]
			res = pool.starmap(mproc_job, args)
		except Exception as err:
			logging.error(err)
			return
	
		end = timer()
		print(f'elapsed time: {end - start}')
		
main()







