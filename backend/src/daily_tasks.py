import psycopg2 as ps
import scrape_oic as so
import logging
from datetime import date
import os
import threading
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
	
def insert_df(conn, df, tablename):
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

	d = date.today().strftime("%Y-%m-%d")
	for t in tickers:
		df = so.get_data(t[0],d)
		print(list(df.loc[0]))
		pd.set_option("display.max_rows", 5, "display.max_columns", None)
		print(df.head())
		break 
		err = insert_df(conn, df, t[0])
		if err:
			logging.error(err)
		else:
			conn.commit()
			logging.info(t[0] + " EOD options data inserted")

main()







