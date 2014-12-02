import abc

class IRemoteExecutor:
	__metaclass__ = abc.ABCMeta

	@abc.abstractmethod
	def execCommand(self, command, timeout):
		return

	@abc.abstractmethod
	def getHost(self): 
	    return

	@abc.abstractmethod    
	def getUser (self):
		return
    