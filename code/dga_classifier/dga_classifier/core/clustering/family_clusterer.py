from dga_classifier.core.clustering.cluster import DomainCluster
from dga_classifier.core.clustering.cluster import DomainClusterToolbox
from dga_classifier.core.clustering.bipartite_graph_clustering import DBScanSpectralHierarchicalClusterer
from dga_classifier.core.clustering.postprocessing import PostProcessor
from dga_classifier.core.linguistic_classifier.linguistic_classifier import DGAClassifier
from dga_classifier.core.clustering.cluster_descriptor import LinguisticDescriptorExtractor
import md5


########################################
## FamilyClusterer
########################################

class FamilyClusterer:
	def __init__(self, cluster):
		self._malicious_cluster = cluster

	def compute_clusters(self, merge = True, min_support = None, max_ratio = None):
		DGAs = list()

		# Filter DGA malicious domains
		for domain in self._malicious_cluster:
			DGA_classifier = DGAClassifier(domain)
			DGA_classifier.classify(strict = True)

			if domain.get_linguistic_feature_set().get_DGA_label() == 'DGA':
				DGAs.append(domain)

		# Create DGA cluster and split
		DGA_cluster = DomainCluster('DGA_cluster')
		DGA_cluster.add_bulk_domains(DGAs)

		toolbox = DomainClusterToolbox()
		list_of_DGA_clusters = toolbox.split(DGA_cluster, 200000) #FIXME 20000

		# DGA families clustering
		if min_support == None and max_ratio == None:
			dbscan_clusterer = DBScanSpectralHierarchicalClusterer()
		elif min_support != None and max_ratio != None:
			dbscan_clusterer = DBScanSpectralHierarchicalClusterer(min_support=min_support, max_ratio=max_ratio)
		elif min_support != None:
			dbscan_clusterer = DBScanSpectralHierarchicalClusterer(min_support=min_support)
		elif max_ratio != None:
			dbscan_clusterer = DBScanSpectralHierarchicalClusterer(max_ratio=max_ratio)


		list_of_subclusters = list()

		for cluster in list_of_DGA_clusters:
			list_of_subclusters.extend(dbscan_clusterer.generate_subclusters(cluster))

		# Post processing
		postprocessor = PostProcessor()
		list_of_list_of_subclusters = postprocessor.postprocess(list_of_subclusters)

		if merge:
			postprocessed_subclusters = list()

			for list_of_clusters in list_of_list_of_subclusters:
				m = md5.new()
				m.update('.'.join(map(lambda x : x.get_identifier(), list_of_clusters)))
				postprocessed_subclusters.append(toolbox.merge(list_of_clusters, m.hexdigest()[:5]))

			for subcluster in postprocessed_subclusters:
				linguistic_descriptor_extractor = LinguisticDescriptorExtractor(subcluster)
				linguistic_descriptor_extractor.compute_features()

			return postprocessed_subclusters
		else:
			return list_of_list_of_subclusters