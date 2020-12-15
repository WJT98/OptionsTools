import psycopg2 as ps
import scrape_oic as so
import logging
from datetime import date
import os
from multiprocessing import Pool, cpu_count
from timeit import default_timer as timer
import pandas as pd

def db_connection(credentials):
	try:
		# create connection and cursor    
		conn = ps.connect(host=credentials['POSTGRES_ADDRESS'],
						database=credentials['POSTGRES_DBNAME'],
						user=credentials['POSTGRES_USERNAME'],
						password=credentials['POSTGRES_PASSWORD'],
						port=credentials['POSTGRES_PORT'])
	except Exception as err:
		#logging.error(print_psycopg2_exception(err))
		print(err)
		conn = None
	return conn
	
def insert_df(df, tablename, conn):
	
	return None

def main():
	if not os.path.isdir("logs"):
		os.makedirs("logs")
	logging.basicConfig(level=logging.DEBUG, 
						format= '[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
     					datefmt='%Y-%m-%d %H:%M:%S',
						handlers=[
							logging.FileHandler('logs/'+date.today().strftime("%Y-%m-%d") + '.log'),
							logging.StreamHandler()])	
	credentials = {'POSTGRES_ADDRESS' : 'historical-options-data.cirab4swhdtx.us-east-2.rds.amazonaws.com', 
				'POSTGRES_PORT' : '5432', 
				'POSTGRES_USERNAME' : 'postgres', 
				'POSTGRES_PASSWORD' : 'asdf1234',
				'POSTGRES_DBNAME' : 'postgres'} 
	
	while True:
		conn = db_connection(credentials)
		if conn is not None: 
			logging.info("DB connection established")
			break
		else:
			logging.error("DB connection refused")

	cur = conn.cursor()
	while True:
		try:
			cur.execute("""SELECT ticker FROM TICKERS""")
		except Exception as err:
			logging.error("SQL SELECT FAILED")
		tickers = cur.fetchall()
		if tickers:
			break

	vdate = date.today().strftime("%Y-%m-%d")
	
	print(f'starting computations on {cpu_count()} cores')
	start = timer()
	
	with Pool() as pool:
		try:
			args = [(t,vdate) for t in tickers]
			res = pool.starmap(so.get_data, args)
		except Exception as err:
			logging.error(err)
			return
		logging.info("EOD options data scraped into list of dataframes for all tickers")
	
		end = timer()
		print(f'elapsed time: {end - start}')
		
		try:
			res = pool.map(so.process_df, res)
		except Exception as err:
			logging.error(err)
			return
		logging.info("Processed all dataframes")
		
		try:
			args = [x + (conn,) for x in res]
			res = pool.starmap(insert_df, args)
		except Exception as err:
			logging.error(err)
			return
		conn.commit()
		logging.info("All dataframes inserted into db + committed")
		
main()







