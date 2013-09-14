from dga_classifier.core.helper.publicsuffix import PublicSuffixList
from dga_classifier.core.database.database import DatabaseInterface
from dga_classifier.core.helper.tools import clean_string
import string


def flatten_domain_name_string(domain_name_string):
	return domain_name_string.replace('.', '')


########################################
## Domain
########################################

class Domain:
	def __init__(self, str_domain_name, experiment):
		self._domain_name = DomainName(str_domain_name)
		self._ip_mappings = None
		self._linguistic_feature_set = None
		self._bipartite_graph_feature_set = None
		self._timeseries = None
		self._experiment = experiment

	def __str__(self):
		return str(self._domain_name)

	def get_domain_name(self):
		return self._domain_name

	def get_ip_mappings(self):
		if (self._ip_mappings == None):
			try:
				database_instance = DatabaseInterface()
			except DatabaseInterface as old_database_instance:
				database_instance = old_database_instance

			self._ip_mappings = database_instance.get_ip_addr_associated_with_domain(self, self._experiment)

		return self._ip_mappings

	def set_linguistic_feature_set(self, feature_set):
		self._linguistic_feature_set = feature_set

	def get_linguistic_feature_set(self):
		if (self._linguistic_feature_set == None):
			raise Exception('The linguistic features are not set.')

		return self._linguistic_feature_set

	def set_bipartite_graph_feature_set(self, feature_set):
		self._bipartite_graph_feature_set = feature_set

	def get_bipartite_graph_feature_set(self):
		if (self._bipartite_graph_feature_set == None):
			raise Exception('The bipartite graph features are not set.')

		return self._bipartite_graph_feature_set

	def get_timeseries(self):
		if self._timeseries == None:
			try:
				database_instance = DatabaseInterface()
			except DatabaseInterface as old_database_instance:
				database_instance = old_database_instance

			self._timeseries = database_instance.get_timeseries_associated_with_domain(self, self._experiment)

		return self._timeseries


########################################
## DomainName
########################################

class DomainName:
	def __init__(self, str_domain_name):
		self._original_domain_name = clean_string(str_domain_name)

		try:
			psl = PublicSuffixList()
		except PublicSuffixList as public_suffix_list_instance:
			psl = public_suffix_list_instance

		suffix = psl.get_public_suffix(self._original_domain_name);
		partition = suffix.partition('.')

		if (len(partition[2]) == 0):
			raise Exception('The domain name ' + self._original_domain_name + ' can not be parsed correctly.')
		
		self._public_suffix = clean_string(partition[2])
		secondary_labels = self._original_domain_name[0 : -len(self._public_suffix) - 1]
		self._labels_list = string.split(secondary_labels, '.')
		self._labels_list = map(lambda x: clean_string(x), self._labels_list)

	def __str__(self):
		return self.get_chosen_prefix() + '.' + self.get_public_suffix()

	def get_public_suffix(self):
		return self._public_suffix

	def get_chosen_prefix(self):
		string = '.'.join(self._labels_list)
		return string

	def get_flatten_chosen_prefix(self):
		return flatten_domain_name_string(self.get_chosen_prefix())

	def get_number_of_labels(self):
		return len(self._labels_list)

	def get_label(self, index = 0):
		return self._labels_list[self.get_number_of_labels() - index]

	def get_original_domain_name(self):
		return self._original_domain_name