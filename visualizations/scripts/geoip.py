import pygeoip
import json 
from pprint import pprint

gi = pygeoip.GeoIP('/usr/local/share/geoip/GeoLiteCity.dat')

json_data = open('../data/p_entropy_test.json')
data = json.load(json_data)

clusters = data['clusters']


for cluster in clusters:
	pprint('Analyzing cluster ' + cluster[u'ID'])
	for ip_address in cluster['sample_ip_mappings']:
		record = gi.record_by_addr(ip_address)
		print '\t' + ip_address + ' -> ' + 'lat: ' + str(record['latitude']) + ", long: " + str(record['longitude']) + ', city: ' + record['city']


# pprint(data)

# gi = pygeoip.GeoIP('/usr/local/share/geoip/GeoLiteCity.dat')

# record = gi.record_by_addr('64.233.161.99')

# print record['longitude']
