import datetime
import time
import subprocess
from sys import argv
import os

def display(comm,listener,talker,list_pass):

	direc='d:\\display\\'

	dt=datetime.datetime.now()
	rem=open(direc+comm[1]+' '+''+dt.strftime('%d-%m-%Y %H-%M-%p')+'.txt','w')
	rem.write(' '.join(comm[2:]))
	n=rem.name
	rem.close()
	sub=subprocess.Popen(['c:\\windows\\notepad.exe',n])
	for i in range(5):
		time.sleep(2)
	sub.terminate()

	
