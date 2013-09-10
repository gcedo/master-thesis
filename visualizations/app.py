from flask import Flask
from flask import render_template
from scripts.geoip import get_clusters

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/map")
def map():
	clusters = get_clusters()
   	return render_template('map.html', clusters=clusters)

@app.route("/domain/<domain>")
def domain(domain):
	return render_template('domain.html')

if __name__ == "__main__":
    app.run(debug=True)