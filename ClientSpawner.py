import json
import subprocess
import threading
import time
from RedisClient import RedisClient
from StaticClusterConfigProvider import StaticClusterConfigProvider
from IsolateNodeFailureMode import IsolateNodeFailureMode
from KillRestartFailureMode import KillRestartFailureMode
from threading import Timer

def spawnClients (numclients, maxVal, clientInstance):
	interval = maxVal/numclients
	low=0
	high=maxVal

	threads=[]

	while (low<high):
		print 'low high %s %s' %(low, low+interval)
		t = threading.Thread(target=rangePut, args=(low,low+interval, clientInstance,)) 
		low+=interval
		threads.append(t)


	for t in threads:
		t.start()	

	for t in threads:
		t.join()	

	collateLogFiles(numclients, maxVal)	

	#read files written by all threads.


def collateLogFiles (numclients, maxVal):
	low = 0
	successes = set()
	fails = set()

	while low < maxVal:
		filename = '/tmp/w%s'%(str(low))
		low+=(maxVal/numclients)
		with open(filename, 'r') as f:
			for line in f:
				(val, status, time) = line.split(':')
				if (status == 'True'):
					successes.add(val)
				else:
					fails.add(val)

	print successes
	print fails
	return successes, fails






def rangePut (low, high, clientInstance):
	i = low
	filename = '/tmp/w%s'%(str(low))
	with open(filename,'w') as f: 
		while (i<high):
			(status, timetaken) = clientInstance.put(i)
			#print 'from thread: %s data inserted: %s status: %s time: %s' %(str(i),threading.current_thread().name, status, timetaken)
			f.write('%s:%s:%s\n'%(str(i), str(status), str(timetaken)))
			time.sleep(0.3)
			i=i+1

def printStats(log, successes, fails):
	ackedAndLost = set()
	ackedAndPresent = set()
	notAckedAndPresent = set()
	notAckedAndAbsent = set()


	for data in successes:
		if data not in log:
			ackedAndLost.add(data)
		else:
			ackedAndPresent.add(data)

	for data in fails:
		if data not in log:
			notAckedAndAbsent.add(data)
		else:
			notAckedAndPresent.add(data)
	return (ackedAndLost, ackedAndPresent, notAckedAndPresent, notAckedAndAbsent)	

def buildFailureObjects(failureConfig):

	#jsonConfigString = """
	#[
	#{"alias":"n1", "ip":"172.31.40.107", "authorized_user":"ec2-user"},
	#{"alias":"n2", "ip":"172.31.32.165", "authorized_user":"ec2-user"},
	#{"alias":"n3", "ip":"172.31.44.108", "authorized_user":"ec2-user"}
	#]
	#"""

	jsonConfigString = """
	[
	{"alias":"n2", "ip":"172.31.32.165", "authorized_user":"ec2-user"},
	{"alias":"n3", "ip":"172.31.44.108", "authorized_user":"ec2-user"},
	{"alias":"n4", "ip":"172.31.39.157", "authorized_user":"ec2-user"}
	]
	"""

	parsedConfig = json.loads(config)
	failureModes = []
	for configElem in parsedConfig:
		action = configElem['action']
		if action == 'ISOLATE':
			clusterConfigProvider = StaticClusterConfigProvider(jsonConfigString)
			targetNode = configElem['node']
			isolateNodeFailureMode = IsolateNodeFailureMode(targetNode, clusterConfigProvider)
			failureModes.append(isolateNodeFailureMode)
		if action == 'CRASH':
			clusterConfigProvider = StaticClusterConfigProvider(jsonConfigString)
			targetNode = configElem['node']
			killFailureMode = KillRestartFailureMode(targetNode, configElem['killCmd'], configElem['restartCmd'], clusterConfigProvider)
			failureModes.append(killFailureMode)

	return failureModes


def failureScheduler (timeBetweenFailures, failureConfig):
	failures = buildFailureObjects(failureConfig)
	print failures
	print 'Will sleep for 120 s before beginning failures'	
	time.sleep(3)
	eventTime = 2
	for failure in failures:
		Timer(eventTime, scheduleFunction, (failure,)).start()		
		print 'Wait 20 seconds between Failures'
		eventTime+=timeBetweenFailures

	sleepTime = len(failures) * timeBetweenFailures  * 2
	time.sleep(sleepTime)



def scheduleFunction (failureMode):
	failureMode.doFailure()

			
def stateMachine(config):
	numclients = 1
	maxVal = 1000
	cli = RedisClient()
	print 'Going to start failure scheduler'
	t = threading.Thread(target=failureScheduler, args=(10, config,)) 
	t.start()

	spawnClients(numclients, maxVal, cli)


	(successes, fails) = collateLogFiles(numclients, maxVal)
	log = set(cli.getLog())
	(ackedAndLost, ackedAndPresent, notAckedAndPresent, notAckedAndAbsent) = printStats (log, successes, fails)

	print 'STATISTICS'
	print 'ackedAndLost %s' %(len(ackedAndLost))
	print 'ackedAndPresent %s'%(len(ackedAndPresent))
	print 'notAckedAndPresent %s'%(len(notAckedAndPresent))
	print 'notAckedAndAbsent %s' %(len(notAckedAndAbsent))
	print ackedAndLost
	print sorted(successes)
	print sorted(log)

	t.join()

def getRedisConfig():
	redis_config = """[ {"action":"ISOLATE", "node": "n4"} ]"""
	return redis_config

if __name__ == '__main__':
	# config = """[
	# {"action":"ISOLATE", "node": "n1"}, 
	# {
	# "action": "CRASH", "node" : "n1", 
	# "killCmd": "ps -effw | grep kafka | grep -v grep | awk '{print $2}' | xargs sudo kill -9",
	# "restartCmd": "sudo /opt/kafka/bin/kafka-server-start.sh /opt/kafka/config/server.properties > /tmp/oo  2>&1 &"
	# }
	# ]"""
	config = getRedisConfig()
	l = buildFailureObjects(config)
	print l

	stateMachine(config)

