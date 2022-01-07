import os
import shutil
import sys
import youtube_dl
import eyed3
from eyed3.id3.frames import ImageFrame

from typing import Any, Dict
from downloader_utils import AUDIO_DIR, VIDEO_DIR, FRAME_DIR, DEFAULT_AUDIO_DL_OPT, DEFAULT_VIDEO_DL_OPT, DownloadInfo, CoverType, URL_ID_REGEX

class Downloader:
    def __init__(self, dl_path: str = None, audio_dl_opt: Dict[str, Any] = DEFAULT_AUDIO_DL_OPT, video_dl_opt: Dict[str, Any] = DEFAULT_VIDEO_DL_OPT):
        if dl_path:
            self.dl_path = dl_path
        else:
            curr_dir = "." if sys.argv[0] == os.path.basename(__file__) else sys.argv[0][:sys.argv[0].rfind('/')]
            self.dl_path = f"{curr_dir}/Downloads"
        self.temp_path = f"{self.dl_path}/TEMP"

        if os.path.exists(self.temp_path):
            shutil.rmtree(self.temp_path)

        self.audio_dl_opt = audio_dl_opt
        self.video_dl_opt = video_dl_opt


    def _dl_audio(self, url: str): #todo start, end time
        curr_audio_dl_opt = dict(self.audio_dl_opt)
        curr_audio_dl_opt['outtmpl'] = f'{self.temp_path}/%(id)s/{AUDIO_DIR}/%(id)s.%(ext)s'
        with youtube_dl.YoutubeDL(curr_audio_dl_opt) as ydl:
            ydl.download([url])

        id = URL_ID_REGEX.match(url).groups()[0]
        dl_path = f'{self.temp_path}/{id}/{AUDIO_DIR}/'
        dl_path_files = [f for f in os.listdir(dl_path) if os.isfile(os.join(dl_path, f))]
        assert len(dl_path_files) == 1
        return dl_path_files[0]

    def _dl_video(self, url: str):
        curr_video_dl_opt = dict(self.video_dl_opt)
        curr_video_dl_opt['outtmpl'] = f'{self.temp_path}/%(id)s/{VIDEO_DIR}/%(id)s.%(ext)s'
        with youtube_dl.YoutubeDL(curr_video_dl_opt) as ydl:
            ydl.download([url])

        id = URL_ID_REGEX.match(url).groups()[0]
        dl_path = f'{self.temp_path}/{id}/{VIDEO_DIR}/'
        dl_path_files = [f for f in os.listdir(dl_path) if os.isfile(os.join(dl_path, f))]
        assert len(dl_path_files) == 1
        return dl_path_files[0]

    def _dl_video_frame(self, url: str):
        video_path = self._dl_video(url)

        id = URL_ID_REGEX.match(url).groups()[0]
        frame_dir_path = f"{self.temp_path}/{id}/{FRAME_DIR}"
        frame_path = f"{frame_dir_path}/{id}.png"

        os.mkdir(frame_dir_path)
        os.system(f'ffmpeg -ss 0 -i {video_path} -frames:v 1 {frame_path} -hide_banner -loglevel error')
        return frame_path

    def _write_metadata(self, audio_path: str, cover_path: str = None):
        audiofile = eyed3.load(audio_path)
        if not audiofile.tag:
            audiofile.initTag()


        if cover_path:
            audiofile.tag.images.set(ImageFrame.FRONT_COVER, open(cover_path,'rb').read(), f'image/png')

    def download(self, downloadInfo: DownloadInfo):
        audio_path = self._dl_audio(downloadInfo.audio_url)

        if downloadInfo.cover_type == CoverType.VIDEO_FRAME:
            self._dl_video_frame(downloadInfo.cover_url)

        self._write_metadata(audio_path)

