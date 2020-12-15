from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_migrate import Migrate

from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .entities.entity import Session, engine, Base
from .entities.ticker import Ticker, TickerSchema

app = Flask(__name__)
CORS(app)
# generate database schema
Base.metadata.create_all(engine)

@app.route('/tickers')
def get_tickers():
	session = Session()

	ticker_objects = session.query(Ticker).all()

	schema = TickerSchema(many=True)
	tickers = schema.dump(ticker_objects)

	session.close()
	return jsonify(tickers)


@app.route('/tickers', methods=['POST'])
def add_ticker():
	new_ticker = TickerSchema(only=('ticker'))\
		.load (request.get_json())

	ticker = Ticker(**new_ticker.ticker)

	session = Session()
	session.add(ticker)
	session.commit()

	new_ticker = TickerSchema().dump(ticker).data
	session.close()
	return jsonify(new_ticker), 201

if __name__ == '__main__':
    app.run(debug=True)

#fuser -n tcp -k 5000
#curl http://0.0.0.0:5000/tickers
#./bootstrap.sh &