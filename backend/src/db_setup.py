import psycopg2
from psycopg2 import pool
import db_config
from psycopg2 import OperationalError, errorcodes, errors, Error
import sys

def db_connection():
	try:
		# create connection and cursor    
		conn = psycopg2.connect(user = db_config.user,
									password = db_config.password,
									host = db_config.host,
									port = db_config.port,
									database = db_config.database)
	except Exception as err:
		raise err
	return conn
	
def print_psycopg2_exception(err):
    # get details about the exception
    err_type, traceback = sys.exc_info()

    # get the line number when exception occured
    line_num = traceback.tb_lineno

    # print the connect() error
    print ("\npsycopg2 ERROR:", err, "on line number:", line_num)
    print ("psycopg2 traceback:", traceback, "-- type:", err_type)

    # psycopg2 extensions.Diagnostics object attribute
    print ("\nextensions.Diagnostics:", err.diag)

    # print the pgcode and pgerror exceptions
    print ("pgerror:", err.pgerror)
    print ("pgcode:", err.pgcode, "\n")

def exec_query(conn, query):
	try:
		cursor = conn.cursor()
		cursor.execute(query)
	except Error as err:
		conn.rollback()
		cursor.close()
		raise err


	
def main():
	try:
		conn = psycopg2.connect(user = db_config.user,
									password = db_config.password,
									host = db_config.host,
									port = db_config.port,
									database = db_config.database)
		if(conn):
			print("Connection created successfully")
		
		exec_query(conn, db_config.create_tickers_query)
		exec_query(conn, db_config.create_options_chain_query)
		exec_query(conn, db_config.create_options_metrics_query)
		

	except (Error, OperationalError) as err:
		conn = None
		print_psycopg2_exception(err)
	finally:
		if (conn):
			conn.close()
			print("PostgreSQL connection is closed")

main()







