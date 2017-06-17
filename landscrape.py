import urllib, urllib2
import json
import sys
from os import makedirs
from os.path import join, expanduser, isfile, exists

# URLS of EarthPorn Subreddit JSON
JSON_URL_TODAY = 'http://www.reddit.com/r/earthporn.json?sort=top&limit=1'
JSON_URL_ALL_TIME = 'http://www.reddit.com/r/earthporn.json?sort=top&t=month&limit=25'

# User Agent String according to Reddit's rules for accessing API: https://github.com/reddit/reddit/wiki/API
USER_AGENT_STRING = {'User-Agent': 'osx:r/EarthPorn.wallpaper.fetcher:v1.0 (by /u/beetchu)'}

# Directory to save wallpaper downloads
# Leave WALLPAPER_DIRECTORY empty to use default directory: /Users/USERNAME/Pictures/EarthPorn Wallpapers
WALLPAPER_DIRECTORY = ''

# Image size tuple (WIDTH, HEIGHT) in pixels
# If set, script will only download images of that specific size
# Leave IMAGE_SIZE empty to download images of any size
# IMAGE_SIZE = ()

# Applescript to change desktop background
SCRIPT_TO_SET_WALLPAPER = """/usr/bin/osascript<<END
tell application "Finder"
set desktop picture to POSIX file "%s"
end tell
END"""

def print_help_message():
    help_message = """
    EarthPorn Wallpaper Fetcher for Mac OS 
    version 1.0     June 2017
    by Sharon Gao   github.com/segao
    
    Usage:
    python landscrape.py [option]
    
    no argument         download the top upvoted image in the past 24 hours and set it as current wallpaper
    -dl                 download the top 25 upvoted images from all time and set the first as current wallpaper
    -help               display this help message
    """
    print(help_message)
    sys.exit()

def get_wallpaper_path(wallpaper_name):
    if WALLPAPER_DIRECTORY.strip() != '': # Remove whitespace
        directory = WALLPAPER_DIRECTORY
    else:
        directory = join(expanduser("~"), 'Pictures/EarthPorn Wallpapers')
    
    if not exists(directory): # Check if directory already exists
        makedirs(directory)   # If not, create new directory
    
    wallpaper_path = join(directory, wallpaper_name)
    return wallpaper_path
    
    
def request_data(url):
    try:
        response = urllib2.Request(url, headers = USER_AGENT_STRING)
        json_data = urllib2.urlopen(response).read() # JSON encoded page data
        data = json.loads(json_data) # Converted page data
    except urllib2.HTTPError, e:
        print('The server could not fulfill the request.')
        print('Error Code: ' + str(e.code))
    except urllib2.URLError, e:
        print('Failed to reach server.')
        print('Reason: ' + str(e.reason))
    download_wallpaper(data)

def download_wallpaper(data):
    is_first_image = 1
    for post in data["data"]["children"]: # Iterate through JSON URLs
        wallpaper_name = i["data"]["title"] + ".jpg" # Create file name based on post title 
        wallpaper_path = get_wallpaper_path(wallpaper_name) # Create file path by calling get_wallpaper_path()
        wallpaper_url = i["data"]["url"] # Fetch image url 
        
        if wallpaper_url[7:12] == "imgur": # Adjusts imgur links to direct image links 
            wallpaper_url += ".jpg" # Ex: http://imgur.com/CG6ihHk -> http://imgur.com/CG6ihHk.jpg
            
        wallpaper_thumbnail = i["data"]["thumbnail"] # Grab thumbnail data
        # From Reddit JSON API:
        # full URL to the thumbnail for this link
        # "self" if this is a self post (Note: self post = text post)
        # "image" if this is a link to an image but has no thumbnail
        # "default" if a thumbnail is not available
        if wallpaper_thumbnail == "self" or wallpaper_thumbnail == "default": # Ignore text/non-image posts
            continue
        try:
            print("Fetching: " + wallpaper_url)
            response = urllib2.Request(wallpaper_url)
            wallpaper_data = urllib2.urlopen(response).read()
            
            if isfile(wallpaper_path):
                print(wallpaper_name + " already exists.")
            else:
                urllib.urlretrieve(wallpaper_url, wallpaper_path)
                print(wallpaper_name + " successfully downloaded.")        
        except: # If image url is invalid, skip
            pass
        
        if is_first_image == 1:
            set_wallpaper(wallpaper_path)
        is_first_image = 0
    
# Set Mac Wallpaper
# Taken from: http://stackoverflow.com/questions/431205/how-can-i-programatically-change-the-background-in-mac-os-x
def set_wallpaper(wallpaper_path):
    if isfile(wallpaper_path):
        import subprocess
        subprocess.Popen(SCRIPT_TO_SET_WALLPAPER%wallpaper_path, shell = True)      
    
def main():
    if len(sys.argv) == 1:
        url = JSON_URL_TODAY
        request_data(url)
    elif len(sys.argv) == 2:
        if sys.argv[1] == '-dl':
            url = JSON_URL_ALL_TIME
            request_data(url)
        elif sys.argv[1] == '-help':
            print_help_message()
        else:
            print('Invalid argument.')
            print_help_message()
    else:
        print_help_message()
        
if __name__ == '__main__':
    main()