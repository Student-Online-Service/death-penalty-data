#!/usr/bin/env python

import sys
import os.path
import ColumnMap
import Mapping
import Execution
from collections import defaultdict

import pprint, json, csv

def prettyprint(AllExecutions):
	pprint.pprint(AllExecutions)

def writeJSON(AllExecutions):
	with open("data.json", "w") as outfile:
	    json.dump(AllExecutions, outfile, indent=4)

def writeCSV(AllExecutions):
	spamWriter = csv.writer(open('espy.csv', 'wb'), delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	spamWriter.writerow(AllExecutions[1].keys())
	for execution in AllExecutions:
		spamWriter.writerow(execution.values())

def writeCSVList(AllExecutions):
	spamWriter = csv.writer(open('data.csv', 'wb'), delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	#spamWriter.writerow(AllExecutions[1].keys())
	for execution in AllExecutions:
		spamWriter.writerow(execution)


Maps = ColumnMap.Maps
CrimeMappings = Mapping.CrimeMappings
AllExecutions = []

if not os.path.isfile('08451-0001-Data.txt'):
	print "Couldn't find '08451-0001-Data.txt'. You need to download it manually (see README)"
	sys.exit()

#1608-2002
with open('08451-0001-Data.txt') as asciidata:
 for penalty in asciidata:
 	current_execution = Execution.Execution()
 	for column in Maps:
 		value = penalty[column['begin']:column['end']+1]
 		if value.isdigit():
 			if column['expand'] == True:
	 			value = int(value)
 				if value == 0:
 					attribute = 0
	 			else:
		 			attribute = CrimeMappings[column['name']][value]

		 	else:
		 		attribute = value
		else:
			attribute = value.strip()
		setattr(current_execution,column['name'],attribute)
	AllExecutions.append(current_execution.getExecution())

writeCSV(AllExecutions)

print "found %d total executions in the data" % len(AllExecutions)

if "--states" in sys.argv:
	AllExecutions = [ex for ex in AllExecutions if ex["JurisdictionOfExecution"] == "State"]	
	print "reduced to %d executions carried out by states" % len(AllExecutions)

data = defaultdict(lambda: defaultdict(int))
total = defaultdict(int)

for ex in AllExecutions:
	data[ex['DateYear']][ex['StateOfExecution']] += 1
	total[ex['StateOfExecution']] += 1

headers = sorted(total.keys())
output = [["year"] + headers]

for y in range(1700, 2003):
	datum = [y]
	for state in headers:		
		datum.append(0 if state not in data[str(y)] else data[str(y)][state])
	output.append(datum)

writeCSVList(output)