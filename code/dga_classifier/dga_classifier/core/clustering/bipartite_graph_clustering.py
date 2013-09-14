from dga_classifier.core.clustering.cluster import DomainCluster
from dga_classifier.core.clustering.cluster import DomainClusterToolbox
from dga_classifier.core.clustering.cluster_descriptor import BipartiteGraphDescriptor
from scipy.sparse import dok_matrix
from scipy.sparse import lil_matrix
from scipy.sparse import csc_matrix
from scipy.sparse.linalg import eigs
import numpy
import math
# import matplotlib.pyplot as plt
# import networkx as nx

########################################
## Flooding clusterer
########################################

# class FloodingClusterer:
# 	def __init__(self):
# 		pass

# 	def generate_subclusters(self, cluster):
# 		remaining_domains = set(cluster)
# 		next_index = 0
# 		label_prefix = cluster.get_identifier() + '_'
# 		list_of_clusters = list()

# 		try:
# 			database_instance = DatabaseInterface()
# 		except DatabaseInterface as old_database_instance:
# 			database_instance = old_database_instance

# 		def propagate_domain(remaining_domains):
# 			domains_remaining = set(remaining_domains)
# 			domains_taken = set()
# 			ip_addr_taken = set()
# 			domains_to_propagate = set()
# 			ip_addrs_to_propagate = set()

# 			first_domain = domains_remaining.pop()
# 			domains_to_propagate.add(first_domain)

# 			while len(domains_to_propagate) > 0 or len(ip_addrs_to_propagate) > 0:
# 				if len(domains_to_propagate) > 0:
# 					domain_to_propagate = domains_to_propagate.pop()
# 					domains_taken.add(domain_to_propagate)

# 					for ip_addr in domain_to_propagate.get_ip_mappings():
# 						if ip_addr in ip_addr_taken or ip_addr in ip_addrs_to_propagate:
# 							continue

# 						ip_addrs_to_propagate.add(ip_addr)

# 				if len(ip_addrs_to_propagate) > 0:
# 					ip_addr_to_propagate = ip_addrs_to_propagate.pop()
# 					ip_addr_taken.add(ip_addr_to_propagate)

# 					domains_to_be_removed = set()

# 					for domain in domains_remaining:
# 						if ip_addr_to_propagate in domain.get_ip_mappings():
# 							domains_to_propagate.add(domain)
# 							domains_to_be_removed.add(domain)

# 					domains_remaining.difference_update(domains_to_be_removed)

# 			return domains_taken

# 		while len(remaining_domains) > 0:
# 			list_of_domains = propagate_domain(remaining_domains)
# 			new_cluster = DomainCluster(label_prefix + str(next_index))
# 			new_cluster.add_bulk_domains(list_of_domains)
# 			list_of_clusters.append(new_cluster)
# 			next_index += 1
# 			remaining_domains.difference_update(list_of_domains)

# 		return list_of_clusters
		

########################################
## DBSCAN spectral hierarchical clusterer
########################################

class DBScanSpectralHierarchicalClusterer:
	def __init__(self, epsilon = 0.1, min_support = 25, max_ratio = 0.7):
		self._epsilon = epsilon
		self._min_support = min_support
		self._max_ratio = max_ratio

	def generate_subclusters(self, cluster):
		if len(cluster) < self._min_support:
			return []

		if len(cluster.get_ip_set()) == len(cluster.get_ip_backbone_set()):
			return [cluster]

		spectral_features_extractor = SpectralFeaturesExtractor(cluster, 1)

		try:
			cluster = spectral_features_extractor.compute_features()
		except:
			return [cluster]

		toolbox = DomainClusterToolbox()
		toolbox.normalize_bipartite_graph_spectral_features(cluster, 0)

		touple_list = list()

		for domain in cluster:
			touple_list.append((domain.get_bipartite_graph_feature_set().get_dimension_value(0), domain))

		cluster.clear_bipartite_graph_features()

		touple_list = sorted(touple_list, key = lambda x: x[0])
		clusters_already_created = []

		last_measure = None
		current_cluster = None
		next_identifier = 0

		values = list()

		for elem in touple_list:
			measure = elem[0]
			domain = elem[1]

			if current_cluster == None or math.fabs(measure - last_measure) > self._epsilon:
				if current_cluster != None:
					average = numpy.average(values)
					std_dev = numpy.std(values)
		
					descriptor = BipartiteGraphDescriptor()
					descriptor.set_centroid(average)
					descriptor.set_std_dev(std_dev)
					current_cluster.set_bipartite_graph_descriptor(descriptor)

				next_cluster_identifier = cluster.get_identifier() + "_" + str(next_identifier)
				current_cluster = DomainCluster(next_cluster_identifier)
				next_identifier += 1
				clusters_already_created.append(current_cluster)
				values = list()

			values.append(measure)
			current_cluster.add_domain(domain)
			last_measure = measure

		if current_cluster != None and len(current_cluster) > 0:
			average = numpy.average(values)
			std_dev = numpy.std(values)
			
			descriptor = BipartiteGraphDescriptor()
			descriptor.set_centroid(average)
			descriptor.set_std_dev(std_dev)
			current_cluster.set_bipartite_graph_descriptor(descriptor)

		if len(clusters_already_created) <= 1:
			return clusters_already_created

		resulting_clusters = list()

		for cluster in clusters_already_created:
			resulting_clusters.extend(self.generate_subclusters(cluster))

		def filtering_function(x):
			if len(x.get_ip_set()) / float(len(x)) < self._max_ratio:
				return True
			else:
				return False

		return filter(filtering_function, resulting_clusters)


