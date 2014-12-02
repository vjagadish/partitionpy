import abc

class IFailureMode:
	__metaclass__ = abc.ABCMeta

	@abc.abstractmethod
	def doFailure(self, args):
		return

	@abc.abstractmethod
	def doRecovery(self, args):
		return
		