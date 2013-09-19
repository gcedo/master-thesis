from flask import Response, render_template, abort, g, jsonify
from dateutil import parser
import pygeoip
import pycountry

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

def get_timeline(domain):
	domain_info = g.db.webview_domains.find_one({'domain' : domain})

	first_request_date = _get_formatted_date(domain_info["first_req_timestamp"])
	last_request_date = _get_formatted_date(domain_info["last_req_timestamp"])
	first_resolution_date = _get_formatted_date(domain_info["first_res_timestamp"])
	last_resolution_date = _get_formatted_date(domain_info["last_res_timestamp"])
	detection_date = _get_formatted_date(domain_info["detection_timestamp"])

	timeline = {
    "timeline":
    {
        "headline":"The Main Timeline Headline Goes here",
        "type":"default",
        "date": [
            {
                "startDate": first_request_date,
                "endDate": last_request_date,
                "headline":"First DNS request"
            },
            {
                "startDate": last_request_date,
                "endDate": last_request_date,
                "headline":"Last DSN request"
            },
            {
                "startDate": first_resolution_date,
                "endDate": last_resolution_date,
                "headline":"First DNS resolution"
            },
            {
                "startDate": last_resolution_date,
                "endDate": last_resolution_date,
                "headline":"Last DSN resolution"
            },
            {
                "startDate": detection_date,
                "endDate": detection_date,
                "headline":"Maliciousness detected"
            }
        ]
    }
	}
	return jsonify(timeline)

def _get_formatted_date(date):
	parser.parse(str(date))
	return str(date.year) + "," + str(date.month) + "," + str(date.day)

def _localize_ip_addresses(addresses):
	gi = pygeoip.GeoIP('data/GeoLiteCity.dat')
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