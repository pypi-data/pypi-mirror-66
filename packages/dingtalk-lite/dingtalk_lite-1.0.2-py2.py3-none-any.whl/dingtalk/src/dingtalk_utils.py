#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading

from dingtalk.src.dingtalk_client import Client

DEFAULT_API_URL = "https://oapi.dingtalk.com/robot/send"


class DingtalkUtils(object):
    is_silent = False
    api_url = DEFAULT_API_URL

    @staticmethod
    def send_text_message(token, message, at_mobiles=None, is_at_all=False):
        if DingtalkUtils.is_silent:
            print(message)
            return

        client = Client(DingtalkUtils.api_url)
        response = client.send_text(token, message, at_mobiles, is_at_all)
        print(response)

    @staticmethod
    def send_text_message_async(token, message, at_mobiles=None, is_at_all=False):
        thread = SendTextMessageThread("Thread-SendTextMessage", token, message, at_mobiles, is_at_all)
        thread.start()

    @staticmethod
    def send_markdown_message(token, title, text, at_mobiles=None, is_at_all=False):
        if DingtalkUtils.is_silent:
            print(text)
            return

        client = Client(DingtalkUtils.api_url)
        response = client.send_markdown(token, title, text, at_mobiles, is_at_all)
        print(response)

    @staticmethod
    def send_markdown_message_async(token, title, text, at_mobiles=None, is_at_all=False):
        thread = SendMarkdownMessageThread("Thread-SendMarkdownMessage", token, title, text, at_mobiles, is_at_all)
        thread.start()


class SendTextMessageThread(threading.Thread):
    def __init__(self, name, token, message, at_mobiles=None, is_at_all=False):
        threading.Thread.__init__(self)
        self.name = name
        self.token = token
        self.message = message
        self.at_mobiles = at_mobiles
        self.is_at_all = is_at_all

    def run(self):
        DingtalkUtils.send_text_message(self.token, self.message, self.at_mobiles, self.is_at_all)


class SendMarkdownMessageThread(threading.Thread):
    def __init__(self, name, token, title, text, at_mobiles=None, is_at_all=False):
        threading.Thread.__init__(self)
        self.name = name
        self.token = token
        self.title = title
        self.text = text
        self.at_mobiles = at_mobiles
        self.is_at_all = is_at_all

    def run(self):
        DingtalkUtils.send_markdown_message(self.token, self.title, self.text, self.at_mobiles, self.is_at_all)
