from sys import argv
import shelve
from subprocess import Popen
import create_dict



def compare(dict1,dict2):
	distance=0
	for k in dict1.keys():
		distance+= dict1[k]*dict2.get(k,0)
	distance=float(distance)/len(dict1)
	return distance


def play(comm):
	create_dict.update_lib()
	data=shelve.open('mydata')
	app=''
	file=''
	app='c:\\program files\\VideoLAN\\VLC\\vlc.exe'
	if comm[0]=='song':
		max_match=0.025
		song=['none']
		dict1=create_dict.get_dict(' '.join(comm[1:]))
		dict=data['songs']
		for key in dict.keys():
			dict2=dict[key]
			res=compare(dict1,dict2)
			if max_match<res:
				max_match=res
				song=[]
				song.append(key)
			elif max_match==res:
				song.append(key)
		if song[0]!='none':
			file='d:\\song_downloads\\'+song[0]+'.mp3'
			print file
			Popen([app,file])
		else:
			print 'No such song found'
	else:
		max_match=0.025
		video=['none']
		dict1=create_dict.get_dict(' '.join(comm[1:]))
		dict=data['videos']
		for key in dict.keys():
			dict2=dict[key]
			res=compare(dict1,dict2)
			if max_match<res:
				max_match=res
				video=[]
				video.append(key)
			elif max_match==res:
				video.append(key)
		if video[0]!='none':
			file='d:\\video_downloads\\'+video[0]+'.mp4'
			print file
			Popen([app,file])
		else:
			print 'No such video found'
#comm=argv[1:]
#play(comm)
#str1=raw_input('enter the string 1')
#str2=raw_input('Enter the string 2')

#dict1=get_dict(str1)
#dict2=get_dict(str2)

#print compare(dict1,dict2)
