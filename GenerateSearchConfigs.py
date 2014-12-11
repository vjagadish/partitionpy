import random
import json

failure_modes = ['ISOLATE', 'HEAL_ISOLATE', 'CRASH']
nodes = ['n1', 'n2', 'n3']

failures = []
for node in nodes:
	for mode in failure_modes:
		failures.append((node, mode))

print "Nodes: ", nodes
print "Failure Modes: ", failure_modes
print "Searching over failure modes..."

condition_list = []
for i in xrange(2**(len(failures))):
	condition = []
	for j in xrange(len(failures)):
		if i & j :
			condition.append(failures[j])
	condition_list.append(condition)

def getFailureConfig(condition):
	config = {}
	timestamp = 0
	for node, mode in condition:
		config[mode] = node
		timestamp += random.randint(0, 100)
		config['TIMESTAMP_' + str(mode)] = timestamp
	print json.dumps(config)
	

for condition in condition_list:
	getFailureConfig(condition)
	raw_input()
