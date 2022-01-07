import json
import os
import re
import sys

from downloader import Downloader
from downloader_utils import CoverType, DownloadInfo

VIDEO_URL_REGEX = re.compile(r"(https:\/\/www\.youtube\.com\/watch\?v=[A-Za-z0-9\-_]+).*")

def main():
    curr_dir = "." if sys.argv[0] == os.path.basename(__file__) else sys.argv[0][:sys.argv[0].rfind('/')]
    with open(f'{curr_dir}/test.json') as json_file:
        data = json.load(json_file)
        print(data)

        audio_urls = []
        video_urls = []

        for item in data:
            audio_url = VIDEO_URL_REGEX.match(item['audio']).groups()[0]
            audio_urls.append(audio_url)
            if 'cover_vid' in item:
                video_urls.append(item['cover_vid'])
            else:
                video_urls.append(audio_url)

        downloader = Downloader()
        downloader.download(DownloadInfo(audio_urls[0], CoverType.VIDEO_FRAME))
        # downloader.dl_audio(audio_urls[0])
        # downloader.dl_video(video_urls)

if __name__ == "__main__":
    main()