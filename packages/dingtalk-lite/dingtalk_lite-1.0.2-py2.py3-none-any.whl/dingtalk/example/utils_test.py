#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dingtalk.src.dingtalk_utils import DingtalkUtils

token = 'your-dingtalk-robot-token'


def test_text():
    DingtalkUtils.is_silent = True
    DingtalkUtils.api_url = '127.0.0.1:8000/api/dingtalk/message'
    DingtalkUtils.send_text_message(token,
                                    "[Ambari Alert] This is a test message, do not worry.")


def test_text_async():
    DingtalkUtils.is_silent = False
    DingtalkUtils.send_text_message_async(token,
                                          "[Ambari Alert] This is a test message, do not worry.")


def test_markdown():
    DingtalkUtils.is_silent = True
    text = "### I am the header\n" + \
           "#### This is a test message, do not worry.\n" + \
           "![girl](https://c-ssl.duitang.com/uploads/item/201605/08/20160508134621_KjzNa.thumb.700_0.gif)\n" + \
           "1. 图片链接1\n" + \
           "2. 图片链接2\n"
    DingtalkUtils.send_markdown_message(token, '[Ambari Alert]', text)


def test_markdown_async():
    text = "### I am the header\n" + \
           "#### This is a test message, do not worry.\n" + \
           "![girl](https://c-ssl.duitang.com/uploads/item/201605/08/20160508134621_KjzNa.thumb.700_0.gif)\n" + \
           "1. 图片链接1\n" + \
           "2. 图片链接2\n"
    DingtalkUtils.send_markdown_message_async(token, '[Ambari Alert]', text)


if __name__ == '__main__':
    test_text()
    # test_text_async()
    # test_markdown()
    # test_markdown_async()
