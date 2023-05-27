import os, ffmpeg, shutil
from pytube import YouTube

class Downloader:
    def __download_audio(self, url, path):
        mov = YouTube(url)
        streams = mov.streams.filter(type='audio')
        stream = streams[0]
        max_abr = int(streams[0].abr[:streams[0].abr.find('kbps')])
        for s in streams:
            abr = int(s.abr[:s.abr.find('kbps')])
            if max_abr < abr:
                stream = s
                max_abr = abr
        title = stream.title.replace('/', '').replace(',', '')
        if not os.path.isfile(f'{path}/{title}.webm'):
            stream.download(f'{path}/')
        return title

    def audio(self, url):
        return self.__download_audio(url, './music')

    def video(self, url):
        mov = YouTube(url)
        streams = mov.streams.filter(type='video')
        stream = streams[0]
        max_fps = int(streams[0].fps)
        max_res = int(streams[0].resolution[:streams[0].resolution.find('p')])
        for s in streams:
            fps = int(s.fps)
            res = int(s.resolution[:s.resolution.find('p')])
            if s.mime_type == 'video/webm' and max_fps < fps and max_res < res:
                stream = s
                max_fps = fps
                max_res = res
        title = stream.title.replace('/', '').replace(',', '')
        if not os.path.isfile(f'./videos/{title}.webm'):
            if not os.path.isdir('./tmp/video'):
                os.makedirs('./tmp/video')
                stream.download('./tmp/video/')
            if not os.path.isdir('./tmp/audio'):
                os.makedirs('./tmp/audio')
            self.__download_audio(url, './tmp/audio')

            video = ffmpeg.input(f'./tmp/video/{title}.webm')
            audio = ffmpeg.input(f'./tmp/audio/{title}.webm')
            ffmpeg.output(video, audio, f'./videos/{title}.webm').run(capture_stderr=True)

            shutil.rmtree('./tmp')
        return title
