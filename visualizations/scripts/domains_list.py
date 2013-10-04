from flask import render_template, g, jsonify, Response
from dateutil import parser

BATCH_SIZE = 100

def render_page_content():
	rows = g.db.webapp_demo.find().sort({"domain" : 1}).limit(BATCH_SIZE)
	return render_template('domains.html', rows=rows)


def render_json_answer(parameters):
	response = dict()
	response["data"] = _build_response_array(parameters)
	return jsonify(response)

def render_csv_response(parameters):
	response_array = _build_response_array(parameters, False)
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

def _build_response_array(parameters, ips=True):
	query_filter = _build_query_filter(parameters)
	if parameters.get("skip") is not None:
		skip = int(parameters.get("skip"))
		rows = g.db.webapp_demo.find(query_filter).limit(BATCH_SIZE).skip(skip * BATCH_SIZE)
	else:
		rows = g.db.webapp_demo.find(query_filter).limit(BATCH_SIZE)

	response_array = list()
	for row in rows:
		temp = dict()
		temp["domain"] = row["domain"]
		temp["label"] = row["label"]
		temp["first_req_timestamp"] = row["first_req_timestamp"]
		temp["last_req_timestamp"] = row["last_req_timestamp"]
		if ips:
			temp["ips"] = row["ips"]
		response_array.append(temp)

	return response_array


def _build_query_filter(parameters):
	query_filter = dict()

	# Check #queries range
	lowerBound = int(parameters['minReqs'])
	upperBound = int(parameters['maxReqs'])
	query_filter["req_count"] = { "$lt" : upperBound, "$gt" : lowerBound }

	# # Check for dates
	sinceDate = parser.parse(parameters["since"])
	print sinceDate
	toDate = parser.parse(parameters["to"])
	print toDate
	query_filter["first_req_timestamp"] = { "$gt" : sinceDate }
	query_filter["last_req_timestamp"]  = { "$lt" : toDate }

	query_filter["$or"] = list()
	# Check DGA
	if parameters['dga'] == 'true':
		query_filter["$or"].append({"label" : "DGA"})
	# Check nonDGA
	if parameters['nonDga'] == 'true':
		query_filter["$or"].append({"label" : "non-DGA"})

	return query_filter