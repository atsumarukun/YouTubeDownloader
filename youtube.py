import os
from pytube import YouTube

class Downloader:
    def audio(self, url):
        mov = YouTube(url)
        streams = mov.streams.filter(type='audio')
        stream = streams[0]
        max_abr = int(streams[0].abr[:streams[0].abr.find('kbps')])
        for s in streams:
            abr = int(s.abr[:s.abr.find('kbps')])
            if max_abr < abr:
                stream = s
                max_abr = abr
        if not os.path.isfile(f'./music{stream.title}.webm'):
            stream.download('./music')
        return stream.title.replace('/', '').replace(',', '')