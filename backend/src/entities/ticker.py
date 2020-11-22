# coding=utf-8
from .entity import Entity, Base
from sqlalchemy import Column, String

from marshmallow import Schema, fields


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

class Ticker(Entity, Base):
	__tablename__ = 'tickers'
	ticker = Column(String, primary_key=True)

class TickerSchema(Schema):
    ticker = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()