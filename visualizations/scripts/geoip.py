import pygeoip
import json 

gi = pygeoip.GeoIP('/usr/local/share/geoip/GeoLiteCity.dat')
json_data = open('data/p_entropy_test.json')
data = json.load(json_data)

class Cluster(object):
	"""object to store parsed json data"""
	def __init__(self, parsed_json):
		self.id = parsed_json['ID']
		self.size = parsed_json['size']
		self.records = []
		self.locate_ip_addresses(parsed_json['sample_ip_mappings'])

	def locate_ip_addresses(self, addresses):
		for address in addresses:
			r = gi.record_by_addr(address)
			record = {}
			record['ip'] = address  
			record['latitude'] = r['latitude']
			record['longitude'] = r['longitude']
			record['city'] = r['city']
			self.records.append(record)


def get_clusters():
	j_clusters = data['clusters']
	clusters = []	
	for cluster in j_clusters:
		c = Cluster(cluster)
		clusters.append(c)
	return clusters


# clusters = get_clusters()
# for cluster in clusters: 
# 	print cluster.id