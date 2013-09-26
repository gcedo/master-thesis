from flask import Response, render_template, abort, g, jsonify

def render_page_content():
	rows = g.db.webview_domains.find( {"$or" : [{"labels" : ["DGA"]}, {"labels": [] }] })
	return render_template('domains.html', rows=rows)


def render_json_answer(parameters):
	response_array = list()

	rows = g.db.webview_domains.find(_build_query_filter(parameters))

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


def _build_query_filter(parameters):
	query_filter = dict()
	query_filter["$or"] = list()

	if parameters['dga'] == 'true':
		if parameters['nx'] == 'true':
			query_filter["$or"].append({"labels" : ["NXDOMAIN", "DGA"]})
		else:
			query_filter["$or"].append({"labels" : ["DGA"]})
	if parameters['nonDga'] == 'true':
		if parameters['nx'] == 'true':
			query_filter["$or"].append({"labels" : ["NXDOMAIN"]})
		else:
			query_filter["$or"].append({"labels" : []})

	return query_filter

def _get_custom_results():
	return None