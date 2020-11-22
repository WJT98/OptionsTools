# coding=utf-8
from .ticker import Ticker
from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_url = 'historical-options-data.cirab4swhdtx.us-east-2.rds.amazonaws.com:5432'
db_name = 'postgres'
db_user = 'postgres'
db_password = 'asdf1234'
engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_url}/{db_name}')
Session = sessionmaker(bind=engine)

Base = declarative_base()



# generate database schema
Base.metadata.create_all(engine)

# start session
session = Session()

# check for existing data
tickers = session.query(Ticker).all()

if len(tickers) == 0:
    # create and persist mock exam
    python_ticker = Ticker("SPY")
    session.add(python_ticker)
    session.commit()
    session.close()

    # reload exams
    tickers = session.query(Ticker).all()

# show existing exams
print('Tracked Tickers:')
for ticker in tickers:
    print(f'{ticker.ticker}')