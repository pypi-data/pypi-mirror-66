from abc import ABC, abstractmethod

from flask import Flask

from iabot.actions import FlaskEndPointAction


class AbstractServer:

    @abstractmethod
    def start(self, *args, **kwargs):
        pass


class HTTPServer(AbstractServer):
    def __init__(self, bot, name='iaBot', port=8000):
        self.app = Flask(name)
        self.bot = bot
        self.app.add_url_rule(
            '/',
            'bot_main_url',
            FlaskEndPointAction(self.bot.on_message)
        )

    def run(self):
        self.app.run()
