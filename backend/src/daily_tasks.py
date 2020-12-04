import psycopg2 as ps
import scrape_oic as so
import logging
import datetime import date

try:
    conn = connect(
        dbname = "python_test",
        user = "WRONG_USER",
        host = "localhost",
        password = "mypass"
    )
except OperationalError as err:
    # pass exception to function
    print_psycopg2_exception(err)

    # set the connection to 'None' in case of error
    conn = None


def db_connection(credentials):
	try:
		# create connection and cursor    
		conn = ps.connect(host=credentials['POSTGRES_ADDRESS'],
						database=credentials['POSTGRES_DBNAME'],
						user=credentials['POSTGRES_USERNAME'],
						password=credentials['POSTGRES_PASSWORD'],
						port=credentials['POSTGRES_PORT'])
	except OperationalError as err:
		logging.exception(print_psycopg2_exception(err))
		conn = None
	return conn
)
	
	

	return conn

def main():
	os.makedirs("logs")
	logger = logging.getLogger(today.strftime("%d/%m/%Y") + '.log')

	credentials = {'POSTGRES_ADDRESS' : 'historical-options-data.cirab4swhdtx.us-east-2.rds.amazonaws.com
	', # change to your endpoint
				'POSTGRES_PORT' : '5432', # change to your port
				'POSTGRES_USERNAME' : 'postgres', # change to your username
				'POSTGRES_PASSWORD' : 'asdf1234', # change to your password
				'POSTGRES_DBNAME' : 'postgres'} # change to your db name
	
	while True:
		conn = db_connection(credentials)
		if conn != None break
	
	cur = conn.cursor()

	while True:
		try:
			cur.execute("""SELECT * FROM TICKERS""")
		except Exception as err:
			#use logger here
		tickers = cur.fetchall()	
		if cur.fetchall() break

	for t in tickers:
		df = so.get_data()
	conn.commit()







