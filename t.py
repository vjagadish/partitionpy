import paramiko
import threading

def foo():
	i=0
	while(i<10000):
		print '%s from thread %s '%(str(i), threading.current_thread().name)
		i=i+1

th1 = threading.Thread(target=foo, args=[])
th2 = threading.Thread(target=foo, args=[])
th3 = threading.Thread(target=foo, args=[])
th1.start()
th2.start()
th3.start()


