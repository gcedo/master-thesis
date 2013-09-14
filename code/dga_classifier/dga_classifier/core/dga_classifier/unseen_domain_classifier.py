from dga_classifier.core.linguistic_classifier.linguistic_classifier import DGAClassifier
from dga_classifier.core.database.database import DatabaseInterface
from termcolor import colored


########################################
## Unseen domain classification
########################################

class UnseenDomainClassification:
	def __init__(self, seen_before, is_dga, classification = None):
		self._seen_before = seen_before
		self._is_dga = is_dga
		self._classification = classification

	def is_dga(self):
		return self._is_dga

	def is_seen_before(self):
		return self._seen_before

	def is_known_classification(self):
		if self._classification == None:
			return False
		else:
			return True

	def __str__(self):
		result = ''

		if self._seen_before:
			result += colored('seen_before', 'cyan')
		else:
			result += colored('never_seen', 'blue')

		if self._is_dga:
			result += ' ' + colored('DGA', 'red')

			if self._classification == None:
				result += ' ' + colored('unknown', 'yellow')
			else:
				result += ' ' + colored(self._classification, 'red')
		else:
			result += ' ' + colored('non-DGA', 'green')

		return result


########################################
## Unseen domain classifier
########################################

class UnseenDomainClassifier:
	def __init__(self, domain, dga_clusters, quiet = True):
		self._domain = domain
		self._dga_clusters = dga_clusters
		self._quiet = quiet

	def get_classification(self):
		DGA_classifier = DGAClassifier(self._domain)
		DGA_classifier.classify(strict = False)
		seen_before = self._seen_before()

		if self._domain.get_linguistic_feature_set().get_DGA_label() == 'non-DGA':
			return UnseenDomainClassification(seen_before, False)

		candidate_clusters = set()

		for cluster in self._dga_clusters:
			if len(set(self._domain.get_ip_mappings()).intersection(cluster.get_ip_set())) > 0:
				candidate_clusters.add(cluster)

		candidate_clusters = filter(self._linguistic_fit, candidate_clusters)

		if len(candidate_clusters) > 0:
			return UnseenDomainClassification(seen_before, True, '/'.join(map(lambda x : x.get_identifier(), list(candidate_clusters))))

		return UnseenDomainClassification(seen_before, True)

	def _seen_before(self):
		try:
			database_instance = DatabaseInterface()
		except DatabaseInterface as old_database_instance:
			database_instance = old_database_instance

		return database_instance.was_domain_seen_in_training(self._domain)

	def _linguistic_fit(self, cluster):
		cluster_descriptor = cluster.get_linguistic_descriptor()
		domain_feature_set = self._domain.get_linguistic_feature_set()

		# Length
		if len(self._domain.get_domain_name().get_chosen_prefix()) < cluster_descriptor.get_length_interval()[0] \
			or len(self._domain.get_domain_name().get_chosen_prefix()) > cluster_descriptor.get_length_interval()[1]:
			if self._quiet == False:
				print self._domain, 'length'
			return False

		# Character set
		char_set = domain_feature_set.get_character_set()

		if len(char_set.intersection(cluster_descriptor.get_character_set())) != len(char_set):
			if self._quiet == False:
				print self._domain, 'char_set'
			return False

		# Numerical characters ratio
		numerical_characters_ratio = domain_feature_set.get_numerical_characters_ratio()

		if numerical_characters_ratio < cluster_descriptor.get_numerical_characters_ratio_interval()[0] \
			or numerical_characters_ratio > cluster_descriptor.get_numerical_characters_ratio_interval()[1]:
			if self._quiet == False:
				print self._domain, 'numerical characters ratio'
			return False		

		# Publix suffix
		if self._domain.get_domain_name().get_public_suffix() not in cluster_descriptor.get_public_suffix_set():
			if self._quiet == False:
				print self._domain, 'public suffix'
			return False

		# Meaningful word ratio
		meaningful_word_ratio = domain_feature_set.get_meaningful_word_ratio()

		if meaningful_word_ratio < cluster_descriptor.get_meaningful_word_ratio_interval()[0] \
			or meaningful_word_ratio > cluster_descriptor.get_meaningful_word_ratio_interval()[1]:
			if self._quiet == False:
				print self._domain, 'meaningful_word_ratio'
			#return False

		# One gram normality score
		one_gram_normality_score = domain_feature_set.get_one_gram_normality_score()

		if one_gram_normality_score < cluster_descriptor.get_one_gram_normality_score_interval()[0] \
			or one_gram_normality_score > cluster_descriptor.get_one_gram_normality_score_interval()[1]:
			if self._quiet == False:
				print self._domain, 'one_gram_normality_score'
			#return False

		# Two gram normality score
		two_gram_normality_score = domain_feature_set.get_two_gram_normality_score()

		if two_gram_normality_score < cluster_descriptor.get_two_gram_normality_score_interval()[0] \
			or two_gram_normality_score > cluster_descriptor.get_two_gram_normality_score_interval()[1]:
			if self._quiet == False:
				print self._domain, 'two_gram_normality_score'
			#return False

		# Three gram normality score
		three_gram_normality_score = domain_feature_set.get_three_gram_normality_score()

		if three_gram_normality_score < cluster_descriptor.get_three_gram_normality_score_interval()[0] \
			or three_gram_normality_score > cluster_descriptor.get_three_gram_normality_score_interval()[1]:
			if self._quiet == False:
				print self._domain, 'three_gram_normality_score'
			#return False

		return True