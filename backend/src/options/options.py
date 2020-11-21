# coding=utf-8

from datetime import datetime
from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_url = 'historical-options-data.cirab4swhdtx.us-east-2.rds.amazonaws.com:5432'
db_name = 'historical-options-data'
db_user = 'postgres'
db_password = 'asdf1234'
engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_url}/{db_name}')
Session = sessionmaker(bind=engine)

Base = declarative_base()


# import psycopg2 as ps
# # define credentials 
# credentials = {'POSTGRES_ADDRESS' : '', # change to your endpoint
#                'POSTGRES_PORT' : '', # change to your port
#                'POSTGRES_USERNAME' : '', # change to your username
#                'POSTGRES_PASSWORD' : '', # change to your password
#                'POSTGRES_DBNAME' : ''} # change to your db name
# # create connection and cursor    
# conn = ps.connect(host=credentials['POSTGRES_ADDRESS'],
#                   database=credentials['POSTGRES_DBNAME'],
#                   user=credentials['POSTGRES_USERNAME'],
#                   password=credentials['POSTGRES_PASSWORD'],
#                   port=credentials['POSTGRES_PORT'])
# cur = conn.cursor()


class Option():
    id = Column(Integer, primary_key=True)
    ticker = Column(String)

    def __init__(self, created_by):
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.last_updated_by = created_by