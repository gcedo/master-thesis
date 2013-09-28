from flask import render_template, g, jsonify, Response

def render_page_content():
	countries, as_names, rows  = _build_response_array()
	return render_template('ips.html', rows=rows)


def render_json_answer(parameters=None):
	response = dict()
	_, _, response["ips"] = _build_response_array(parameters)
	return jsonify(response)


def _build_response_array(parameters=None):
	response_array = list()
	countries = set()
	as_names = set()
	if parameters:
		pass
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

	return countries, as_names, response_array


def _build_query_filter(parameters):
	query_filter = dict()
	return query_filter


def _fetch_documents():
	return g.db.webview_ips.find({}, \
			{'ip' : True, 'domain_count' : True, 'geolocalization' : True, 'as_code' : True, 'as_name' : True}) \
	     .sort([('domain_count' , -1), ('ip', 1)]) \
