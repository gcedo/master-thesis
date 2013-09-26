from flask import Response, render_template, abort, g, jsonify

def render_page_content(mime="html"):

	rows = g.db.webview_domains.find().limit(40)
	return render_template('domains.html', rows=rows)