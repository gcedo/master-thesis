from pymongo import Connection

db = Connection().botime
records = db.blacklist_domains.find()

counter = 0

for record in records:
	black_domain = db.dns_compressed.find_one({"domain" : record["domain"]})
	if black_domain:
		db.domains_blacklisted.insert(black_domain)
		print str(counter) + " : " + black_domain["domain"] + " inserted."
		counter += 1
	else:
		black_domain = db.dns_compressed2.find_one({"domain" : record["domain"]})
		if black_domain:
			db.domains_blacklisted.insert(black_domain)
			print str(counter) + " " + black_domain["domain"] + " inserted."
			counter += 1


