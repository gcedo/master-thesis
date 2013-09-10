from flask import Response, render_template, abort, g, jsonify

def render_page_content(domain):
	domain_info = g.db.webview_domains.find_one({'domain' : domain})

	record = dict()
	record["domain"] = domain_info["domain"]

	response = jsonify(record)
	return response