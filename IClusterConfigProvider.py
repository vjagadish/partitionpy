import abc

class IClusterConfigProvider:
	__metaclass__ = abc.ABCMeta

	@abc.abstractmethod
	def getConfiguredHosts(self, args=None):
		return

	@abc.abstractmethod
	def getConfiguredHostIPs(self, args=None):
		return

	@abc.abstractmethod
	def getAuthorizedUserName(self, hostIP, args=None):
		return

	@abc.abstractmethod
	def getHostConfig(self, alias):
		return

	@abc.abstractmethod
	def getHostIP(self, alias):
		return

		