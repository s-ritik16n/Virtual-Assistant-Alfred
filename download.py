import os
import sys
import time
import pyautogui
import smtplib
import shutil
import shelve
from selenium import webdriver
import play
import create_dict
from threading import Thread
def count_file_type(direc,ext):
	ctr=0
	for i in os.listdir(direc):
		if i.endswith(ext):
			ctr=ctr+1
		
	return ctr

def download(comm,listener,talker,list_pass):
	final_direc=''
	direc=''
	chromeopt= webdriver.ChromeOptions()
	if comm[1]=='song':
		final_direc="d:\\song_downloads"
		direc="d:\\song_downloads\\"+' '.join(comm[2:])
		os.makedirs("d:\\song_downloads\\"+' '.join(comm[2:]))
		prefs={"download.default_directory":direc}
		format='.mp3'
		wait=60
	else:
		final_direc="d:\\video_downloads"
		direc="d:\\video_downloads\\"+' '.join(comm[2:])
		os.makedirs("d:\\video_downloads\\"+' '.join(comm[2:]))
		prefs={"download.default_directory":direc}
		format='.mp4'
		wait=120

	curr=count_file_type(direc,format)

	chromeopt.add_experimental_option("prefs",prefs)
	browser=webdriver.Chrome(chrome_options=chromeopt)
	#for hiding uncomment-
	browser.set_window_position(-2000,0)
	browser.get('http://google.com/search?q='+' '.join(comm[2:]))
	res=browser.find_element_by_class_name('_Rm')
	link=res.text
	#browser.get(res.text)-This is the YouTube link found from the first result form websearch
	#res.click()
	browser.get('http://www.onlinevideoconverter.com/video-converter')
	res=browser.find_element_by_id('texturl')
	res.send_keys(link)
	res=browser.find_element_by_class_name('selectbox')
	res.click()
	res=browser.find_element_by_partial_link_text(format)
	res.click()
	res=browser.find_element_by_class_name('start-button')
	res.click()
	time.sleep(20)
	print browser.current_url
	res=browser.find_element_by_id('downloadq')
	res.click()
	while curr==count_file_type(direc,format):
		time.sleep(5)	
	browser.quit()
	lis=os.listdir(direc)
	name=lis[0]
	shutil.move(direc+'\\'+name,final_direc)
	os.rmdir(direc)
	smtpobj=smtplib.SMTP('smtp.gmail.com',587)
	smtpobj.ehlo()
	smtpobj.starttls()
	smtpobj.login(listener,list_pass)
	smtpobj.sendmail(listener,talker,'Subject:'+comm[1]+' download completed'+"""
		
		
		"""+name)
	smtpobj.quit()
	
	
	
	
	
	
	
	

