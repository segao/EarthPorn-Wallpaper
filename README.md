# Landscrape
A python script that downloads the top upvoted images from the nature and landscape subreddit, [/r/EarthPorn](https://reddit.com/r/EarthPorn), and sets it as your current Mac OS wallpaper.

# About
This script uses the existing Reddit JSON API. Instructions for its use can be found [here](https://github.com/reddit/reddit/wiki/API).
[This](http://stackoverflow.com/questions/431205/how-can-i-programatically-change-the-background-in-mac-os-x) particular Stack Overflow post helped me code how to change the Mac wallpaper.

A custom directory path can be used, otherwise all images will be saved to <b>'/Users/USERNAME/Pictures/EarthPorn Wallpapers'</b>. Changing the JSON URLs to another image based subreddit should fetch the top posts from that specific subreddit.

# Usage
Download and set today's top post as wallpaper:
```
python landscrape.py
```

Download the top 25 posts of the last month and set the first as wallpaper using `-dl`. Add the directory to your System Preferences to allow automatic wallpaper changes.
```
python landscrape.py -dl
```
Display help message:
```
python landscrape.py -help
```
