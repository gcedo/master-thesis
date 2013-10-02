import sys
import md5
import math
from scipy.stats import ks_2samp
from dga_classifier.core.clustering.cluster import DomainClusterDatabaseFactory
from dga_classifier.core.clustering.cluster import DomainClusterFileFactory
from dga_classifier.core.clustering.family_clusterer import FamilyClusterer
from dga_classifier.core.clustering.cluster import DomainClusterToolbox
from dga_classifier.core.dga_classifier.unseen_domain_classifier import UnseenDomainClassifier
from dga_classifier.core.timeseries.timeseries import TimeseriesToolbox
from dga_classifier.core.export.webinterface import WebInterfaceGenerator
from dga_classifier.core.linguistic_classifier.linguistic_classifier import DGAClassifier
from dga_classifier.core.helper.tools import colored_label
from dga_classifier.core.helper import jsontools
from termcolor import colored


########################################
## External test
########################################

def external_test(limit=True):
	print "Warming up..."
	exposure_cluster_factory = DomainClusterDatabaseFactory(identifier = 'exposure', experiment = False)
	exposure_cluster = exposure_cluster_factory.get()
	print "Exposure dataset retrieved"

	# Reducing cluster size for testing purposes
	if limit == True:
		cluster_toolbox = DomainClusterToolbox()
		exposure_cluster = cluster_toolbox.split(exposure_cluster, 5000, 1)[0]

	print "Computing clusters"
	family_clusterer = FamilyClusterer(exposure_cluster)
	dga_subclusters = family_clusterer.compute_clusters()
	print "Computing clusters: OK"

	for subcluster in dga_subclusters:
		print str(subcluster)

	print jsontools.domain_clusters_to_json(dga_subclusters)

	experiment_cluster_factory = DomainClusterDatabaseFactory(identifier = 'experiment', experiment = True)
	experiment_cluster = experiment_cluster_factory.get()

	for domain in experiment_cluster:
		unseen_domain_classifier = UnseenDomainClassifier(domain, dga_subclusters)
		classification = unseen_domain_classifier.get_classification()

		if classification.is_known_classification() == False:
			continue

		print domain, classification


########################################
## Webapp test Oct 1 2013
########################################
def webapp_test():
	print 'Getting database instance'
	webapp_cluster_factory = DomainClusterDatabaseFactory(identifier='webapp', experiment=False, webapp=True)
	webapp_cluster = webapp_cluster_factory.get()
	print 'Getting database instance: OK'

	print 'Computing clusters'
	family_clusterer = FamilyClusterer(webapp_cluster)
	dga_subclusters = family_clusterer.compute_clusters()
	print 'Computing clusters: OK'

	print jsontools.domain_clusters_to_json(dga_subclusters)


########################################
## Internal test
########################################

def internal_test():
	exposure_cluster_factory = DomainClusterDatabaseFactory(identifier = 'exposure_blacklist', experiment = False)
	exposure_cluster = exposure_cluster_factory.get()

	cluster_toolbox = DomainClusterToolbox()
	paritioned_clusters = cluster_toolbox.split(exposure_cluster, 10800)

	test_cluster = paritioned_clusters[0]
	test_cluster.set_identifier('test_cluster')
	training_cluster = cluster_toolbox.merge(paritioned_clusters[1:], 'training_cluster')

	family_clusterer = FamilyClusterer(training_cluster)
	dga_sublusters = family_clusterer.compute_clusters()

	for subcluster in dga_sublusters:
		print str(subcluster)

	for domain in test_cluster:
		unseen_domain_classifier = UnseenDomainClassifier(domain, dga_sublusters)
		classification =  unseen_domain_classifier.get_classification()

		print domain, classification


########################################
## Timeline analysis
########################################

def timeline_analysis():
	exposure_cluster_factory = DomainClusterDatabaseFactory(identifier = 'exposure', experiment = False)
	exposure_cluster = exposure_cluster_factory.get()

	family_clusterer = FamilyClusterer(exposure_cluster)
	dga_list_of_list_of_clusters = family_clusterer.compute_clusters(merge = False)

	timeseries_toolbox = TimeseriesToolbox()
	webinterface_generator = WebInterfaceGenerator()

	for list_of_clusters in dga_list_of_list_of_clusters:
		m = md5.new()
		m.update(list_of_clusters[0].get_identifier().split(':')[0])
		family_id = m.hexdigest()

		print '#####################################################'
		print '#### Family ID: ' + family_id
		print '#####################################################'

		for cluster in list_of_clusters:
			print str(cluster)

		if len(list_of_clusters) > 1:
			webinterface_generator.generate('export/' + family_id + '.html', timeseries_toolbox.export_google_charts_js(list_of_clusters))


########################################
## AGD filtering test
########################################

def agd_filtering_test():
	cluster_factory = DomainClusterFileFactory('dga_classifier/assets/conficker.c.txt', False)
	cluster = cluster_factory.get('cluster_0')

	count = 0

	for domain in cluster:
		classifier = DGAClassifier(domain)
		classifier.classify(strict = True)

		label = domain.get_linguistic_feature_set().get_DGA_label()

		if domain.get_linguistic_feature_set().get_DGA_label() == 'DGA':
			count = count + 1

	print 'Positives are (strict): ' + str(count / float(len(cluster)))

	count = 0

	for domain in cluster:
		classifier = DGAClassifier(domain)
		classifier.classify(strict = False)

		label = domain.get_linguistic_feature_set().get_DGA_label()

		if domain.get_linguistic_feature_set().get_DGA_label() == 'DGA':
			count = count + 1

	print 'Positives are (loose): ' + str(count / float(len(cluster)))


