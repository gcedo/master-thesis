from dga_classifier.core.helper.tools import clean_string
from dga_classifier.core.domain.domain import Domain
from dga_classifier.core.database.database import DatabaseInterface
from dga_classifier.core.clustering.cluster_descriptor import BipartiteGraphDescriptor
from dga_classifier.core.timeseries.timeseries import TimeseriesToolbox
from dga_classifier.core.helper.tools import AutonomousSystemDatabase
from dga_classifier.core.helper.tools import colored_label
import random
import numpy


########################################
## Domain cluster toolbox
########################################

class DomainClusterToolbox:
	def __init__(self):
		pass

	def copy(self, cluster, identifier):
		new_cluster = DomainCluster(identifier)
		new_cluster.add_bulk_domains(cluster)

		return new_cluster

	def merge(self, cluster_list, identifier):
		new_cluster = DomainCluster(identifier)

		for cluster in cluster_list:
			new_cluster.add_bulk_domains(cluster)

		return new_cluster

	def split(self, cluster, size, max_number = None):
		all_domains = list(cluster)

		def sample():
			temp = list()
			temp.extend(all_domains[0:size])
			count = len(temp)

			for elem in all_domains[size:]:
				count = count + 1
				p = size / float(count)

				if (random.random() < p):
					index_to_remove = random.randrange(0, len(temp))
					temp[index_to_remove] = elem

			return temp

		if max_number == None:
			max_number = len(cluster)

		resulting_clusters = list()
		cluster_prefix = cluster.get_identifier() + "_"

		next_index = 0

		while True:
			if next_index == max_number:
				break

			if len(all_domains) <= size:
				new_cluster = DomainCluster(cluster_prefix + str(next_index))
				new_cluster.add_bulk_domains(all_domains)
				resulting_clusters.append(new_cluster)
				break

			current_sample = sample()
			current_sample_set = set(current_sample)

			all_domains = filter(lambda x: x not in current_sample_set, all_domains)
			new_cluster = DomainCluster(cluster_prefix + str(next_index))
			next_index += 1
			new_cluster.add_bulk_domains(current_sample)
			resulting_clusters.append(new_cluster)

		return resulting_clusters

	def normalize_bipartite_graph_spectral_features(self, cluster, dimension):
		values = list()

		for domain in cluster:
			value = domain.get_bipartite_graph_feature_set().get_dimension_value(dimension)
			values.append(value)

		average = numpy.average(values)
		std_dev = numpy.std(values)

		for domain in cluster:
			old_value = domain.get_bipartite_graph_feature_set().get_dimension_value(dimension)

			if std_dev > 0:
				new_value = (old_value - average) / std_dev
			else:
				new_value = (old_value - average)

			domain.get_bipartite_graph_feature_set().set_dimension_value(dimension, new_value)


########################################
## Domain cluster database factory
########################################

class DomainClusterDatabaseFactory:
	def __init__(self, experiment, identifier = 'cluster_0', webapp=False):
		try:
			database_instance = DatabaseInterface()
		except DatabaseInterface as old_database_instance:
			database_instance = old_database_instance

		self._cluster = DomainCluster(identifier)
		# START: Web app: Oct 1 2013
		for domain_name in database_instance.get_all_domain_names(experiment, webapp):
			self._cluster.add_domain(Domain(domain_name, experiment, webapp))
		# END: Web app: Oct 1 2013

	def get(self):
		return self._cluster


#######################################
# Domain cluster file factory
#######################################

class DomainClusterFileFactory:
	def __init__(self, file_path, two_columns_format):
		self._clusters = dict()

		with open(file_path.strip(), 'r') as lines:
			if not two_columns_format:
				self._clusters['cluster_0'] = DomainCluster('cluster_0')

			for line in lines:
				line = clean_string(line)

				if two_columns_format:
					partition = line.partition(',')
					str_domain_name = clean_string(partition[0])
					cluster_identifier = clean_string(partition[2])

					if cluster_identifier in self._clusters:
						current_cluster = self._clusters[cluster_identifier]
					else:
						current_cluster = DomainCluster(cluster_identifier)
						self._clusters[cluster_identifier] = current_cluster

					current_cluster.add_domain(Domain(str_domain_name))
				else:
					self._clusters['cluster_0'].add_domain(Domain(line, None))

	def get_identifiers(self):
		return self._clusters.keys()

	def get(self, cluster_identifier):
		if (cluster_identifier in self._clusters):
			return self._clusters[cluster_identifier]
		else:
			raise Exception('The cluster identifier ' + cluster_identifier + ' does not exist.')


