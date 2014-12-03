import commands
import logging
import redis
import subprocess
import time

from IDbClient import IDbClient

class RedisClient (IDbClient):

	def __init__ (self, args = None):
		self.client = redis.StrictRedis()

	def put(self, data, args=None):
		start = time.time()
		success = False
		try:
			# we just care about the key right now
			print data
			response = self.client.set(data, "foo")
			if response:
				success = True
		except Exception, err:
			logging.exception(err)

		time_taken = time.time() - start
		return (success, time.time()-start)	

	def getLog(self, args=None):
		return self.client.keys()

def main():
	cli = RedisClient()
	for i in range(0, 10):
		print cli.put(i)
	print cli.getLog()

if __name__ == '__main__':
	main()
