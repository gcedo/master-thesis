from dga_classifier.core.helper.tools import Dictionary
import re
import math


def get_n_grams(n, string):
	if len(string) < n:
		return []

	result = list()

	for i in range(0, len(string) + 1 - n):
		n_gram = string[i:i + n]
		result.append(n_gram)

	return result


########################################
## Meaningful words
########################################

class MeaningfulWordsExtractor:
	def __init__(self, domain):
		self._str_domain_name = domain.get_domain_name().get_flatten_chosen_prefix().replace('-', '')
		
		try:
			self._dictionary = Dictionary()
		except Dictionary as dictionary_instance:
			self._dictionary = dictionary_instance

	def _longest_word_in_string(self, string, min_length = 3):
		string_len = len(string)

		if string_len < min_length:
			return None

		for current_len in range(min_length, string_len + 1)[ : :-1]:
			for current_start in range(0, string_len - current_len + 1):
				string_to_try = string[current_start:current_start + current_len]

				if self._dictionary.is_word(string_to_try):
					return string_to_try

		return None

	def meaningful_words_length(self):
		remaining_string = self._str_domain_name
		count = 0;

		while True:
			longest_word = self._longest_word_in_string(remaining_string)

			if longest_word == None:
				break

			remaining_string = remaining_string.replace(longest_word, '%', 1)
			count = count + len(longest_word)

		return count

	def meaningful_words_ratio(self):
		return self.meaningful_words_length() / float(len(self._str_domain_name))


#######################################
# Numerical characters
#######################################

class NumericalCharactersExtractor:
	def __init__(self, domain):
		self._str_domain_name = domain.get_domain_name().get_flatten_chosen_prefix()

	def characters_number(self):
		regex = re.compile(r'[^0-9]+')
		filtered_str_domain_name = regex.sub('', self._str_domain_name)

		return len(filtered_str_domain_name)

	def characters_ratio(self):
		return self.characters_number() / float(len(self._str_domain_name))


########################################
## Vowel characters
########################################

# class VowelCharactersExtractor:
# 	def __init__(self, domain):
# 		self._str_domain_name = domain.get_domain_name().get_flatten_chosen_prefix()

# 	def characters_number(self):
# 		regex = re.compile(r'[^aeiou]+')
# 		filtered_str_domain_name = regex.sub('', self._str_domain_name)

# 		return len(filtered_str_domain_name)

# 	def characters_ratio(self):
# 		return self.characters_number() / float(len(self._str_domain_name))


########################################
## Dash characters
########################################

# class DashCharactersExtractor:
# 	def __init__(self, domain):
# 		self._str_domain_name = domain.get_domain_name().get_flatten_chosen_prefix()

# 	def characters_number(self):
# 		regex = re.compile(r'[^-]+')
# 		filtered_str_domain_name = regex.sub('', self._str_domain_name)

# 		return len(filtered_str_domain_name)

# 	def characters_ratio(self):
# 		return self.characters_number() / float(len(self._str_domain_name))


#######################################
# Character set
#######################################

class CharacterSetExtractor:
	def __init__(self, domain):
		self._str_domain_name = domain.get_domain_name().get_flatten_chosen_prefix()

	def set(self):
		result_set = set()

		for char in self._str_domain_name:
			result_set.add(char)

		return result_set

	# def set_size(self):
	# 	return len(self.set())

	# def set_ratio(self):
	# 	return self.set_size() / float(len(self._str_domain_name))


########################################
## Character-digit transitions
########################################

# class CharacterDigitTransitionsExtractor:
# 	def __init__(self, domain):
# 		self._str_domain_name = domain.get_domain_name().get_flatten_chosen_prefix().replace('-', '')

# 	def transitions_number(self):
# 		count = 0
# 		is_last_digit = self._str_domain_name[0].isdigit()

# 		for char in self._str_domain_name:
# 			is_this_digit = char.isdigit()

# 			if is_this_digit != is_last_digit:
# 				count = count + 1
# 				is_last_digit = is_this_digit

# 		return count

# 	def transitions_ratio(self):
# 		return self.transitions_number() / float(len(self._str_domain_name) - 1)


########################################
## N-gram normality
########################################

class NGramNormalityExtractor:
	def __init__(self, domain):
		self._str_domain_name = domain.get_domain_name().get_flatten_chosen_prefix().replace('-', '')

	def normality_score(self, n):
		score_accumulator = 0;
		count = 0

		try:
			dictionary = Dictionary()
		except Dictionary as dictionary_instance:
			dictionary = dictionary_instance

		for n_gram in get_n_grams(n, self._str_domain_name):
			if n == 1:
				current_count = dictionary.one_gram_count(n_gram)
			elif n == 2:
				current_count = dictionary.two_gram_count(n_gram)
			elif n == 3:
				current_count = dictionary.three_gram_count(n_gram)
			else:
				raise Exception('In NGramAnomalyExtractor n should be 1, 2 or 3')

			score_accumulator = score_accumulator + current_count
			count = count + 1

		if count == 0:
			return 0

		return score_accumulator / float(count)