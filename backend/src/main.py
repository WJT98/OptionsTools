from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .entities.entity import Session, engine, Base
from .entities.ticker import Ticker

# generate database schema
Base.metadata.create_all(engine)

# start session
session = Session()

# check for existing data
tickers = session.query(Ticker).all()

if len(tickers) == 0:
    # create and persist mock tickers
    python_ticker = Ticker("SPY")
    session.add(python_ticker)
    session.commit()
    session.close()

    # reload tickers
    tickers = session.query(Ticker).all()

# show existing tickers
print('Tracked Tickers:')
for ticker in tickers:
    print(f'{ticker.ticker}: ')