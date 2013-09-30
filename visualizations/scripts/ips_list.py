from flask import render_template, g, jsonify, Response

BATCH_SIZE = 100

def render_page_content():
	rows  = _build_response_array()
	countries = g.db.webview_ips.distinct('geolocalization.country_code')
	countries = list(countries)
	countries.sort()
	return render_template('ips.html', rows=rows, countries=countries)


def render_json_answer(parameters=None):
	response = dict()
	response["ips"] = _build_response_array(parameters)
	return jsonify(response)


def render_csv_response(parameters=None):
	response_array = _build_response_array(parameters)
	values_array = list()

	for row in response_array:
		values = list()
		for key, value in row.items():
			values.append(value)
		values_array.append(values)

	def generate():
		yield "as_code; as_name; country_code; ip\n"
		for row in values_array:
			yield ';'.join(row) + '\n'

	return Response(generate(), mimetype='text/csv')


def _build_response_array(parameters=None):
	response_array = list()

	if parameters and parameters.getlist("countries"):
		query_filter = _build_query_filter(parameters)
		print query_filter
		rows = _fetch_documents(query_filter)
	else:
		rows = _fetch_documents()

	for row in rows:
		temp = dict()
		temp["ip"] = row["ip"]
		country = row["geolocalization"]["country_code"]
		temp["country_code"] = country
		as_name = row["as_name"]
		temp["as_name"] = as_name
		temp["as_code"] = row["as_code"]
		response_array.append(temp)

	return response_array


def _build_query_filter(parameters):
	query_filter = dict()

	# Countries
	query_filter["$or"] = list()
	for country in parameters.getlist("countries"):
		query_filter["$or"].append({"geolocalization.country_code" : country.encode('ascii','ignore')})

	return query_filter


def _fetch_documents(query_filter=None):
	if query_filter:
		return g.db.webview_ips.find(query_filter).limit(100)
	else:
		return g.db.webview_ips.find({}, \
			{'ip' : True, 'domain_count' : True, 'geolocalization' : True, 'as_code' : True, 'as_name' : True}) \
	     .sort([('domain_count' , -1), ('ip', 1)]).limit(100)
