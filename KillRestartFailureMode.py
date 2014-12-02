from IFailureMode import IFailureMode
from StaticClusterConfigProvider import StaticClusterConfigProvider
from SshRemoteExecutor import SshRemoteExecutor


class KillRestartFailureMode (IFailureMode):

	def __init__ (self, hostToIsolate, killCommand, restartCommand, clusterConfigProvider):
		self.hostToIsolate = hostToIsolate
		self.ipToIsolate = clusterConfigProvider.getHostIP(hostToIsolate)
		self.killCommand = killCommand
		self.restartCommand = restartCommand
		self.clusterConfigProvider = clusterConfigProvider

	def doFailure(self, args = None):
		self.runProcess (self.killCommand)

	def doRecovery(self, args = None):
		self.runProcess (self.restartCommand)

	def runProcess(self, command):
		hostConfig = self.clusterConfigProvider.getHostConfig(self.hostToIsolate)
		authorized_user = hostConfig['authorized_user']
		addMissingKeys = True
		timeout = 10000
		executor = SshRemoteExecutor(self.hostToIsolate, authorized_user, addMissingKeys, timeout)
		executor.execCommandAsync(command)
		

IFailureMode.register(KillRestartFailureMode)

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


	restartCmd = 'sudo /opt/kafka/bin/kafka-server-start.sh /opt/kafka/config/server.properties > /tmp/oo  2>&1 &'
	killCmd = "ps -effw | grep kafka | grep -v grep | awk '{print $2}' | xargs sudo kill -9"

	isolateNodeFailureMode = KillRestartFailureMode('n1', killCmd, restartCmd, clusterConfigProvider)
	isolateNodeFailureMode.doFailure()

	raw_input()
	isolateNodeFailureMode.doRecovery()

if __name__ == "__main__":
    main()


	