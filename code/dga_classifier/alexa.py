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

	try:
		linguistic_normality = LinguisticNormality()
	except LinguisticNormality as linguistic_normality_instance:
		linguistic_normality = linguistic_normality_instance

	for domain in cluster:
		features_extractor = FeaturesExtractor(domain)
		feature_set = features_extractor.compute_feature_set()
		domain.set_linguistic_feature_set(feature_set)

		distance = linguistic_normality.compute_distance(domain)

		if distance > linguistic_normality.get_threshold(strict=True):
			label = 'AGD'
		elif distance > linguistic_normality.get_threshold(strict=False):
			label = 'semi-AGD'
		else:
			label = 'HGD'

		print domain,\
			feature_set.get_meaningful_word_ratio(),\
			feature_set.get_one_gram_normality_score(),\
			feature_set.get_two_gram_normality_score(),\
			feature_set.get_three_gram_normality_score(),\
			label


if __name__ == '__main__':
	sys.exit(main(sys.argv))