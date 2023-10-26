import os, ffmpeg, shutil
from pytube import YouTube

class Downloader:
    def __audio(self, url):
        mov = YouTube(url)
        streams = mov.streams.filter(type='audio')
        stream = streams[0]
        max_abr = int(streams[0].abr[:streams[0].abr.find('kbps')])
        for s in streams:
            abr = int(s.abr[:s.abr.find('kbps')])
            if max_abr < abr:
                stream = s
                max_abr = abr
        title = stream.title.replace('/', '').replace(',', '').replace("#", "").replace(":", "")
        if not os.path.isfile(f'./tmp/audio/{title}.webm'):
            if not os.path.isdir('./tmp/audio'):
                os.makedirs('./tmp/audio')
            stream.download(f'./tmp/audio/')
        return title

    def __video(self, url):
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
        title = stream.title.replace('/', '').replace(',', '').replace("#", "").replace(":", "")
        if not os.path.isfile(f'./tmp/video/{title}.webm'):
            if not os.path.isdir('./tmp/video'):
                os.makedirs('./tmp/video')
            stream.download('./tmp/video/')

    def music(self, url):
        title = self.__audio(url)
        if not os.path.isfile(f'./music/{title}.mp3'):
            stream = ffmpeg.input(f'./tmp/audio/{title}.webm')
            ffmpeg.output(stream, f'./music/{title}.mp3').run(capture_stderr=True)

        if os.path.isdir('./tmp'):
            shutil.rmtree('./tmp')
        return title


    def video(self, url):
        title, _ = self.__audio(url), self.__video(url)
        if not os.path.isfile(f'./videos/{title}.mp4'):
            video = ffmpeg.input(f'./tmp/video/{title}.webm')
            audio = ffmpeg.input(f'./tmp/audio/{title}.webm')
            ffmpeg.output(video, audio, f'./videos/{title}.mp4').run(capture_stderr=True)

        if os.path.isdir('./tmp'):
            shutil.rmtree('./tmp')
        return title
