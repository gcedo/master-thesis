from flask import render_template, g, jsonify

def render_page_content():
	countries, as_names, rows  = _build_response_array()
	return render_template('ips.html', rows=rows, countries=countries, as_names=as_names)


def render_json_answer(parameters=None):
	response = dict()
	_, _, response["ips"] = _build_response_array(parameters)
	return jsonify(response)


def _build_response_array(parameters=None):
	response_array = list()
	countries = set()
	as_names = set()
	if parameters:
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
		countries.add(country)
		as_name = row["as_name"]
		temp["as_name"] = as_name
		as_names.add(as_name)
		temp["as_code"] = row["as_code"]

		response_array.append(temp)
		sorted_countries = list()
		for country in countries:
			sorted_countries.append(country)
		sorted_countries.sort()

	return sorted_countries, as_names, response_array


def _build_query_filter(parameters):
	query_filter = dict()

	# Countries
	query_filter["$or"] = list()
	for country in parameters.getlist("countries"):
		query_filter["$or"].append({"geolocalization.country_code" : country.encode('ascii','ignore')})

	return query_filter


def _fetch_documents(query_filter=None):
	if query_filter:
		return g.db.webview_ips.find(query_filter)
	else:
		return g.db.webview_ips.find({}, \
			{'ip' : True, 'domain_count' : True, 'geolocalization' : True, 'as_code' : True, 'as_name' : True}) \
	     .sort([('domain_count' , -1), ('ip', 1)])
