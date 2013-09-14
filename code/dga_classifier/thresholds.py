import sys
from dga_classifier.core.linguistic_classifier.linguistic_classifier import FeaturesExtractor
from dga_classifier.core.linguistic_classifier.linguistic_classifier import LinguisticNormality
from dga_classifier.core.clustering.cluster import DomainClusterFileFactory


########################################
## Main method
########################################

def main(argv):
	# Inport all domains
	cluster_factory = DomainClusterFileFactory('dga_classifier/assets/alexa100.txt', False)
	cluster = cluster_factory.get('cluster_0')	

	# Computer features
	for domain in cluster:
		features_extractor = FeaturesExtractor(domain)
		feature_set = features_extractor.compute_feature_set()

		domain.set_linguistic_feature_set(feature_set)

	try:
		linguistic_normality = LinguisticNormality()
	except LinguisticNormality as linguistic_normality_instance:
		linguistic_normality = linguistic_normality_instance

	for i in range(1000):
		max_distance = i * 0.1
		false_positives = 0

		for domain in cluster:
			distance = linguistic_normality.compute_distance(domain)

			if distance > max_distance:
				false_positives = false_positives + 1

		print max_distance, false_positives / float(len(cluster))

	# values = []

	# for domain in cluster:
	# 	distance = linguistic_normality.compute_distance(domain)
	# 	values.append(distance)

	# values = sorted(values)

	# print ';\n'.join(map(str, values))

if __name__ == '__main__':
	sys.exit(main(sys.argv))