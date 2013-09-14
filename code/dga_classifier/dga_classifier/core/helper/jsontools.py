import json

def domain_feature_set_to_json(domain, feature_set):
	dictionary = dict()
	dictionary["domain"] = domain.get_domain_name().get_original_domain_name()
	dictionary["meaningful_word_ratio"] = feature_set.get_meaningful_word_ratio()
	dictionary["one_gram"] = feature_set.get_one_gram_normality_score()
	dictionary["two-gram"] = feature_set.get_two_gram_normality_score()
	dictionary["three-gram"] = feature_set.get_three_gram_normality_score()
	dictionary["label"] = feature_set.get_DGA_label()

	return json.dumps(dictionary)