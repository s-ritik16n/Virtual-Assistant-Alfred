import datetime
import time
import smtplib
import subprocess
from sys import argv
import os

def reminder(comm,listener,talker,list_pass):
	direc='d:\\reminders\\'
	dt=datetime.datetime.now()
	rem=open(direc+comm[1]+' '+''+dt.strftime('%d-%m-%Y %H-%M-%p')+'.txt','w')
	rem.write(' '.join(comm[2:]))
	#sub=subprocess.Popen(['c:\\windows\\notepad.exe',rem.name])
	print rem.name
	rem.close()
	smtpobj=smtplib.SMTP('smtp.gmail.com',587)
	smtpobj.ehlo()
	smtpobj.starttls()
	smtpobj.login(listener,list_pass)
	smtpobj.sendmail(listener,talker,'Subject: Reminder '+comm[1]+' saved.\n'+"""
		
		
		"""+' '.join(comm[2:]))
	smtpobj.quit()
	return True
	