########################################
## Spectral feature set
########################################

class SpectralFeatureSet:
	def __init__(self, dimensions):
		self._dimensions = dimensions
		self._values = [None for i in range(dimensions)]

	def export_header(self):
		return ', '.join(map(lambda x: 'f' + x, map(str, range(self._dimensions))))

	def export(self):
		return ', '.join(map(str, self._values))

	def set_dimension_value(self, index, value):
		self._values[index] = numpy.longdouble(value)

	def get_dimension_value(self, index):
		if (self._values[index] == None):
			raise Exception('The feature dimension[' + str(i) + '] was not set.')

		return self._values[index]


########################################
## Spectral features extractor
########################################

class SpectralFeaturesExtractor:
	def __init__(self, cluster, dimensions):
		self._cluster = cluster
		self._dimensions = dimensions

	def compute_features(self):
		sparse_matrix = self._generate_sparse_matrix()
		(reduced_matrix, s_matrix) = self._compute_reduced_matrix(sparse_matrix)

		###########################
		# FIXME

		# for i in range(s_matrix.shape[0]):
		# 	for j in range(s_matrix.shape[1]):
		# 		if s_matrix[i, j] > 0:
		# 			s_matrix[i, j] = 1

		# if len(self._cluster) > 4600:
		# 	try:
		# 		G = nx.from_scipy_sparse_matrix(s_matrix)
		# 		pos = nx.spring_layout(G, scale = 1)
		# 		nx.draw_networkx_nodes(G, pos, node_size = 10, node_color = 'w')
		# 		#nx.draw_networkx_edges(G, pos, width = 0.1, alpha = 0.5)
		# 		plt.axis('off')
		# 		plt.savefig(self._cluster.get_identifier())
		# 		print 'Export!', self._cluster.get_identifier(), str(len(self._cluster))
		# 	except Exception as e:
		# 		print str(e)
		# 		return
		###########################

		###########################
		# FIXME

		# if len(self._cluster) > 600:
		# 	print 'graph'
		# 	print '['
		# 	print '    directed 0'

		# 	for i in range(s_matrix.shape[0]):
		# 		print '    node'
		# 		print '    ['
		# 		print '        id ' + str(i)
		# 		print '        label "' + str(i) + '"'
		# 		print '    ]'

		# 	for i in range(s_matrix.shape[0]):
		# 		for j in range(s_matrix.shape[1])[i+1:]:
		# 			if s_matrix[i, j] > 0:
		# 				print '    edge'
		# 				print '    ['
		# 				print '        source ' + str(i)
		# 				print '        target ' + str(j)
		# 				print '    ]'
		# 	print ']'
		###########################

		i = 0
		for domain in self._cluster:
			feature_set = SpectralFeatureSet(self._dimensions)

			for j in range(self._dimensions):
				value = reduced_matrix[j][i]
				feature_set.set_dimension_value(j, numpy.real(value))
			i = i + 1

			domain.set_bipartite_graph_feature_set(feature_set)

		return self._cluster

	def _generate_sparse_matrix(self):
		ip_dict = dict()
		domains_list = list()

		for domain in self._cluster:
			domains_list.append(domain)

			for ip in domain.get_ip_mappings():
				if ip in ip_dict:
					ip_dict[ip] = (ip_dict[ip][0], ip_dict[ip][1] + 1)
				else:
					ip_dict[ip] = (len(ip_dict), 1)

		columns = len(domains_list)
		rows = len(ip_dict)

		matrix = lil_matrix((rows, columns))

		i = 0
		for domain in self._cluster:
			cumulative = 0
			for ip in domain.get_ip_mappings():
				cumulative = cumulative + 1 / float(ip_dict[ip][1])

			for ip in domain.get_ip_mappings():
				matrix[ip_dict[ip][0], i] = 1 / float(ip_dict[ip][1]) / cumulative
			i = i + 1

		return matrix

	def _compute_reduced_matrix(self, matrix):
		s_matrix = csc_matrix(matrix).transpose().dot(dok_matrix(matrix))
		eigen_values = eigs(s_matrix, self._dimensions)

		result = eigen_values[1].transpose()
		#row_mean = result.mean(axis = 1)
		#new_result = (result / row_mean[:, numpy.newaxis])

		return result, s_matrix