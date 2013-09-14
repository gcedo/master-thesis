import sys
import math
import re
from dga_classifier.core.clustering.cluster import DomainClusterDatabaseFactory
from dga_classifier.core.clustering.family_clusterer import FamilyClusterer


########################################
## Sensitivity evaluation
########################################

def sensitivity_evaluation():
	def _compute_average_entropies(list_of_clusters):
		def _entropies(cluster):
			suffixes = dict()
			lengths= dict()
			ratios = dict()

			for domain in cluster:
				public_suffix = domain.get_domain_name().get_public_suffix()
				length = len(domain.get_domain_name().get_chosen_prefix())
				regex = re.compile(r'[^0-9]+')
				ratio = len(regex.sub('', domain.get_domain_name().get_chosen_prefix())) / float(len(domain.get_domain_name().get_chosen_prefix()))

				ratio = round(ratio, 1)

				if public_suffix not in suffixes:
					suffixes[public_suffix] = 0

				suffixes[public_suffix] = suffixes[public_suffix] + 1

				if length not in lengths:
					lengths[length] = 0

				lengths[length] = lengths[length] + 1

				if ratio not in ratios:
					ratios[ratio] = 0

				ratios[ratio] = ratios[ratio] + 1


			suffix_probabilities = list()

			for suffix in suffixes:
				suffix_probabilities.append(suffixes[suffix] / float(len(cluster)))

			suffix_logs = map(lambda x : x * math.log(1 / float(x), 2), suffix_probabilities)


			length_probabilities = list()

			for length in lengths:
				length_probabilities.append(lengths[length] / float(len(cluster)))

			length_logs = map(lambda x : x * math.log(1 / float(x), 2), length_probabilities)


			ratio_probabilities = list()

			for ratio in ratios:
				ratio_probabilities.append(ratios[ratio] / float(len(cluster)))

			ratio_logs = map(lambda x : x * math.log(1 / float(x), 2), ratio_probabilities)

			return sum(suffix_logs) , sum(length_logs), sum(ratio_logs)


		if len(list_of_clusters) == 0:
			return [0.0, 0.0, 0.0]

		cumulative_entropy_suffix = 0
		cumulative_entropy_length = 0
		cumulative_entropy_ratio = 0
		total_size = 0

		for cluster in list_of_clusters:
			total_size += len(cluster)
			suffix_entropy, length_entropy, ratio_entropy = _entropies(cluster)

			cumulative_entropy_suffix += len(cluster) * suffix_entropy
			cumulative_entropy_length += len(cluster) * length_entropy
			cumulative_entropy_ratio += len(cluster) * ratio_entropy

		return [cumulative_entropy_suffix / float(total_size), cumulative_entropy_length / float(total_size), cumulative_entropy_ratio / float(total_size)]


	exposure_cluster_factory = DomainClusterDatabaseFactory(identifier = 'exposure', experiment = False)
	exposure_cluster = exposure_cluster_factory.get()


	family_clusterer = FamilyClusterer(exposure_cluster)

	for max_ratio in [0.5 * x + 1 for x in range(101)]:
		dga_sublusters = family_clusterer.compute_clusters(max_ratio=max_ratio)
		print max_ratio, len(dga_sublusters), ' '.join(map(str, _compute_average_entropies(dga_sublusters)))


########################################
## Main method
########################################

def main(argv):
	return sensitivity_evaluation()

if __name__ == '__main__':
	sys.exit(main(sys.argv))