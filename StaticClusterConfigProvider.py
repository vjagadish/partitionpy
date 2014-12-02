from IClusterConfigProvider import IClusterConfigProvider
import json

class StaticClusterConfigProvider:

	def __init__ (self, jsonConfigString):
		self.config = json.loads(jsonConfigString)
		print self.config


	def getConfiguredHosts(self, args=None):
		hostAliases = []
		for host in self.config:
			hostAliases.append(host['alias'])
		return hostAliases

	def getConfiguredHostIPs(self, args=None):
		hostIPs = []
		for host in self.config:
			hostIPs.append(host['ip'])
		return hostIPs

	def getAuthorizedUserName(self, hostIP, args=None):
		for host in self.config:
			if host['ip'] == hostIP:
				return host['authorized_user']
		return None

	def getHostConfig(self, alias):
		for host in self.config:
			if host['alias'] == alias:
				return host
		return None		

	def getHostIP(self, alias):
		for host in self.config:
			if host['alias'] == alias:
				return host['ip']
		return None		



IClusterConfigProvider.register(StaticClusterConfigProvider)

def main():
	jsonConfigString = """
	[
	{"alias":"n1", "ip":"172.31.40.107", "authorized_user":"ec2-user"},
	{"alias":"n2", "ip":"172.31.32.165", "authorized_user":"ec2-user"},
	{"alias":"n3", "ip":"172.31.44.108", "authorized_user":"ec2-user"},
	{"alias":"n4", "ip":"172.31.39.157", "authorized_user":"ec2-user"}
	]
	"""
	print "here"
	clusterConfigProvider = StaticClusterConfigProvider(jsonConfigString)
	print clusterConfigProvider.getConfiguredHostIPs()


if __name__ == "__main__":
    main()




