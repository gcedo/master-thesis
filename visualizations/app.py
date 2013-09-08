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

if __name__ == "__main__":
    app.run(debug=True)