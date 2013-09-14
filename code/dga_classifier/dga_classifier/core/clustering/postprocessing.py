from dga_classifier.core.clustering.cluster import DomainClusterToolbox
from dga_classifier.core.clustering.cluster import DomainCluster


def apply_mask(ip_address, mask = 16):
			if (mask != 0 and mask != 8 and mask != 16):
				raise Exception('The mask should be 0, 8 or 16.')

			ip_address_split = ip_address.split('.')

			if mask >= 8:
				ip_address_split[3] = '*'

			if mask >= 16:
				ip_address_split[2] = '*'

			return '.'.join(ip_address_split)


########################################
## Post processing module
########################################

class PostProcessor:
	def __init__(self):
		pass

	def postprocess(self, list_of_clusters):
		list_of_clusters = self._merge_for_ip_similarity(list_of_clusters)

		result = list()

		for cluster in list_of_clusters:
			result.append(self._split_for_ip_backbone(cluster))

		return result;

	def _merge_for_ip_similarity(self, list_of_clusters, min_fitting_value = 0):
		def compute_ip_based_distance(cluster1, cluster2):
			set1 = set(map(lambda x: apply_mask(x, 0), cluster1.get_ip_set()))
			set2 = set(map(lambda x: apply_mask(x, 0), cluster2.get_ip_set()))
			intersection = set1.intersection(set2)

			return len(intersection) / float(min(len(set1), len(set2)))

		toolbox = DomainClusterToolbox()
		cluster_dictionary = dict()
		main_dict = dict()

		for cluster in list_of_clusters:
			cluster_id = cluster.get_identifier()
			main_dict[cluster_id] = dict()
			cluster_dictionary[cluster_id] = cluster

		for cluster_id in main_dict:
			for other_cluster_id in main_dict:
				if (other_cluster_id > cluster_id):
					main_dict[cluster_id][other_cluster_id] = compute_ip_based_distance(cluster_dictionary[cluster_id], cluster_dictionary[other_cluster_id])

		def find_gratest():
			best_value = -1
			best_cluster_id = None
			best_other_cluster_id = None

			for cluster_id in main_dict:
				for other_cluster_id in main_dict[cluster_id]:
					current_value = main_dict[cluster_id][other_cluster_id]

					if current_value > best_value:
						best_value = current_value
						best_cluster_id = cluster_id
						best_other_cluster_id = other_cluster_id

			return (best_cluster_id, best_other_cluster_id, best_value)

		def clear_dictionaries(id1, id2):
			del cluster_dictionary[id1]
			del cluster_dictionary[id2]

			for cluster_id in main_dict:
				if id1 in main_dict[cluster_id]:
					del main_dict[cluster_id][id1]
	
				if id2 in main_dict[cluster_id]:
					del main_dict[cluster_id][id2]

			del main_dict[id1]
			del main_dict[id2]

		while len(cluster_dictionary) > 1:
			(cluster0_id, cluster1_id, fitting_value) = find_gratest()

			if fitting_value <= min_fitting_value:
				break

			cluster0 = cluster_dictionary[cluster0_id]
			cluster1 = cluster_dictionary[cluster1_id]

			clear_dictionaries(cluster0_id, cluster1_id)

			cluster0_1 = toolbox.merge([cluster0, cluster1], cluster0_id + '+' + cluster1_id)
			cluster0_1_id = cluster0_1.get_identifier()

			main_dict[cluster0_1_id] = dict()

			for cluster_id in cluster_dictionary:
				main_dict[cluster0_1_id][cluster_id] = compute_ip_based_distance(cluster0_1, cluster_dictionary[cluster_id])

			cluster_dictionary[cluster0_1_id] = cluster0_1

		result = list()

		for elem in cluster_dictionary:
			result.append(cluster_dictionary[elem])

		return result

	def _split_for_ip_backbone(self, cluster):
		identifiers = dict()
		result = list()

		for domain in cluster:
			ip_mappings = sorted(list(set(map(lambda x: apply_mask(x, 0), domain.get_ip_mappings()))))
			identifier = '/'.join(ip_mappings)

			if identifier not in identifiers:
				identifiers[identifier] = list()

			identifiers[identifier].append(domain)

		for identifier in identifiers:
			new_cluster = DomainCluster(cluster.get_identifier() + ':' + identifier)
			new_cluster.add_bulk_domains(identifiers[identifier])
			result.append(new_cluster)

		return result