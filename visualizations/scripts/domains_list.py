from flask import Response, render_template, abort, g, jsonify

def render_page_content():

	rows = g.db.webview_domains.find().limit(40)
	return render_template('domains.html', rows=rows)


def render_json_answer(parameters):
	response_array = list()

	if parameters['dga'] == 'true':
		rows = g.db.webview_domains.find({ 'labels': 'DGA'})

	for row in rows:
		temp = dict()
		temp["domain"] = row["domain"]
		temp["labels"] = row["labels"]
		temp["first_req_timestamp"] = row["first_req_timestamp"]
		temp["last_req_timestamp"] = row["last_req_timestamp"]
		response_array.append(temp)

	response = dict()
	response["data"] = response_array

	return jsonify(response)


def _get_custom_results():
	return None