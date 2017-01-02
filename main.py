import getpass
import smtplib
import pyzmail
import Queue
import download
import reminder
import display
import play
from threading import Thread
import time
from imapclient import IMAPClient,SEEN
import datetime
import logging
import shutil
print '''
		THE ASSISTANT IS NOW ONLINE:
	'''
inst_queue=Queue.Queue()
def worker_threads():
	dt=datetime.datetime.now()
	strdt=dt.strftime('%d-%b-%Y')
	logging_file='d:\\logs\\log of '+strdt+'.txt'
	logging.basicConfig(filename=logging_file,level=logging.DEBUG,format='%(asctime)s - %(levelname)s - %(message)s')
	ch=0
	while ch==0:
		while inst_queue.empty():
			time.sleep(2)
		while not inst_queue.empty() and ch==0:
			lis=inst_queue.get()
			comm=lis[0]
			listener=lis[1]
			talker=lis[2]
			list_pass=lis[3]
			attempt=lis[4]
			#print comm
			#print listener
			#print list_pass
			if attempt<2:
				if comm[0]=='quit':
					ch=1
				elif comm[0]=='download':
					try:
						download.download(comm,listener,talker,list_pass)
						logging.debug(' '.join(comm[1:])+'  download complete')
					except:
						logging.debug('exception occurred in download task re-queued')
						try:
							if comm[1]=='song':
								shutil.rmtree('d:\\song_downloads\\'+' '.join(comm[2:]))
							else:
								shutil.rmtree('d:\\video_downloads\\'+' '.join(comm[2:]))
						except:
							pass
						print 'task re-queued'
						inst_queue.put([comm,listener,talker,list_pass,attempt+1])
				elif comm[0]=='reminder':
					try:
						reminder.reminder(comm,listener,talker,list_pass)
						logging.debug('reminder set')
					except:
						logging.debug('exception occurred in reminder task re-queued')
						print 'task re-queued'
						inst_queue.put([comm,listener,talker,list_pass,attempt+1])
				elif comm[0]=='display':
					try:
						t=Thread(target=display.display,args=[comm,listener,talker,list_pass])
						t.start()
					except:
						logging.debug('exeption occurred in display task requeued')
						inst_queue.put([comm,listener,talker,list_pass,attempt+1])
				elif comm[0]=='play':
					try:
						play.play(comm[1:])
					except:
						logging.debug('exception occurred in reminder task re-queued')
						print 'task re-queued'
						inst_queue.put([comm,listener,talker,list_pass,attempt+1])
				else:
					smtpobj=smtplib.SMTP('smtp.gmail.com',587)
					smtpobj.ehlo()
					smtpobj.starttls()
					smtpobj.login(listener,list_pass)
					smtpobj.sendmail(listener,talker,'Subject:COMMAND NOT RECOGNIZED.\n'+' '.join(comm))
					smtpobj.quit()
				inst_queue.task_done()
			else:
				smtpobj=smtplib.SMTP('smtp.gmail.com',587)
				smtpobj.ehlo()
				smtpobj.starttls()
				smtpobj.login(listener,list_pass)
				smtpobj.sendmail(listener,talker,'Subject:I\'am afraid the ttask could not be completed.\n'+' '.join(comm))
				smtpobj.quit()
				inst_queue.task_done()
			
			
		
for i in range(2):		
	t1=Thread(target=worker_threads)
	t1.start()
		

dt=datetime.datetime.now()
strdt=dt.strftime('%d-%b-%Y')
logging_file='d:\\logs\\log of '+strdt+'.txt'
logging.basicConfig(filename=logging_file,level=logging.DEBUG,format='%(asctime)s - %(levelname)s - %(message)s')
logging.debug('ASSISTANT SESSION STARTED')
listener=''
talker=''
passw=''
try:
	smtpobj= smtplib.SMTP('smtp.gmail.com',587)
	smtpobj.ehlo()
	smtpobj.starttls()
except:
	logging.debug('server login failed')
while True:
	print '\nENTER THE EMAIL ADDRESS FOR THE LISTENER EMAIL'
	listener=raw_input()
	logging.debug('listener: '+listener)
	print 'ENTER THE PASSWORD FOR THE LISTENER EMAIL ID'
	passw=getpass.getpass()
	#print passw

	try:
		smtpobj.login(listener,passw)
		print 'ENTER THE TALKER EMAIL ADDRESS'
		talker=raw_input()
		logging.debug('talker: '+talker)
		smtpobj.sendmail(listener,talker,'Subject:ALFRED AT YOUR SERVICE.\n')
		print 'successfull login. Waiting for commands...'
		logging.debug('listener login successfull')
		break;
	except smtplib.SMTPAuthenticationError:
		print 'incorrect login credentials'
		logging.debug('listener logging failed trying again')

imapobj=IMAPClient('imap.gmail.com',ssl=True)
imapobj.login(listener,passw)
imapobj.select_folder('INBOX')
UIDs=imapobj.search(['ON '+strdt,'UNSEEN','FROM '+talker])
ch=0
while ch==0:
	while len(UIDs)==0:
		time.sleep(5)
		imapobj.select_folder('INBOX')
		UIDs=imapobj.search(['ON '+strdt,'UNSEEN','FROM '+talker])
#print UIDs
	for uid in UIDs:
		rawmessages=imapobj.fetch([uid],['BODY[]','FLAGS'])
		message=pyzmail.PyzMessage.factory(rawmessages[uid]['BODY[]'])
		msg_sub=message.get_subject()
		print msg_sub
		msg=message.text_part.get_payload().decode(message.text_part.charset)
		msg=msg.strip()
		print 'COMMAND RECIEVED:'
		print msg
		comms=msg.split('\n')
		for commstr in comms:
			commstr=commstr.strip()
			logging.debug('COMMAND: '+commstr)
			comm=commstr.split(' ')
			comm[0]=comm[0].lower()
			if comm[0]=='quit':
				for i in range(2):
					inst_queue.put([['quit'],listener,talker,passw,0])
				ch=1
				break;
			else:
				inst_queue.put([comm,listener,talker,passw,0])
				
			if ch==1:
				inst_queue.join()
				break;
	imapobj.delete_messages(UIDs)
	UIDs=[]

try:
	smtpobj= smtplib.SMTP('smtp.gmail.com',587)
	smtpobj.ehlo()
	smtpobj.starttls()
	smtpobj.login(listener,passw)
	smtpobj.sendmail(listener,talker,'Subject:ALFRED OFFLINE. THANK YOU\n')		
	imapobj.logout()
	smtpobj.quit()

except smtplib.SMTPAuthenticationError:
		print 'incorrect login credentials'
		logging.debug('listener logging failed')


