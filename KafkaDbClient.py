import os
import traceback
import sys
import time
import subprocess
import logging
from time import sleep

from kafka import KafkaClient, SimpleProducer, SimpleConsumer
from IDbClient import IDbClient

class KafkaDbClient (IDbClient):

	def __init__ (self, args = None):
		self.kafka = KafkaClient("n1:9092,n2:9092,n3:9092")
		self.producer = SimpleProducer(self.kafka, async=False,
                          req_acks=SimpleProducer.ACK_AFTER_CLUSTER_COMMIT,
                          ack_timeout=5000)
		self.topic = 'rr5'
		command = "sudo /opt/kafka/bin/kafka-create-topic.sh  --partition 1  --topic %s --replica 3 --zookeeper n4:2181  " %(self.topic)
		print command
		self.executeProcessLocally (command)


	def put(self, data, args=None):
		start = time.time()
		success = False


		try:
			response = self.producer.send_messages(self.topic, str(data))
			if response and response[0].error == 0:
				success = True
		except Exception, err:
			logging.exception(err)

		time_taken = time.time() - start

		return (success, time.time()-start)	

	def getLog(self, args=None):

		command = "sudo timeout 7s /opt/kafka/bin/kafka-console-consumer.sh --zookeeper n4:2181 --topic %s  --from-beginning > /tmp/op" % (self.topic)
		self.executeProcessLocally (command)
		log = []

		with open('/tmp/op','r') as f:
			for line in f:
				log.append(line.strip())
		return log		

	def executeProcessLocally(self, command):
		exitStatus = subprocess.call (command, shell=True)
		sleep(2)
		return exitStatus

def main():
	cli = KafkaDbClient()
	#for i in range(0, 10):
	#	print cli.put(i)
	print cli.getLog()

if __name__ == '__main__':
	main()









