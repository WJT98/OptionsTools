from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_migrate import Migrate
import src.daily_tasks
import time
from datetime import date, timedelta
import os
import requests


from apscheduler.schedulers.background import BackgroundScheduler
#schedule this for 
d =  date.today().strftime("%Y-%m-%d")
sched = BackgroundScheduler(daemon=True)
sched.add_job(scrape_options,'date',run_date='2009-11-06 16:30:05', args=['text'])
sched.start()

def schedule_scraper(next_period):
	sched.add_job(scrape_options,'date',run_date='2009-11-06 16:30:05', args=['text'])

def scrape_options():
	#TODO: log instead
	print(print_date_time(), + ": starting scraper")
	r = requests.get('http://en.wikipedia.org/wiki/Monty_Python')

	yesterday = date.today() - timedelta(days=1)
	last_modified_date = yesterday
	while(last_modified_date == yesterday):
		last_modified_date = r.headers["Last-Modified"]
		time.sleep(600)
	src.daily_tasks.run_scraper()
	tomorrow = date.today() + timedelta(days=1)
	schedule_scraper(tomorrow)
	
def print_date_time():
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))

app = Flask(__name__)
CORS(app)

@app.route('/tickers')
def get_tickers():
	#return jsonify(tickers)
	return

@app.route('/logs')
def get_log():
	d = date.today().strftime("%Y-%m-%d")
	with open(os.getcwd() + 'src/logs/'+d+'.log') as f:
	#with open(os.getcwd() + '/src/logs/2020-12-27.log') as f:
		log = f.read()
	print(log)
	return log


@app.route('/tickers/<ticker>', methods=['POST'])
def add_ticker(ticker):
	
	#return jsonify(new_ticker), 201
	return 201

if __name__ == '__main__':
    app.run(debug=True)





#fuser -n tcp -k 5000
#curl http://0.0.0.0:5000/logs
#./bootstrap.sh &