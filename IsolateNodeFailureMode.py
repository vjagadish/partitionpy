from IFailureMode import IFailureMode
from StaticClusterConfigProvider import StaticClusterConfigProvider
from SshRemoteExecutor import SshRemoteExecutor


class IsolateNodeFailureMode (IFailureMode):

	def __init__ (self, hostToIsolate, clusterConfigProvider):
		self.hostToIsolate = hostToIsolate		
		self.clusterConfigProvider = clusterConfigProvider
		self.ipToIsolate = clusterConfigProvider.getHostIP(hostToIsolate)

	def doFailure(self, args = None):

		allhosts = self.clusterConfigProvider.getConfiguredHosts()

		for host in allhosts:
			if host != self.hostToIsolate:
				hostConfig = self.clusterConfigProvider.getHostConfig(host)
				alias = hostConfig['alias']
				authorized_user = hostConfig['authorized_user']
			
				timeout = 10000
				addMissingKeys = True
				executor = SshRemoteExecutor(host, authorized_user, addMissingKeys, timeout)
			
				command = 'sudo iptables -A INPUT -s %s -j DROP' % (self.hostToIsolate)
				executor.execCommand(command)
			
				command = 'sudo iptables -A INPUT -s %s -j DROP' % (self.ipToIsolate)
				executor.execCommand(command)


	def doRecovery(self, args = None):
		allhosts = self.clusterConfigProvider.getConfiguredHosts()
		for host in allhosts:
			if host != self.hostToIsolate:
				hostConfig = self.clusterConfigProvider.getHostConfig(host)
				alias = hostConfig['alias']
				authorized_user = hostConfig['authorized_user']
			
				timeout = 10000
				addMissingKeys = True
				executor = SshRemoteExecutor(host, authorized_user, addMissingKeys, timeout)
			
				command = 'sudo iptables -X' 
				executor.execCommand(command)
			
				command = 'sudo iptables -F' 
				executor.execCommand(command)


				

IFailureMode.register(IsolateNodeFailureMode)

def main():

	#DON'T ADD n4 here. We'll need it to heal the partition and get n1 back.
	jsonConfigString = """
	[
	{"alias":"n1", "ip":"172.31.40.107", "authorized_user":"ec2-user"},
	{"alias":"n2", "ip":"172.31.32.165", "authorized_user":"ec2-user"},
	{"alias":"n3", "ip":"172.31.44.108", "authorized_user":"ec2-user"}
	]
	"""
	clusterConfigProvider = StaticClusterConfigProvider(jsonConfigString)



	isolateNodeFailureMode = IsolateNodeFailureMode('n1', clusterConfigProvider)
	isolateNodeFailureMode.doFailure()

	raw_input()
	isolateNodeFailureMode.doRecovery()

if __name__ == "__main__":
    main()


	