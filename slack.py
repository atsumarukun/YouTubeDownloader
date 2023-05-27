from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

class Slack:
    def __init__(self, token, app_token, function, *args):
        self.app = App(token=token)
        self.handler = SocketModeHandler(self.app, app_token)
        self.function = function
        self.args = args

    def __body_parser(self, body):
        userid = body['event']['user']
        channel = body['event']['channel']
        blocks = body['event']['blocks'][0]
        elements = blocks['elements'][0]
        text = ''
        for element in elements['elements']:
            if element['type'] == 'text':
                text += element['text']
            elif element['type'] == 'link':
                text += element['url']
        return userid, channel, text

    def run(self):
        @self.app.event('message')
        def EventMention(body, say, logger):
            logger.info(body)
            userid, channel, text = self.__body_parser(body)
            output = self.function(channel, text, *self.args)
            say(f'<@{userid}> {output}')

        self.handler.start()