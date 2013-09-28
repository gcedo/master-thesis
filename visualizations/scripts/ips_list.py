from flask import render_template, g, jsonify, Response

def render_page_content():
	rows  = _build_response_array()
	return render_template('ips.html', rows=rows)


def render_json_answer(parameters=None):
	response = dict()
	response["ips"] = _build_response_array(parameters)
	return jsonify(response)


def _build_response_array(parameters=None):
	response_array = list()
	if parameters:
		pass
	else:
		rows = _fetch_documents()

	for row in rows:
		temp = dict()
		temp["ip"] = row["ip"]
		temp["country_code"] = row["geolocalization"]["country_code"]
		temp["as_name"] = row["as_name"]
		temp["as_code"] = row["as_code"]

		response_array.append(temp)

	return response_array


def _build_query_filter(parameters):
	query_filter = dict()
	return query_filter


def _fetch_documents():
	return g.db.webview_ips.find({}, \
			{'ip' : True, 'domain_count' : True, 'geolocalization' : True, 'as_code' : True, 'as_name' : True}) \
	     .sort([('domain_count' , -1), ('ip', 1)]) \
