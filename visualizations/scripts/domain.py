from flask import Response, render_template, abort, g

def render_page_content():
	return render_template('domain.html')