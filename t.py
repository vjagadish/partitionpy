import paramiko
import threading
import time
from threading import Timer
import sched

def print_time(x):
	print "From print_time %s  ", str(x)

def foo():
	print time.time()
	x=1
	Timer(5, print_time, (x,)).start()
	Timer(10, print_time, (x,)).start()
	time.sleep(11)

#foo()




