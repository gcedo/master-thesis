from flask import Flask, g, render_template, request
from pymongo import Connection
from scripts.geoip import get_clusters
import scripts.domain as domain_engine
import scripts.map as map_engine

app = Flask(__name__)

# Database Handling
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


# Malicious Results
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

@app.route("/domains")
def domains():
   	return render_template("domains.html")

@app.route("/registars")
def registars():
   	return render_template("registars.html")

@app.route("/ips")
def ips():
   	return render_template("ips.html")

# How Phoenix Works routes
@app.route("/how_it_works")
def how():
   	return render_template("how_it_works.html")

@app.route("/filtering")
def filtering():
   	return render_template("agd_filtering.html")

@app.route("/clustering")
def clustering():
   	return render_template("clustering.html")

@app.route("/fingerprinting")
def fingerprinting():
   	return render_template("fingerprinting.html")

# Main
if __name__ == "__main__":
    app.run(debug=True)