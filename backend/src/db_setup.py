import psycopg2
from psycopg2 import pool
import db_config
from psycopg2 import Error



def create_tickers():
	query = '''CREATE TABLE IF NOT EXISTS tickers (
		id			BIGSERIAL	NOT NULL,
		name		TEXT		NOT NULL,
		exchange 	TEXT		NOT NULL,
		PRIMARY KEY(id));'''

def create_options_chain():
	query = '''CREATE TABLE IF NOT EXISTS option_chain (
		id				BIGSERIAL	PRIMARY	KEY	NOT NULL,
		underlying_id	BIGSERIAL	NOT NULL,
		exp_date		DATE		NOT NULL,
		strike			SMALLINT 	NOT NULL,
		option			BIT(1)		NOT NULL,
		PRIMARY KEY(id),
		FOREIGN KEY(underlying_id) REFERENCES tickers(id));'''

def create_options_metrics():
	query = '''CREATE TABLE IF NOT EXISTS option_chain (
			id				BIGSERIAL		PRIMARY	KEY	NOT NULL,
			option_id		BIGSERIAL		NOT NULL,
			v_date			DATE			NOT NULL,
			bid				REAL 			NOT NULL,
			ask				REAL			NOT NULL,
			volume			INTEGER			NOT NULL,
			open_interest	BIGINT			NOT NULL,
			iv				NUMERIC(5,2)	NOT NULL
			delta			NUMERIC(5,4)	NOT NULL,
			gamma			NUMERIC(5,4)	NOT NULL,
			theta			NUMERIC(5,4)	NOT NULL,	
			alpha			NUMERIC(5,4)	NOT NULL,
			vega			NUMERIC(5,4)	NOT NULL,
			rho				NUMERIC(5,4)	NOT NULL,
			option			BIT(1)		NOT NULL,
			PRIMARY KEY(id),
			FOREIGN KEY(option_id) REFERENCES options_chain(id));'''


def main():
	try:
		postgreSQL_pool = psycopg2.pool.SimpleConnectionPool(1, 20,
												user = db_config.user,
												password = db_config.password,
												host = db_config.host,
												port = db_config.port,
												database = db_config.database)
			
		if(postgreSQL_pool):
			print("Connection pool created successfully")

		# Use getconn() to Get Connection from connection pool
		ps_connection  = postgreSQL_pool.getconn()

		if(ps_connection):
			print("successfully received connection from connection pool ")

			postgreSQL_pool.putconn(ps_connection)
			print("Put away a PostgreSQL connection")

	except (Exception, Error) as error :
		print ("Error while connecting to PostgreSQL", error)

	finally:
		if (postgreSQL_pool):
			postgreSQL_pool.closeall
		print("PostgreSQL connection pool is closed")



main()







