import os, re
from dotenv import load_dotenv

from slack import Slack
from youtube import Downloader

def response(channel, text):
    downloader = Downloader()
    pattern = 'https?://[\w/:%#\$&\?\(\)~\.=\+\-]+'
    urls = re.findall(pattern, text)
    response_text = '\n-------------------------------------\n下記をダウンロードしました.\n-------------------------------------\n'
    try:
        for url in urls:
            response_text += f'\n・{downloader.audio(url)}'
    except:
        response_text = 'ダウンロードに失敗しました.'
    return response_text

def main():
    load_dotenv()
    slack = Slack(os.environ['BOT_TOKEN'], os.environ['APP_TOKEN'], response)
    slack.run()

if __name__ == '__main__':
    main()