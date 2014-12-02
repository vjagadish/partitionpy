from IRemoteExecutor import IRemoteExecutor
import paramiko
import logging
import socket

class SshRemoteExecutor (IRemoteExecutor):

	def __init__ (self, hostname, username, addMissingKeys, timeout):
		self.hostname = hostname	
		self.username = username
		self.addMissingKeys = addMissingKeys
		self.timeout = timeout
		print 'Configured executor with hostname: %s  username : %s ' %(hostname, username)
    

	def execCommandAsync (self, command):
		ssh = paramiko.SSHClient()

		if self.addMissingKeys:
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

		try: 
			print 'Running command asynchronously: %s on host %s' %(command, self.hostname)

			ssh.connect(self.hostname, username=self.username, timeout = self.timeout)

		except (paramiko.SSHException, socket.error) as e:
			logging.exception('Ssh Connection error')
			raise e	

		ssh.exec_command(command)


	def execCommand(self, command):
		ssh = paramiko.SSHClient()

		if self.addMissingKeys:
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

		try: 
			print 'Running command: %s on host %s' %(command, self.hostname)

			ssh.connect(self.hostname, username=self.username, timeout = self.timeout)

		except (paramiko.SSHException, socket.error) as e:
			logging.exception('Ssh Connection error')
			raise e	

		stdin, stdout, stderr = ssh.exec_command(command)
		status =  stdout.channel.recv_exit_status()
		print 'Status of command: %s on host %s is %s' %(command, self.hostname, status)

		output = stdout.readlines()
		print output

		error = stderr.readlines()
		print error

		ssh.close()

		return status, output


	def getUser(self):
		return self.username


	def getHost(self):	
		return self.hostname	

IRemoteExecutor.register(SshRemoteExecutor)

def main():
	sshc = SshRemoteExecutor('n1', 'ec2-user', True, 1000)
	print sshc.getUser()
	print sshc.getHost()
	code, output = sshc.execCommand ('uptime')
	print code, output

if __name__ == "__main__":
    main()




