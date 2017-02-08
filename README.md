# Alfred (Virtual-Assistant)
This is a mini Virtual Assistant (named Alfred) for automating basic tasks.

The Assistant is commanded via email, and hence, is independent of limitations of proximity.

The current tasks are:
  1. Downloads Songs and Videos.
    (_The downloaded content is not meant for commercial purpose_)
  2. Play Songs and Videos from your library
    (_finds the best match and plays the file, or Queues it automatically._)
  3. Set a display message that lasts for 10 seconds.
  4. Set a reminder.
  
###Milestones:
1. setting up a multi user interface and multi assistant interface.
2. using Speech recognition for commands
3. make the following folder on the host computer:
 - d:/song_downloads
 - d:/video_downloads
 - d:/logs
 - d:/reminders
 - d:/display

###Usage of Speech Recognition
1. input the listener email id and password
2. input the talker email address
3. send commands from talker to listener of the form:
 - download song `song name`
 - download video `video name`
 - reminder `title` `message`
 - display `title` `message`
 - quit

**Also**: commands are separated by a new line character

