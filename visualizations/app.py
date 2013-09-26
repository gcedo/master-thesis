from flask import Flask, g, render_template, request, session, redirect, url_for
from pymongo import MongoClient
from scripts.geoip import get_clusters
import scripts.domain as domain_engine
import scripts.map as map_engine
import scripts.domains_list as domains_engine

app = Flask(__name__)

# Spaghetti Login Management
USERNAME = "captain_kirk"
PASSWORD = "vombato.is.cute42"
SECRET_KEY = 'development key'
ALLOWED_ITEMS = ["/static/css/bootstrap.min.css", "/static/js/bootstrap.min.js",
                 "/login", "/static/js/jquery.min.js"]

app.config.from_object(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True


#Database Handling
def connect_db():
	client = MongoClient('mongodb://phoenix-user:vombato.is.cute42@ds045938.mongolab.com:45938/botime')
	return client.botime

@app.before_request
def before_request():
  if not session.get('logged_in') and request.path not in ALLOWED_ITEMS:
    return redirect(url_for('login'))
  g.db = connect_db()

@app.route("/login", methods=['GET', 'POST'])
def login():
  error = None
  if request.method == 'POST':
    if request.form['username'] != USERNAME:
      error = 'Invalid username'
    elif request.form['password'] != PASSWORD:
      error = 'Invalid password'
    else:
      session['logged_in'] = True
      return redirect("/")
  return render_template('login.html', error=error)


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
  if 'json' in request.args:
    parameters = dict()
    parameters["dga"] = request.args["dga"]
    return domains_engine.render_json_answer(parameters=parameters)
  else:
    return domains_engine.render_page_content()

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