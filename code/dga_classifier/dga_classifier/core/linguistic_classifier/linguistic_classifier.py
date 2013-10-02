from dga_classifier.core.linguistic_classifier.linguistic_features_extractors import MeaningfulWordsExtractor
from dga_classifier.core.linguistic_classifier.linguistic_features_extractors import NumericalCharactersExtractor
#from dga_classifier.core.linguistic_classifier.linguistic_features_extractors import VowelCharactersExtractor
#from dga_classifier.core.linguistic_classifier.linguistic_features_extractors import DashCharactersExtractor
from dga_classifier.core.linguistic_classifier.linguistic_features_extractors import CharacterSetExtractor
#from dga_classifier.core.linguistic_classifier.linguistic_features_extractors import CharacterDigitTransitionsExtractor
from dga_classifier.core.linguistic_classifier.linguistic_features_extractors import NGramNormalityExtractor
from dga_classifier.core.clustering.cluster import DomainClusterFileFactory
from dga_classifier.core.helper import jsontools
from scipy.spatial.distance import mahalanobis
import scipy
import numpy


########################################
## Feature set
########################################

class FeatureSet:
	def __init__(self):
		self._meaningful_word_ratio = None
		self._numerical_characters_ratio = None
		# self._vowel_characters_ratio = None
		# self._dash_characters_ratio = None
		self._character_set = None
		# self._character_digit_transitions_ratio = None
		self._one_gram_normality_score = None
		self._two_gram_normality_score = None
		self._three_gram_normality_score = None
		self._DGA_label = None

	def export_header(self):
		# return 'meaningful_word_ratio, numerical_characters_ratio, vowel_characters_ratio, dash_characters_ratio, character_set, character_digit_transitions_ratio, one_gram_normality_score, two_gram_normality_score, three_gram_normality_score'
		return 'meaningful_word_ratio, numerical_characters_ratio, one_gram_normality_score, two_gram_normality_score, three_gram_normality_score, DGA_label'

	def __str__(self):
		string = ''
		string += str(self.get_meaningful_word_ratio())
		string += ', '
		#string += str(self.get_numerical_characters_ratio())
		#string += ', '
		# string += str(self.get_vowel_characters_ratio())
		# string += ', '
		# string += str(self.get_dash_characters_ratio())
		# string += ', '
		#string += str(self.get_character_set())
		#string += ', '
		# string += str(self.get_character_digit_transitions_ratio())
		# string += ', '
		string += str(self.get_one_gram_normality_score())
		string += ', '
		string += str(self.get_two_gram_normality_score())
		string += ', '
		string += str(self.get_three_gram_normality_score())
		string += ', '
		string += str(self.get_DGA_label())

		return string

	def set_meaningful_word_ratio(self, feature):
		self._meaningful_word_ratio = feature

	def get_meaningful_word_ratio(self):
		if self._meaningful_word_ratio == None:
			raise Exception('The feature meaningful_word_ratio was not set.')

		return self._meaningful_word_ratio

	def set_numerical_characters_ratio(self, feature):
		self._numerical_characters_ratio = feature

	def get_numerical_characters_ratio(self):
		if (self._numerical_characters_ratio == None):
			raise Exception('The feature numerical_characters_ratio was not set.')

		return self._numerical_characters_ratio

	# def set_vowel_characters_ratio(self, feature):
	# 	self._vowel_characters_ratio = feature

	# def get_vowel_characters_ratio(self):
	# 	if (self._vowel_characters_ratio == None):
	# 		raise Exception('The feature vowel_characters_ratio was not set.')

	# 	return self._vowel_characters_ratio

	# def set_dash_characters_ratio(self, feature):
	# 	self._dash_characters_ratio = feature

	# def get_dash_characters_ratio(self):
	# 	if (self._dash_characters_ratio == None):
	# 		raise Exception('The feature dash_characters_ratio was not set.')

	# 	return self._dash_characters_ratio

	def set_character_set(self, feature):
		self._character_set = feature

	def get_character_set(self):
		if (self._character_set == None):
			raise Exception('The feature character_set was not set.')

		return self._character_set

	# def set_character_digit_transitions_ratio(self, feature):
	# 	self._character_digit_transitions_ratio = feature

	# def get_character_digit_transitions_ratio(self):
	# 	if (self._character_digit_transitions_ratio == None):
	# 		raise Exception('The feature character_digit_transitions_ratio was not set.')

	# 	return self._character_digit_transitions_ratio

	def set_one_gram_normality_score(self, feature):
		self._one_gram_normality_score = feature

	def get_one_gram_normality_score(self):
		if self._one_gram_normality_score == None:
			raise Exception('The feature one_gram_normality_score was not set.')

		return self._one_gram_normality_score

	def set_two_gram_normality_score(self, feature):
		self._two_gram_normality_score = feature

	def get_two_gram_normality_score(self):
		if self._two_gram_normality_score == None:
			raise Exception('The feature two_gram_normality_score was not set.')

		return self._two_gram_normality_score

	def set_three_gram_normality_score(self, feature):
		self._three_gram_normality_score = feature

	def get_three_gram_normality_score(self):
		if self._three_gram_normality_score == None:
			raise Exception('The feature three_gram_normality_score was not set.')

		return self._three_gram_normality_score

	def set_DGA_label(self, label):
		self._DGA_label = label

	def get_DGA_label(self):
		if self._DGA_label == None:
			return 'unknown'

		return self._DGA_label;


