from flask import Response, render_template, abort, g, jsonify
import pygeoip

def render_page_content(domain_name, mime="html"):
	domain_info = g.db.webview_domains.find_one({'domain' : domain_name})

	record = dict()
	record["domain"] = domain_info["domain"]
	record["first_resolution_timestamp"] = domain_info["first_res_timestamp"]
	record["last_resolution_timestamp"] = domain_info["last_res_timestamp"]
	record["first_request_timestamp"] = domain_info["first_req_timestamp"]
	record["last_request_timestamp"] = domain_info["last_req_timestamp"]
	record["labels"] = domain_info["labels"]
	record["country_preview"] = domain_info["country_preview"]
	record["country_count"] = domain_info["country_count"]
	record["res_count"] = domain_info["res_count"]
	record["ip_count"] = domain_info["ip_count"]
	record["req_count"] = domain_info["req_count"]
	record["detection_timestamp"] = domain_info["detection_timestamp"]
	record["as_preview"] = domain_info["as_preview"]
	record["as_count"] = domain_info["as_count"]

	record["ips"] = _localize_ip_addresses(domain_info["ip_preview"])

	if (mime is "html"):
		return render_template('domain.html', record=record)
	else:
		response = jsonify(record)
		return response

def _localize_ip_addresses(addresses):
	gi = pygeoip.GeoIP('/usr/local/share/geoip/GeoLiteCity.dat')
	records = dict()
	for address in addresses:
		r = gi.record_by_addr(address["ip"])
		record = dict()
		record['ip'] = address  
		record['latitude'] = r['latitude']
		record['longitude'] = r['longitude']
		record['city'] = r['city']
		records[address["ip"]] = record
	return records