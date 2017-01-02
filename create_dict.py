import os
import shelve

def get_dict(inp):
	#get the dictionary of count of trigrams
	dict={}
	lis=inp.split(' ')
	for str in lis:
		str=str.lower()
		if len(str)>=3:
			for i in range(len(str)-2):
				dict.setdefault(str[i:i+3],0)
				dict[str[i:i+3]]+=1
		
		else:
			dict.setdefault(str,0)
			dict[str]+=1
	return dict
	

def update_lib():
	#getting the songs list and creating a tri gram dictionary
	lis=os.listdir('d:\\song_downloads')
	lis=[x.strip('.mp3') for x in lis if x.endswith('.mp3')]
	dict_of_song={}
	for str in lis:
		dict=get_dict(str)
		dict_of_song[str]=dict

	# getting the videos list and creating a tri gram dictionary
	shelfile=shelve.open('mydata')
	shelfile['songs']=dict_of_song
	
	
	lis=os.listdir('d:\\video_downloads')
	lis=[x.strip('.mp4') for x in lis if x.endswith('.mp4')]
	#print lis[:3]
	dict_of_video={}
	for str in lis:
		dict=get_dict(str)
		dict_of_video[str]=dict
	shelfile['videos']=dict_of_video
