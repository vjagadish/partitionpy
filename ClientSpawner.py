import threading
from KafkaDbClient import KafkaDbClient




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
	print 'boo'

	filename = '/tmp/w%s'%(str(low))
	with open(filename,'w') as f: 
		while (i<high):
			(status, timetaken) = clientInstance.put(i)
			print 'from thread: %s data inserted: %s status: %s time: %s' %(str(i),threading.current_thread().name, status, timetaken)
			f.write('%s:%s:%s\n'%(str(i), str(status), str(timetaken)))
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


def stateMachine():
	numclients = 3
	maxVal = 30
	cli = KafkaDbClient()
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





if __name__ == '__main__':
	stateMachine()

