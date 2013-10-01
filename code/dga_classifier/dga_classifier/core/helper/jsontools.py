import json
from pymongo import Connection

def domain_feature_set_to_json(domain, feature_set):
	dictionary = dict()
	dictionary["domain"] = domain.get_domain_name().get_original_domain_name()
	dictionary["meaningful_word_ratio"] = feature_set.get_meaningful_word_ratio()
	dictionary["one_gram"] = feature_set.get_one_gram_normality_score()
	dictionary["two-gram"] = feature_set.get_two_gram_normality_score()
	dictionary["three-gram"] = feature_set.get_three_gram_normality_score()
	dictionary["label"] = feature_set.get_DGA_label()

	db = Connection().botime
	record = db.dns_compressed2.find({'domain' : dictionary['domain']})
	for entry in record:
		dictionary["first_req_timestamp"] = entry["first_query"]
		dictionary["last_req_timestamp"]  = entry["last_query"]
		dictionary["first_res_timestamp"] = entry["first_reply"]
		dictionary["last_res_timestamp"]  = entry["last_reply"]
		dictionary["queries"] = entry["queries"]

	ip_entries = db.dns_compressed_ips.find({'domain' : dictionary['domain']}, {"ip" : 1})
	ips_list = list()
	for ip_entry in ip_entries:
		ips_list.append(ip_entry["ip"])
	dictionary["ips"] = ips_list

	db.webapp_demo.insert(dictionary)


def domain_cluster_to_json(cluster):
	return json.dumps(_domain_cluster_to_dictionary(cluster))


def _domain_cluster_to_dictionary(cluster):
	dictionary = dict()
	dictionary["id"] = cluster.get_identifier()

	dictionary["ips"] = list(cluster.get_ip_backbone_set())

	domains = cluster.get_domains()
	domain_names = [x.get_domain_name().get_original_domain_name() for x in domains]
	dictionary["domains"] = domain_names

	d = cluster.get_linguistic_descriptor()
	dictionary["length_interval"] = d.get_length_interval()
	dictionary["character_set"] = list(d.get_character_set())
	dictionary["numerical_ratio"] = d.get_numerical_characters_ratio_interval()
	dictionary["public_suffix"] = list(d.get_public_suffix_set())
	dictionary["meaningful_word"] = d.get_meaningful_word_ratio_interval()
	dictionary["one_gram"] = d.get_one_gram_normality_score_interval()
	dictionary["two_gram"] = d.get_one_gram_normality_score_interval()
	dictionary["three_gram"] = d.get_one_gram_normality_score_interval()

	return dictionary


def domain_clusters_to_json(clusters):
	dictionary = dict()
	dictionary["clusters"] = list()
	for cluster in clusters:
		dictionary["clusters"].append(_domain_cluster_to_dictionary(cluster))

	return json.dumps(dictionary)