import psycopg2
import psycopg2.extras
import scrape_oic as so
import logging
from datetime import date
import os

from multiprocessing import Pool, cpu_count, Lock
from timeit import default_timer as timer
import pandas as pd
import db_config
import db_setup
import csv

def update_options_chain(ticker, conn):
	try:
		cursor = conn.cursor()
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
		cursor.execute(q)
		conn.commit()
	except Exception as err:
		raise err
	finally:
		if cursor: 
			cursor.close()
		

# def update_options_metrics(ticker, conn):

def truncate_table(conn):
	try:
		cursor = conn.cursor()
		cursor.execute('TRUNCATE TABLE imports;')
	except Exception as err:
		raise err
	finally:
		if cursor:
			cursor.close()

def import_table(csv_file, ticker, conn):
	try:
		cursor = conn.cursor()
		with open(csv_file, 'r') as f:
			reader = csv.reader(f)
			headers = next(reader)
			cursor.copy_from(f, 'imports', columns=headers,sep=',')
			conn.commit()
	except Exception as err:
		raise err
	finally:
		if cursor: 
			cursor.close()

def main():
	conn = db_setup.get_conn()
	ticker = ('SPY', 'NYSE')
	csv = 'csv/SPY/2020-12-31/2020-12-26.csv'
	try:
		start = timer()
		truncate_table(conn)
		import_table(csv,ticker,conn)			
		end = timer()
		update_options_chain('SPY', conn)
		print(f'elapsed time: {end - start}')
	except Exception as err:
		db_setup.print_psycopg2_exception(err)

if __name__ == '__main__':
	main()