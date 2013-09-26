from flask import render_template, g, jsonify, Response
from dateutil import parser

def render_page_content():
	rows = g.db.webview_domains.find().limit(40)
	return render_template('domains.html', rows=rows)


def render_json_answer(parameters):
	response = dict()
	response["data"] = _build_response_array(parameters)
	return jsonify(response)

def render_csv_response(parameters):
	response_array = _build_response_array(parameters)
	values_array = list()

	for row in response_array:
		values = list()
		for key, value in row.items():
			if key == "labels":
				values.append(str(','.join(value)))
			else:
				values.append(str(value))
		values_array.append(values)

	def generate():
		yield "domain; labels; first_req_timestamp; last_req_timestamp; reqs\n"
		for row in values_array:
			yield ';'.join(row) + '\n'

	return Response(generate(), mimetype='text/csv')

def _build_response_array(parameters):
	query_filter = _build_query_filter(parameters)
	rows = g.db.webview_domains.find(query_filter)

	response_array = list()
	for row in rows:
		temp = dict()
		temp["domain"] = row["domain"]
		temp["labels"] = row["labels"]
		temp["first_req_timestamp"] = row["first_req_timestamp"]
		temp["last_req_timestamp"] = row["last_req_timestamp"]
		temp["reqs"] = row["req_count"]
		response_array.append(temp)

	return response_array


def _build_query_filter(parameters):
	query_filter = dict()

	# Check #queries range
	lowerBound = int(parameters['minReqs'])
	upperBound = int(parameters['maxReqs'])
	query_filter["req_count"] = { "$lt" : upperBound, "$gt" : lowerBound }

	# Check for dates
	sinceDate = parser.parse(parameters["since"])
	print sinceDate
	toDate = parser.parse(parameters["to"])
	print toDate
	query_filter["first_req_timestamp"] = { "$gt" : sinceDate }
	query_filter["last_req_timestamp"]  = { "$lt" : toDate }

	if parameters['nx'] == 'true' or parameters['dga'] == 'true' or parameters['nonDga'] == 'true':
		query_filter["$or"] = list()
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