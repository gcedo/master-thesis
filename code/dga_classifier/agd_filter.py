import sys
from scipy.stats import ks_2samp
from dga_classifier.core.linguistic_classifier.linguistic_classifier import FeaturesExtractor
from dga_classifier.core.linguistic_classifier.linguistic_classifier import LinguisticNormality
from dga_classifier.core.clustering.cluster import DomainClusterFileFactory


########################################
## Main method
########################################

def main(argv):
	try:
		linguistic_normality = LinguisticNormality()
	except LinguisticNormality as linguistic_normality_instance:
		linguistic_normality = linguistic_normality_instance

	# alexa_cluster_factory = DomainClusterFileFactory('dga_classifier/assets/alexa100.txt', False)
	# alexa_cluster = alexa_cluster_factory.get('cluster_0')
	# alexa_cluster.set_identifier('alexa')
	# alexa_values = []

	# for domain in alexa_cluster:
	# 	features_extractor = FeaturesExtractor(domain)
	# 	feature_set = features_extractor.compute_feature_set()
	# 	domain.set_linguistic_feature_set(feature_set)

	# 	value = linguistic_normality.compute_distance(domain)
	# 	alexa_values.append(value)

	sources = ['alexa100', 'torpig', 'bamital', 'conficker.a', 'conficker.b', 'conficker.c']

	for source1 in sources:
		cluster_factory1 = DomainClusterFileFactory('dga_classifier/assets/' + source1 + '.txt', False)
		cluster1 = cluster_factory1.get('cluster_0')
		cluster1_values = []

		for domain1 in cluster1:
			features_extractor = FeaturesExtractor(domain1)
			feature_set = features_extractor.compute_feature_set()
			domain1.set_linguistic_feature_set(feature_set)

			value = linguistic_normality.compute_distance(domain1)
			cluster1_values.append(value)

		for source2 in sources:
			cluster_factory2 = DomainClusterFileFactory('dga_classifier/assets/' + source2 + '.txt', False)
			cluster2 = cluster_factory2.get('cluster_0')
			cluster2_values = []

			for domain2 in cluster2:
				features_extractor = FeaturesExtractor(domain2)
				feature_set = features_extractor.compute_feature_set()
				domain2.set_linguistic_feature_set(feature_set)

				value = linguistic_normality.compute_distance(domain2)
				cluster2_values.append(value)

			(_, pvalue) = ks_2samp(cluster1_values, cluster2_values)
			print 'Testing', source1, source2, pvalue

	# print 'distance, ' + ', '.join(sources) 

	# for i in range(1000):
	# 	max_distance = i * 0.01

	# 	string = str(max_distance)

	# 	for cluster in clusters:
	# 		out = len(filter(lambda x : x >= max_distance, distances[cluster.get_identifier()]))
	# 		tot = len(distances[cluster.get_identifier()])
	# 		string = string + ', ' + str(out / float(tot))

	# 	print string


if __name__ == '__main__':
	sys.exit(main(sys.argv))