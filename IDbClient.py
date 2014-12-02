import abc

class IDbClient:
	__metaclass__ = abc.ABCMeta

	@abc.abstractmethod
	def put(self, element, args=None):
		return

	@abc.abstractmethod
	def getLog(self, element, args=None):
		return
		