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
from PIL import Image
import cv2

VIDEO_ID_REGEX = re.compile(r"https:\/\/www\.youtube\.com\/watch\?v=([A-Za-z0-9\-_]+).*")
DIR_PATH = "./Downloads"
TEMP_PATH = f"{DIR_PATH}/temp"

class DlLogger(object):
    def debug(self, msg):
        pass
    def warning(self, msg):
        pass
    def error(self, msg):
        print(msg)

start_dl = True
dl_format = ""
def dl_hook(d):
    global start_dl, dl_format
    if d['status'] == 'downloading':
        if not start_dl:
            sys.stdout.write("\033[F")
        else:
            print(f"Begin {dl_format} Download...")
        start_dl = False
        print(d['filename'], d['_percent_str'], d['_eta_str'])
    if d['status'] == 'finished':
        print(f"Processing {dl_format}...")
        start_dl = True

AUDIO_YTDL_OPTS = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': f'{TEMP_PATH}/%(id)s.%(ext)s',
    'logger': DlLogger(),
    'progress_hooks': [dl_hook],
}

VIDEO_YTDL_OPTS = {
    'format': 'bestvideo/best',
    'outtmpl': f'{TEMP_PATH}/%(id)s.%(ext)s',
    'logger': DlLogger(),
    'progress_hooks': [dl_hook],
}

class VideoDl():
    def __init__(self, video_url):
        self.video_url = video_url
        self.video_id = VIDEO_ID_REGEX.match(video_url).groups()[0]
        self.audio_path = f'{TEMP_PATH}/{self.video_id}.mp3'
        self.video_path = f'{TEMP_PATH}/{self.video_id}.webm'
        self.image_path = f'{TEMP_PATH}/{self.video_id}.png'




if len(sys.argv) <= 1:
    print("Please input a youtube URL.")
    quit()

if os.path.exists(TEMP_PATH):
    shutil.rmtree(TEMP_PATH)
os.mkdir(TEMP_PATH)

video_dls = [VideoDl(video_url) for video_url in sys.argv[1:]]

for video_dl in video_dls:
    print(video_dl.video_url)
    dl_format = "AUDIO"
    with youtube_dl.YoutubeDL(AUDIO_YTDL_OPTS) as ydl:
        ydl.download([video_dl.video_url])
    dl_format = "VIDEO"
    with youtube_dl.YoutubeDL(VIDEO_YTDL_OPTS) as ydl:
        ydl.download([video_dl.video_url])

    success, image = cv2.VideoCapture(video_dl.video_path).read()
    if success:
        cv2.imwrite(video_dl.image_path, image)
        audiofile = eyed3.load(video_dl.audio_path)
        if not audiofile.tag:
            audiofile.initTag()
        audiofile.tag.images.set(ImageFrame.FRONT_COVER, open(video_dl.image_path,'rb').read(), 'image/png')
        audiofile.tag.save(version=eyed3.id3.ID3_V2_3)

# reg = re.compile(r"https:\/\/www\.youtube\.com\/watch\?v=([A-Za-z0-9]+).*")

# for vid_url in vid_urls:
#     print("downloading image")
#     video_id = reg.match(vid_url).groups()[0]
#     image_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
#     filename = image_url.split("/")[-1]
#     meta = ydl.extract_info(vid_url, download=False)
#     r = requests.get(image_url, stream = True)

#     if r.status_code == 200:
#         r.raw.decode_content = True
        
#         # Open a local file with wb ( write binary ) permission.
#         with open(filename,'wb') as f:
#             shutil.copyfileobj(r.raw, f)
            
#         print('Image sucessfully Downloaded: ',filename)
#     else:
#         print('Image Couldn\'t be retreived')

#     with Image.open(filename) as img:
#         left = (img.width - img.height) // 2
#         right = left + img.height
#         img = img.crop((left, 0, right, img.height))
#         img.save(filename)

    # id = meta['id']
    # audiofile = eyed3.load(f'{DIR_PATH}/temp-{vid_id}.mp3')
    # if (audiofile.tag == None):
    #     audiofile.initTag()

    # audiofile.tag.images.set(ImageFrame.FRONT_COVER, open(filename,'rb').read(), 'image/png')
    # audiofile.tag.save(version=eyed3.id3.ID3_V2_3)

# TODO
# crop thumbnail
# make it work for png thumbnails
# put in error checking
# make it work for a playlist
# make it work for multiple videos
# add checking for if it is an autogenerated video
# add more metadata to song file