from flask import Response, render_template, abort, g, jsonify

def render_page_content():
	rows = g.db.webview_domains.find().limit(40)
	return render_template('domains.html', rows=rows)


def render_json_answer(parameters):
	response_array = list()
	query_filter = _build_query_filter(parameters)

	if query_filter["$or"]:
		rows = g.db.webview_domains.find(query_filter)
	else:
		rows = g.db.webview_domains.find()

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

	# Check #queries range
	lowerBound = int(parameters['minReqs'])
	upperBound = int(parameters['maxReqs'])
	query_filter["req_count"] = { "$lt" : upperBound, "$gt" : lowerBound }

	# Check NX
	if parameters['nx'] == 'true':
		query_filter["$or"].append({"labels" : ["NXDOMAIN"]})

	# Check DGA
	if parameters['dga'] == 'true':
		if parameters['nx'] == 'true':
			query_filter["$or"].append({"labels" : ["NXDOMAIN", "DGA"]})
		else:
			query_filter["$or"].append({"labels" : ["DGA"]})

	# Check nonDGA
	if parameters['nonDga'] == 'true':
		if parameters['nx'] == 'true':
			query_filter["$or"].append({"labels" : ["NXDOMAIN"]})
		else:
			query_filter["$or"].append({"labels" : []})

	return query_filter

def _get_custom_results():
	return None