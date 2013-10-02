from pymongo import Connection

db = Connection().botime
records = db.blacklist_domains.find()

for record in records:
	black_domain = db.dns_compressed.find_one({"domain" : record["domain"]})
	if black_domain:
		print black_domain["domain"] + " inserted."
		db.domains_blacklisted.insert(black_domain)
	else:
		black_domain = db.dns_compressed2.find_one({"domain" : record["domain"]})
		if black_domain:
			db.domains_blacklisted.insert(black_domain)
			print black_domain["domain"] + " inserted."