########################################
## Domain cluster
########################################

class DomainCluster:
	def __init__(self, cluster_identifier):
		self._domain_list = list()
		self._identifier = cluster_identifier
		self._bipartite_graph_descriptor = None
		self._linguistic_descriptor = None
		self._timeseries = None

	def __len__(self):
		return len(self._domain_list)

	def __str__(self):
		preview_domains = 10
		preview_ips = 10
		preview_as = 10

		decoration = colored_label('#########################################')

		result = colored_label('ID: ') + self._identifier + '\n'
		result += colored_label('Size: ') + str(len(self)) + '\n'

		if self._bipartite_graph_descriptor != None:
			result += str(self._bipartite_graph_descriptor) + '\n'

		ip_list = list(self.get_ip_set())
		result += colored_label('IP mappings size: ') + str(len(ip_list)) + '\n'
		result += colored_label('Sample IP mappings:\n')
		result += '\n'.join(map(lambda x: '     -->  ' + str(x), ip_list[0:preview_ips])) + '\n'

		# ip_backbone_list = list(self.get_ip_backbone_set())
		# result += 'Backbone IP mappings size: ' + str(len(ip_backbone_list)) + '\n'
		# result += 'Backbone sample IP mappings:\n'
		# result += '\n'.join(map(lambda x: '     -->  ' + str(x), ip_backbone_list[0:preview_ips])) + '\n'

		# as_list = list(self.get_as_set())
		# result += colored_label('AS mappings size: ') + str(len(as_list)) + '\n'
		# result += colored_label('Sample AS mappings:\n')
		# result += '\n'.join(map(lambda x: '     -->  ' + str(x), as_list[0:preview_as])) + '\n'

		if self._linguistic_descriptor != None:
			result += str(self._linguistic_descriptor) + '\n'

		result += colored_label('Sample domains:\n')
		result += '\n'.join(map(lambda x: '     -->  ' + str(x), self._domain_list[0:preview_domains]))
		result += '\n' + decoration

		return result

	def __iter__(self):
		return iter(self._domain_list)

	def set_identifier(self, identifier):
		self._identifier = identifier

	def get_identifier(self):
		return self._identifier

	def add_domain(self, domain):
		self._domain_list.append(domain)

	def add_bulk_domains(self, container):
		for domain in container:
			self._domain_list.append(domain)

	def clear_bipartite_graph_features(self):
		self._bipartite_graph_descriptor = None

		for domain in self._domain_list:
			domain.set_bipartite_graph_feature_set(None)

	def get_as_set(self):
		try:
			as_db_instance = AutonomousSystemDatabase()
		except AutonomousSystemDatabase as old_as_db_instance:
			as_db_instance = old_as_db_instance

		ip_set = self.get_ip_set()
		as_set = set()

		for ip in ip_set:
			as_set.add(as_db_instance.get_as_by_address(ip))

		return as_set

	def get_domains(self):
		return self._domain_list

	def get_ip_set(self):
		ip_set = set()

		for domain in self._domain_list:
			for ip in domain.get_ip_mappings():
				ip_set.add(ip)

		return ip_set

	def get_ip_backbone_set(self):
		ip_set = set(self._domain_list[0].get_ip_mappings())

		for domain in self._domain_list[1:]:
			ip_set.intersection_update(domain.get_ip_mappings())

		return ip_set

	def set_bipartite_graph_descriptor(self, descriptor):
		self._bipartite_graph_descriptor = descriptor

	def get_bipartite_graph_descriptor(self):
		if self._bipartite_graph_descriptor == None:
			raise Exception('The bipartite graph descriptor is not set.')

		return self._bipartite_graph_descriptor

	def set_linguistic_descriptor(self, descriptor):
		self._linguistic_descriptor = descriptor

	def get_linguistic_descriptor(self):
		if self._linguistic_descriptor == None:
			raise Exception('The linguistic descriptor is not set.')

		return self._linguistic_descriptor

	def get_timeseries(self):
		if self._timeseries == None:
			list_of_timeseries = map(lambda x: x.get_timeseries(), self._domain_list)
			toolbox = TimeseriesToolbox()
			self._timeseries = toolbox.merge(list_of_timeseries, sum)

		return self._timeseries