from dga_classifier.core.helper.tools import colored_label
import numpy


########################################
## Bipartite graph descriptor
########################################

class BipartiteGraphDescriptor:
	def __init__(self):
		self._centroid = None
		self._std_dev = None

	def set_centroid(self, feature):
		self._centroid = feature

	def get_centroid(self):
		if self._centroid == None:
			raise Exception('The centroid is not set.')

		return self._centroid

	def set_std_dev(self, feature):
		self._std_dev = feature

	def get_std_dev(self):
		if self._std_dev == None:
			raise Exception('The standard deviation is not set.')

		return self._std_dev

	def __str__(self):
		result = colored_label('Bipartite graph centroid: ') + str(self.get_centroid()) + '\n'
		result += colored_label('Bipartite graph standard deviation: ') + str(self.get_std_dev())

		return result


########################################
## LinguisticDescriptor
########################################

class LinguisticDescriptor:
	def __init__(self):
		self._length_interval = None
		self._character_set = None
		self._numerical_characters_ratio_interval = None
		self._public_suffix_set = None
		self._meaningful_word_ratio_interval = None
		self._one_gram_normality_score_interval = None
		self._two_gram_normality_score_interval = None
		self._three_gram_normality_score_interval = None

	def set_length_interval(self, interval):
		self._length_interval = interval

	def get_length_interval(self):
		if self._length_interval == None:
			raise Exception('The length interval is not set.')

		return self._length_interval

	def set_character_set(self, char_set):
		self._character_set = char_set

	def get_character_set(self):
		if self._character_set == None:
			raise Exception('The character set is not set.')

		return self._character_set

	def set_numerical_characters_ratio_interval(self, interval):
		self._numerical_characters_ratio_interval = interval

	def get_numerical_characters_ratio_interval(self):
		if self._numerical_characters_ratio_interval == None:
			raise Exception('The numerical characters ratio interval is not set.')

		return self._numerical_characters_ratio_interval

	def set_public_suffix_set(self, suffix_set):
		self._public_suffix_set = suffix_set

	def get_public_suffix_set(self):
		if self._public_suffix_set == None:
			raise Exception('The pubblic suffix set is not set.')

		return self._public_suffix_set

	def set_meaningful_word_ratio_interval(self, interval):
		self._meaningful_word_ratio_interval = interval

	def get_meaningful_word_ratio_interval(self):
		if self._meaningful_word_ratio_interval == None:
			raise Exception('The meaningful word ratio interval was not set.')

		return self._meaningful_word_ratio_interval

	def set_one_gram_normality_score_interval(self, interval):
		self._one_gram_normality_score_interval = interval

	def get_one_gram_normality_score_interval(self):
		if self._one_gram_normality_score_interval == None:
			raise Exception('The one gram normality score interval was not set.')

		return self._one_gram_normality_score_interval

	def set_two_gram_normality_score_interval(self, interval):
		self._two_gram_normality_score_interval = interval

	def get_two_gram_normality_score_interval(self):
		if self._two_gram_normality_score_interval == None:
			raise Exception('The two gram normality score interval was not set.')

		return self._two_gram_normality_score_interval

	def set_three_gram_normality_score_interval(self, interval):
		self._three_gram_normality_score_interval = interval

	def get_three_gram_normality_score_interval(self):
		if self._three_gram_normality_score_interval == None:
			raise Exception('The three gram normality score interval was not set.')

		return self._three_gram_normality_score_interval

	def __str__(self):
		result = colored_label('Length: ') + str(self.get_length_interval()) + '\n'
		result += colored_label('Character set len: ') + str(len(self.get_character_set())) + '\n'
		result += colored_label('Numerical characters ratio: ') + str(self.get_numerical_characters_ratio_interval()) + '\n'
		result += colored_label('Public suffixes: ') + str(self.get_public_suffix_set()) + '\n'
		result += colored_label('Meaningful word ratio: ') + str(self.get_meaningful_word_ratio_interval()) + '\n'
		result += colored_label('One gram normality score: ') + str(self.get_one_gram_normality_score_interval()) + '\n'
		result += colored_label('Two gram normality score: ') + str(self.get_two_gram_normality_score_interval()) + '\n'
		result += colored_label('Three gram normality score: ') + str(self.get_three_gram_normality_score_interval())
		
		return result


########################################
## Linguistic descriptor extractor
########################################

class LinguisticDescriptorExtractor:
	def __init__(self, cluster):
		self._cluster = cluster

	def compute_features(self):
		linguistic_descriptor = LinguisticDescriptor()
		linguistic_descriptor.set_length_interval(self._compute_length_interval())
		linguistic_descriptor.set_character_set(self._compute_character_set())
		linguistic_descriptor.set_numerical_characters_ratio_interval(self._compute_numerical_characters_ratio_interval())
		linguistic_descriptor.set_public_suffix_set(self._compute_pubblic_suffix_set())
		linguistic_descriptor.set_meaningful_word_ratio_interval(self._compute_meaning_word_ratio_interval())
		linguistic_descriptor.set_one_gram_normality_score_interval(self._compute_one_gram_normality_score())
		linguistic_descriptor.set_two_gram_normality_score_interval(self._compute_two_gram_normality_score())
		linguistic_descriptor.set_three_gram_normality_score_interval(self._compute_three_gram_normality_score())

		self._cluster.set_linguistic_descriptor(linguistic_descriptor)
		return self._cluster

	def _compute_length_interval(self):
		values = list()

		for domain in self._cluster:
			value = len(domain.get_domain_name().get_chosen_prefix())
			values.append(value)

		return (min(values), max(values))

	def _compute_character_set(self):
		char_set = set()

		for domain in self._cluster:
			char_set = char_set.union(domain.get_linguistic_feature_set().get_character_set())

		return char_set

	def _compute_numerical_characters_ratio_interval(self):
		values = list()

		for domain in self._cluster:
			value = domain.get_linguistic_feature_set().get_numerical_characters_ratio()
			values.append(value)

		return (min(values), max(values))

	def _compute_pubblic_suffix_set(self):
		suffix_set = set()

		for domain in self._cluster:
			suffix_set.add(domain.get_domain_name().get_public_suffix())

		return suffix_set

	def _compute_meaning_word_ratio_interval(self):
		values = list()

		for domain in self._cluster:
			value = domain.get_linguistic_feature_set().get_meaningful_word_ratio()
			values.append(value)

		return (min(values), max(values))

	def _compute_one_gram_normality_score(self):
		values = list()

		for domain in self._cluster:
			value = domain.get_linguistic_feature_set().get_one_gram_normality_score()
			values.append(value)

		return (min(values), max(values))

	def _compute_two_gram_normality_score(self):
		values = list()

		for domain in self._cluster:
			value = domain.get_linguistic_feature_set().get_two_gram_normality_score()
			values.append(value)

		return (min(values), max(values))

	def _compute_three_gram_normality_score(self):
		values = list()

		for domain in self._cluster:
			value = domain.get_linguistic_feature_set().get_three_gram_normality_score()
			values.append(value)

		return (min(values), max(values))