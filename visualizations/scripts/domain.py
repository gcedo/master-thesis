from flask import render_template, g, jsonify
from dateutil import parser
import pygeoip

def render_page_content(domain_name, mime="html"):
	domain_info = g.db.webapp_demo.find_one({'domain' : domain_name})

	record = dict()
	record["domain"] = domain_info["domain"]
	record["first_request_timestamp"] = domain_info["first_req_timestamp"]
	record["last_request_timestamp"] = domain_info["last_req_timestamp"]
	record["first_resolution_timestamp"] = domain_info["first_res_timestamp"]
	record["last_resolution_timestamp"] = domain_info["last_res_timestamp"]
	record["label"] = domain_info["label"]
	record["req_count"] = domain_info["req_count"]
	record["queries"] = domain_info["queries"]

	record["ips"], countries = _localize_ip_addresses(domain_info["ips"])

	if (mime is "html"):
		return render_template('domain.html', record=record, countries=countries)
	else:
		response = jsonify(record)
		return response

def get_timeline(domain):
	domain_info = g.db.webapp_demo.find_one({'domain' : domain})

	first_request_date = _get_formatted_date(domain_info["first_req_timestamp"])
	last_request_date = _get_formatted_date(domain_info["last_req_timestamp"])
	last_resolution_date = _get_formatted_date(domain_info["last_res_timestamp"])
	first_resolution_date = _get_formatted_date(domain_info["first_res_timestamp"])

	timeline = {
    "timeline":
    {
        "headline":"Domain requests and replies",
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
                "startDate": last_resolution_date,
                "endDate": last_resolution_date,
                "headline":"Last DSN request"
            },
            {
                "startDate": first_resolution_date,
                "endDate": last_resolution_date,
                "headline":"Last DSN request"
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
	countries = dict()
	print addresses
	for address in addresses:
		r = gi.record_by_addr(address)
		record = dict()
		record['ip'] = address
		record['latitude'] = r['latitude']
		record['longitude'] = r['longitude']
		record['city'] = r['city']
		records[address] = record
		countries[r['country_code'].lower()] = r['country_name']
	return records, countries