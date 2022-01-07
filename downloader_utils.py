import re
import sys

from enum import Enum, auto

URL_ID_REGEX = re.compile(r"https:\/\/www\.youtube\.com\/watch\?v=([A-Za-z0-9\-_]+).*")
AUDIO_DIR = "AUDIO"
VIDEO_DIR = "VIDEO"
FRAME_DIR = "FRAME"

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

DEFAULT_AUDIO_DL_OPT = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': "mp3",
        'preferredquality': '192',
    }],
    'logger': DlLogger(),
    'progress_hooks': [dl_hook]
}

DEFAULT_VIDEO_DL_OPT = {
    'format': 'bestvideo/best',
    # 'postprocessors': [{
    #     'key': 'FFmpegVideoConvertor',
    #     'preferedformat': VIDEO_FORMAT,
    # }],
    'logger': DlLogger(),
    'progress_hooks': [dl_hook],
}

class CoverType(Enum):
    THUMBNAIL = auto()
    VIDEO_FRAME = auto()

class DownloadInfo:
    def __init__(self, audio_url: str, cover_type: CoverType = None, cover_url: str = None, video_frame: int = None):
        self.audio_url = audio_url
        self.cover_type = cover_type
        self.cover_url = cover_url if cover_url else audio_url