########################################
## Features extractor
########################################

class FeaturesExtractor:
	def __init__(self, domain):
		self._domain = domain

	def compute_feature_set(self):
		features_set = FeatureSet()

		features_set.set_meaningful_word_ratio(MeaningfulWordsExtractor(self._domain).meaningful_words_ratio())
		features_set.set_numerical_characters_ratio(NumericalCharactersExtractor(self._domain).characters_ratio())
		# features_set.set_vowel_characters_ratio(VowelCharactersExtractor(self._domain).characters_ratio())
		# features_set.set_dash_characters_ratio(DashCharactersExtractor(self._domain).characters_ratio())
		features_set.set_character_set(CharacterSetExtractor(self._domain).set())
		# features_set.set_character_digit_transitions_ratio(CharacterDigitTransitionsExtractor(self._domain).transitions_ratio())

		n_gram_normality_extractor = NGramNormalityExtractor(self._domain)

		features_set.set_one_gram_normality_score(n_gram_normality_extractor.normality_score(1))
		features_set.set_two_gram_normality_score(n_gram_normality_extractor.normality_score(2))
		features_set.set_three_gram_normality_score(n_gram_normality_extractor.normality_score(3))

		return features_set


########################################
## Classifier
########################################

class DGAClassifier:
	def __init__(self, domain):
		self._domain = domain

	def classify(self, strict = True):
		features_extractor = FeaturesExtractor(self._domain)
		feature_set = features_extractor.compute_feature_set()

		# meaningful_words_ratio = feature_set.get_meaningful_word_ratio()
		# one_gram_normality_score = feature_set.get_one_gram_normality_score()
		# two_gram_normality_score = feature_set.get_two_gram_normality_score()
		# three_gram_normality_score = feature_set.get_three_gram_normality_score()

		self._domain.set_linguistic_feature_set(feature_set)

		try:
			linguistic_normality = LinguisticNormality()
		except LinguisticNormality as linguistic_normality_instance:
			linguistic_normality = linguistic_normality_instance

		if linguistic_normality.compute_distance(self._domain) < linguistic_normality.get_threshold(strict):
			label = 'non-DGA'
		else:
			label = 'DGA'

		feature_set.set_DGA_label(label)

		print jsontools.domain_feature_set_to_json(self._domain, feature_set)


########################################
## Linguistic normality
########################################

class LinguisticNormality:
	__instance = None

	def __init__(self):
		if LinguisticNormality.__instance:
			raise LinguisticNormality.__instance

		LinguisticNormality.__instance = self

		cluster_factory = DomainClusterFileFactory('dga_classifier/assets/alexa100.txt', False)
		normal_cluster = cluster_factory.get('cluster_0')

		meaningful_word_ratio_list = list()
		one_gram_normality_score_list = list()
		two_gram_normality_score_list = list()
		three_gram_normality_score_list = list()

		for domain in normal_cluster:
			features_extractor = FeaturesExtractor(domain)
			feature_set = features_extractor.compute_feature_set()

			meaningful_word_ratio_list.append(feature_set.get_meaningful_word_ratio())
			one_gram_normality_score_list.append(feature_set.get_one_gram_normality_score())
			two_gram_normality_score_list.append(feature_set.get_two_gram_normality_score())
			three_gram_normality_score_list.append(feature_set.get_three_gram_normality_score())

		samples = numpy.array([meaningful_word_ratio_list, one_gram_normality_score_list, two_gram_normality_score_list, three_gram_normality_score_list])
		cov_matrix = numpy.cov(samples)

		self._cov_inv = numpy.linalg.inv(cov_matrix)
		self._centroid = numpy.array([numpy.average(meaningful_word_ratio_list), numpy.average(one_gram_normality_score_list), numpy.average(two_gram_normality_score_list), numpy.average(three_gram_normality_score_list)])

	def compute_distance(self, domain):
		meaningful_word_ratio = domain.get_linguistic_feature_set().get_meaningful_word_ratio()
		one_gram_normality_score = domain.get_linguistic_feature_set().get_one_gram_normality_score()
		two_gram_normality_score = domain.get_linguistic_feature_set().get_two_gram_normality_score()
		three_gram_normality_score = domain.get_linguistic_feature_set().get_three_gram_normality_score()

		current_sample = numpy.array([meaningful_word_ratio, one_gram_normality_score, two_gram_normality_score, three_gram_normality_score])

		for i in range(len(current_sample)):
			if self._centroid[i] < current_sample[i]:
				current_sample[i] = self._centroid[i]

		distance = mahalanobis(current_sample, self._centroid, self._cov_inv)

		return distance

	def get_threshold(self, strict = True):
		if strict:
			return 1.98
		else:
			return 1.35