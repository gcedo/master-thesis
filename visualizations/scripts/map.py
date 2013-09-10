from flask import Response, render_template, abort, g
from geoip import get_clusters

def render_page_content():
	clusters = get_clusters()
	return render_template('map.html', clusters=clusters)