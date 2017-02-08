import sys

def main():
    if sys.platform == "linux2":
        setpaths("l")
    elif sys.platform == "win32":
        setpaths("w")

def setpaths(pref):
    if pref == "l":
        os.environ["SONGS_DIR"]=os.getenv("HOME")+"/alfred/songs/"
        os.environ["VIDEOS_DIR"]=os.getenv("HOME")+"/alfred/videos/"
        os.environ["LOG_FILE"]=os.getenv("HOME")+"/alfred/logs/log-"
        os.environ["REMINDER"] = os.getenv("HOME")+"/alfred/reminders/"
        os.environ["VLC"]="vlc"
    else:
        os.environ["SONGS_DIR"]="D:\\alfred\\songs\\"
        os.environ["VIDEOS_DIR"]="D:\\alfred\\videos\\"
        os.environ["LOG_FILE"]="D:\\alfred\\logs\\log-"
        os.environ["VLC"]="c:\\program files\\VideoLAN\\VLC\\vlc.exe"
        os.environ["REMINDER"]="d:\\reminders\\"
    os.environ["VIDEO_CONV"]="http://www.onlinevideoconverter.com/video-converter"

if __name__ == '__main__':
    main()
