import pygeoip
import json 
from bulkwhois.shadowserver import BulkWhoisShadowserver

gi = pygeoip.GeoIP('/usr/local/share/geoip/GeoLiteCity.dat')
json_data = open('data/p_entropy_test.json')
# json_data = open('data/p_entropy_test.small.json')
data = json.load(json_data)

class Cluster(object):
	"""object to store parsed json data"""
	def __init__(self, parsed_json):
		self.id = parsed_json['ID']
		self.size = parsed_json['size']
		self.records = []
		self.locate_ip_addresses(parsed_json['sample_ip_mappings'])
		self.domains = parsed_json["sample_domains"]
		self.public_suffixes = parsed_json["public_suffixes"]

	def locate_ip_addresses(self, addresses):
		bulk_whois = BulkWhoisShadowserver()
		ascii_addresses = [address.encode('ascii', 'ignore') for address in addresses]
		for address in ascii_addresses:
			r = gi.record_by_addr(address)
			w = bulk_whois.lookup_ips([address])
			record = {}
			record['ip'] = address  
			record['latitude'] = r['latitude']
			record['longitude'] = r['longitude']
			record['city'] = r['city']
			record['whois'] = w[address]
			self.records.append(record)


def get_clusters():
	j_clusters = data['clusters']
	clusters = []	
	for cluster in j_clusters:
		c = Cluster(cluster)
		clusters.append(c)
	return clusters