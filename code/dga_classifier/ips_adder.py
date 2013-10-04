from pymongo import Connection
import sys

def insert_ips_in_dgas_404_not_null():
	db = Connection().botime
	dgas = db.dgas_404_not_null_reply

	documents = dgas.find(timeout=False)

	n_of_docs = documents.count()
	counter = 0

	for document in documents:
		new_doc = dict()
		new_doc["domain"] = document["domain"]
		ip_entries = db.dns_compressed_ips.find({'domain' : document['domain']}, {"ip" : 1})
		ips_list = list()
		for ip_entry in ip_entries:
			ips_list.append(ip_entry["ip"])
		new_doc["ips"] = ips_list
		new_doc["last_res_timestamp"] = document["last_reply"]
		new_doc["last_req_timestamp"] = document["last_query"]
		new_doc["first_req_timestamp"] = document["first_query"]
		new_doc["first_res_timestamp"] = document["first_reply"]
		new_doc["queries"] = document["queries"]
		new_doc["label"] = document["label"]

		req_count = 0
		for query in document["queries"]:
			req_count += query["count"]
		new_doc["req_count"] = req_count

		db.webapp_demo.insert(new_doc)
		print "Done analyzing " + document["domain"] + " " + str(counter) + "/" + str(n_of_docs)
		counter += 1


def main(argv):
	return insert_ips_in_dgas_404_not_null()

if __name__ == '__main__':
	sys.exit(main(sys.argv))