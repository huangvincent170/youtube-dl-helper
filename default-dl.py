from __future__ import unicode_literals
import requests
import shutil
import youtube_dl
import sys
import re
import os
import shutil
import eyed3
from eyed3.id3.frames import ImageFrame

if len(sys.argv) <= 1:
    print("Please input a youtube URL.")
    quit()

vid_urls = sys.argv[1:]

dirpath = "./Downloads/"
if os.path.exists(dirpath):
    shutil.rmtree(dirpath)
os.mkdir(dirpath)

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': './Downloads/temp-%(id)s.%(ext)s',
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download(sys.argv[1:])

reg = re.compile(r"https:\/\/www\.youtube\.com\/watch\?v=([A-Za-z0-9]+).*")

for vid_url in vid_urls:
    print("downloading image")
    video_id = reg.match(vid_url).groups()[0]
    image_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
    filename = image_url.split("/")[-1]
    meta = ydl.extract_info(vid_url, download=False)
    r = requests.get(image_url, stream = True)

    if r.status_code == 200:
        r.raw.decode_content = True
        
        # Open a local file with wb ( write binary ) permission.
        with open(filename,'wb') as f:
            shutil.copyfileobj(r.raw, f)
            
        print('Image sucessfully Downloaded: ',filename)
    else:
        print('Image Couldn\'t be retreived')

    id = meta['id']
    audiofile = eyed3.load(f'{dirpath}temp-{id}.mp3')
    if (audiofile.tag == None):
        audiofile.initTag()

    audiofile.tag.images.set(ImageFrame.FRONT_COVER, open(filename,'rb').read(), 'image/jpeg')
    audiofile.tag.save(version=eyed3.id3.ID3_V2_3)