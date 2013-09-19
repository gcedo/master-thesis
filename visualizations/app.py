from flask import Flask, g, render_template, request
from pymongo import MongoClient
from scripts.geoip import get_clusters
import scripts.domain as domain_engine
import scripts.map as map_engine

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True

#Database Handling
def connect_db():
	client = MongoClient('mongodb://phoenix-user:vombato.is.cute42@ds045938.mongolab.com:45938/botime')
	return client.botime

@app.before_request
def before_request():
  g.db = connect_db()

@app.route("/")
def index():
  return render_template("index.html")


# Malicious Results
@app.route("/map")
def map():
  return map_engine.render_page_content()

@app.route("/overview")
def overview():
  return render_template('results_overview.html')

@app.route("/domains")
def domains():
  return render_template("domains.html")

@app.route("/domain/<domain>")
def domain(domain):
  if 'json' in request.args:
    return domain_engine.render_page_content(domain, mime='json')
  elif 'timeline' in request.args:
    return domain_engine.get_timeline(domain)
  else:
    return domain_engine.render_page_content(domain, mime='html')

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