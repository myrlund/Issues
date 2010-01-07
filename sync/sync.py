# -*- coding: utf8 -*-

import sys

MODEL_DELIM = ":"
FIELD_DELIM = ";"

f = open("economy.csv", "rb")
c = f.read()
c = c.splitlines()

def parse_header(line):
	model, fields = line.split(MODEL_DELIM)
	fields = [f.strip() for f in fields.split(FIELD_DELIM)]
	return (model, fields)

def parse_line(line, fields, model=None):
	content = line.split(FIELD_DELIM)
	if len(fields) != len(content):
		raise KeyError("Antall felter stemmer ikke overens i %s." % model)
	data = {}
	for n in range(len(fields)):
		data[fields[n]] = content[n] or '""'
	# if fields and fields[0] == "number":
	# 	print dict.fromkeys(fields, line)
	return data

model, fields = parse_header(c.pop(0))	
lines = {}
lines[model] = {"fields": fields, "rows": []}
line = ""
while c:
	line += c.pop(0)
	if len(line) == 0:
		line = c.pop(0)
		model, fields = parse_header(line)
		lines[model] = {"fields": fields, "rows": []}
		line = ""
	else:
		if line[-1] in ["\"", ";"]:
			line = parse_line(line, fields, model)
			lines[model]["rows"].append(line)
			line = ""

# print lines["contract_project"]["rows"]

# Replace project_code with project_ids in contracts
project_tbl = "contract_project"
project_map = {}
n = 1
for project in lines[project_tbl]["rows"]:
	project["number"] = int(project["number"][1:-1])
	project["id"] = n
	project_map[project["number"]] = n
	n += 1

for contract in lines["contract_contract"]["rows"]:
	contract["project_id"] = int(contract["project_id"][1:-1])
	if contract["project_id"] in project_map.keys():
		contract["project_id"] = project_map[contract["project_id"]]
	else:
		# Lag tomt prosjekt
		project_map[contract["project_id"]] = n
		lines[project_tbl]["rows"].append({"number": contract["project_id"], "mod_date": '"0000-00-00 00:00:00"', "pub_date": '"0000-00-00 00:00:00"', "title": '"Uten tittel"', "tax_rate": '"0.25"', "id": n})
		contract["project_id"] = n
		n += 1
	
	# contract["project_id"] = project_map[contract["project_id"]]
	contract["id"] = int(contract["id"][1:-1])

# Split up changes and invoices
for inv in lines["invoices_determine"]["rows"]:
	inv["change"] = int(inv["change"][1:-1])
	if inv["change"] == 1:
		model = "invoices_change"
		if not inv["status_id"]:
			inv["status_id"] = "0"
	else:
		model = "invoices_invoice"
	
	lines[model]["rows"].append(inv)
	for field in inv.keys():
		if field not in lines[model]["fields"]:
			del inv[field]

del lines["invoices_determine"]

for field in lines["invoices_changestatusdate"]["fields"]:
	if field == "project_number":
		del field
for statusdate in lines["invoices_changestatusdate"]["rows"]:
	del statusdate["project_number"]

# for model, dataset in lines.iteritems():
# 	for row in dataset["rows"]:
# 		for field in row.keys():
# 			if row[field] == None:
# 				row[field] = '""'

sql = "BEGIN TRANSACTION;"
for model, data in lines.iteritems():
	for inst in data["rows"]:
		sql += "\n"
		sql += "INSERT INTO %s (%s) VALUES " % (model, ", ".join(data["rows"][0].keys()))
		sql += "(%s)" % ", ".join([str(inst[f]) for f in data["rows"][0].keys()]) + ";"
sql += "\nCOMMIT;"

# print project_map
print sql
