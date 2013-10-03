from pymongo import Connection
import requests
import sys

GOOGLE = "https://sb-ssl.google.com/safebrowsing/api/lookup?client=api&apikey=ABQIAAAAon-fFtRSQr5xGW0An38rAhTNlWfV3cKDagZ18YLN5Ovd24feiw&appver=1.0&pver=3.0&url=http%3A%2F%2F"

def copy_dga_non_ok():
	db = Connection().botime
	dgas = db.dga_dns_backup

	# documents = dgas.find()
	documents = dgas.find({"domain": { "$gt" : "kugou.com"}},timeout=False)

	for document in documents:
		print "Analyzing domain " + document["domain"]
		try:
			requests.head("http://" + document["domain"], timeout=0.5)
		except requests.exceptions.ConnectionError:
			print "Inserting domain " + document["domain"]
			db.dgas_404.insert(document)
		except requests.exceptions.Timeout:
			print "Inserting domain " + document["domain"]
			db.dgas_404.insert(document)


def main(argv):
	return copy_dga_non_ok()

if __name__ == '__main__':
	sys.exit(main(sys.argv))