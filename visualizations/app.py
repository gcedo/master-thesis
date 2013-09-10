from flask import Flask, g, render_template, request
from pymongo import Connection
from scripts.geoip import get_clusters
import scripts.domain as domain_engine
import scripts.map as map_engine

app = Flask(__name__)


def connect_db():
	conn = Connection()
	db = conn.botime
	return conn, db

@app.before_request
def before_request():
    g.conn, g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    g.conn.close()

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/map")
def map():
   	return map_engine.render_page_content()

@app.route("/domain/<domain>")
def domain(domain):
	if 'json' in request.args:
		return domain_engine.render_page_content(domain, mime='json')
	elif 'timeline' in request.args:
		return domain_engine.get_timeline(domain)
	else:
		return domain_engine.render_page_content(domain, mime='html')

if __name__ == "__main__":
    app.run(debug=True)