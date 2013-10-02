import sys
from pymongo import Connection
from dga_classifier.core.linguistic_classifier.linguistic_classifier import DGAClassifier
from dga_classifier.core.domain.domain import Domain

SIZE = 897167 + 897464

def extract_dga_domains():
	db = Connection().botime
	collections = [db.dns_compressed, db.dns_compressed2]

	old_out, new_out = "", ""
	counter = 0

	for collection in collections:
		print "Using collection " + str(collection)
		documents = collection.find()
		for document in documents:
			counter += 1
			new_out = "Analyzing: " + document["domain"] + " -  " + str(counter) + "/" + str(SIZE)
			sys.stdout.write('\r' + (' ' * len(old_out)))
			sys.stdout.write('\r' + new_out)
			old_out = new_out

			domain = Domain(document["domain"], False)
			DGA_Classifier = DGAClassifier(domain)
			DGA_Classifier.classify(strict=True)

			if domain.get_linguistic_feature_set().get_DGA_label() == 'DGA':
				db.dga_dns.insert(document)

def main(argv):
	return extract_dga_domains()

if __name__ == '__main__':
	sys.exit(main(sys.argv))