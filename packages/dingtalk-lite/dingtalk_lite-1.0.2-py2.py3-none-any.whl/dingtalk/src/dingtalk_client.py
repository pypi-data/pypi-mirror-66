#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

import requests

ACTION_CARD_NOT_HIDE_AVATAR = "0"
ACTION_CARD_HIDE_AVATAR = "1"
ACTION_CARD_BTN_ORIENTATION_V = "0"
ACTION_CARD_BTN_ORIENTATION_H = "1"


class ActionCardButton(object):
    title = ''
    action_url = ''

    def __init__(self, title, url):
        self.title = title
        self.action_url = url

    def to_json(self):
        return {
            "title": self.title,
            "actionURL": self.action_url
        }


class FeedCardLink(object):
    title = ''
    message_url = ''
    pic_url = ''

    def __init__(self, title, message_url, pic_url):
        self.title = title
        self.message_url = message_url
        self.pic_url = pic_url

    def to_json(self):
        return {
            "title": self.title,
            "messageURL": self.message_url,
            "picURL": self.pic_url
        }


class Client(object):
    url = ''

    def __init__(self, url):
        self.url = url

    def send_text(self, token, content, at_mobiles=None, is_at_all=False):
        """
        # :param at_mobiles: ['138xxxxxxxx', '139xxxxxxxx']
        """

        data = {
            "msgtype": "text",
            "text": {
                "content": content
            },
            "at": {
                "atMobiles": at_mobiles,
                "isAtAll": is_at_all
            }
        }

        return self._get_response(token, data)

    def send_link(self, token, title, text, message_url, pic_url=None):
        data = {
            "msgtype": "link",
            "link": {
                "text": text,
                "title": title,
                "picUrl": pic_url,
                "messageUrl": message_url
            }
        }

        return self._get_response(token, data)

    def send_markdown(self, token, title, text, at_mobiles=None, is_at_all=False):
        """
        # :param text: markdown format content
        # :param at_mobiles: ['138xxxxxxxx', '139xxxxxxxx']
        """

        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": text
            },
            "at": {
                "atMobiles": at_mobiles,
                "isAtAll": is_at_all
            }
        }

        return self._get_response(token, data)

    def send_single_actioncard(self, token, title, text, single_title, single_url,
                               hide_avatar=ACTION_CARD_NOT_HIDE_AVATAR,
                               btn_orientation=ACTION_CARD_BTN_ORIENTATION_V):
        """
        # :param text: markdown format content
        """

        data = {
            "msgtype": "actionCard",
            "actionCard": {
                "title": title,
                "text": text,
                "hideAvatar": hide_avatar,
                "btnOrientation": btn_orientation,
                "singleTitle": single_title,
                "singleURL": single_url
            }
        }

        return self._get_response(token, data)

    def send_multi_actioncard(self, token, title, text, btns,
                              hide_avatar=ACTION_CARD_NOT_HIDE_AVATAR,
                              btn_orientation=ACTION_CARD_BTN_ORIENTATION_V):
        """
        # :param text: markdown format content
        # :param btns: [ActionCardButton(), ActionCardButton()]
        """

        data = {
            "msgtype": "actionCard",
            "actionCard": {
                "title": title,
                "text": text,
                "hideAvatar": hide_avatar,
                "btnOrientation": btn_orientation,
                "btns": []
            }
        }

        for btn in btns:
            obj = btn.to_json()
            data['actionCard']['btns'].append(obj)

        return self._get_response(token, data)

    def send_feedcard(self, token, links):
        """
        # :param links: [FeedCardLink(), FeedCardLink()]
        """

        data = {
            "msgtype": "feedCard",
            "links": []
        }

        for link in links:
            obj = link.to_json()
            data['links'].append(obj)

        return self._get_response(token, data)

    def _get_response(self, token, data):
        headers = {
            "Content-Type": "application/json"
        }

        json_data = json.dumps(data)

        full_url = "%s?access_token=%s" % (self.url, token)
        response = requests.post(url=full_url, data=json_data, headers=headers)
        return response