########################################
## Sample cluster
########################################

def sample_cluster():
	cluster_factory = DomainClusterFileFactory('dga_classifier/assets/torpig.txt', False)
	cluster = cluster_factory.get('cluster_0')

	cluster_toolbox = DomainClusterToolbox()
	reduced_cluster = cluster_toolbox.split(cluster, 5000, 1)[0]

	for domain in reduced_cluster:
		print domain


########################################
## Bamital test
########################################

def bamital_test():
	bamital_cluster_factory = DomainClusterDatabaseFactory(identifier = 'bamital', experiment = False)
	bamital_cluster = bamital_cluster_factory.get()

	print bamital_cluster

	family_clusterer = FamilyClusterer(bamital_cluster)
	dga_sublusters = family_clusterer.compute_clusters()

	for subcluster in dga_sublusters:
		print str(subcluster)


########################################
## P-test
########################################

def p_test():
	exposure_cluster_factory = DomainClusterDatabaseFactory(identifier = 'exposure', experiment = False)
	exposure_cluster = exposure_cluster_factory.get()

	family_clusterer = FamilyClusterer(exposure_cluster)
	dga_sublusters = family_clusterer.compute_clusters()

	for subcluster in dga_sublusters:
		print str(subcluster)

	for one in range(len(dga_sublusters)):
		subcluster_1 = dga_sublusters[one]
		values_1 = list()

		for domain in subcluster_1:
			values_1.append(len(domain.get_domain_name().get_chosen_prefix()))

		for two in range(one + 1,len(dga_sublusters)):
			subcluster_2 = dga_sublusters[two]
			values_2 = list()

			for domain in subcluster_2:
				values_2.append(len(domain.get_domain_name().get_chosen_prefix()))

			(_, pvalue) = ks_2samp(values_1, values_2)

			print 'Matching ' + str(subcluster_1.get_identifier()) + ' against ' + str(subcluster_2.get_identifier()) + ': ' + str(pvalue)


########################################
## Entropy test
########################################

def entropy_test():
	def _compute_average_entropy(list_of_clusters):
		def _entropy(cluster):
			suffixes = dict()

			for domain in cluster:
				public_suffix = domain.get_domain_name().get_public_suffix()

				if public_suffix not in suffixes:
					suffixes[public_suffix] = 0

				suffixes[public_suffix] = suffixes[public_suffix] + 1

			probabilities = list()

			for suffix in suffixes:
				probabilities.append(suffixes[suffix] / float(len(cluster)))

			logs = map(lambda x : x * math.log(1 / float(x), 2), probabilities)

			return sum(logs)

		if len(list_of_clusters) == 0:
			return 0.0

		cumulative_entropy = 0
		total_size = 0

		for cluster in list_of_clusters:
			total_size += len(cluster)
			cumulative_entropy += len(cluster) * _entropy(cluster)

		return cumulative_entropy / float(total_size)

	exposure_cluster_factory = DomainClusterDatabaseFactory(identifier = 'exposure', experiment = False)
	exposure_cluster = exposure_cluster_factory.get()

	family_clusterer = FamilyClusterer(exposure_cluster)
	dga_sublusters = family_clusterer.compute_clusters()

	for subcluster in dga_sublusters:
		print str(subcluster)

	for one in range(len(dga_sublusters)):
		subcluster_1 = dga_sublusters[one]

		for two in range(one + 1,len(dga_sublusters)):
			subcluster_2 = dga_sublusters[two]

			apart = _compute_average_entropy([subcluster_1, subcluster_2])
			together = _compute_average_entropy([DomainClusterToolbox().merge([subcluster_1, subcluster_2], 'hello')])

			print 'Matching ' + str(subcluster_1.get_identifier()) + ' against ' + str(subcluster_2.get_identifier()) + ': ' + str(together - apart)


########################################
## Migration test
########################################

def migrations_test():
	exposure_cluster_factory = DomainClusterDatabaseFactory(identifier = 'exposure', experiment = False)
	exposure_cluster = exposure_cluster_factory.get()

	family_clusterer = FamilyClusterer(exposure_cluster)
	list_of_list_of_subclusters = family_clusterer.compute_clusters(merge = False)

	timeseries_toolbox = TimeseriesToolbox()
	webinterface_generator = WebInterfaceGenerator()

	for l in list_of_list_of_subclusters:
		m = md5.new()
		m.update(l[0].get_identifier().split(':')[0])
		family_ip = m.hexdigest()

		print '#####################################################'
		print '#### Family ID: ' + family_ip
		print '#####################################################'

		if len(l) > 1:
			for cluster in l:
				print str(cluster)

			print timeseries_toolbox.export_csv(l)
			webinterface_generator.generate('export_final/' + family_ip + '.html', timeseries_toolbox.export_google_charts_js(l))


########################################
## Main method
########################################

def main(argv):
	# print "Executing internal test"
	# return internal_test()
	return external_test()
	#return timeline_analysis()
	#return agd_filtering_test()
	# return sample_cluster()
	#return bamital_test()
	#return p_test()
	#return entropy_test()
	#return migrations_test()
	# return webapp_test()

if __name__ == '__main__':
	sys.exit(main(sys.argv))
