#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dingtalk.src.dingtalk_client import Client, ActionCardButton, FeedCardLink


token = 'your-dingtalk-robot-token'
API_URL = "https://oapi.dingtalk.com/robot/send"

client = Client(API_URL)


def test_text():
    response = client.send_text(token,
                                "[Ambari Alert] This is a test message, do not worry.")
    print(response)


def test_link():
    response = client.send_link(token, '[Ambari Alert]', 'I am the text',
                                'https://ding-doc.dingtalk.com/doc#/serverapi2/qf2nxq')
    print(response)


def test_markdown():
    text = "### I am the header\n" + \
           "#### This is a test message, do not worry.\n" + \
           "![girl](https://c-ssl.duitang.com/uploads/item/201605/08/20160508134621_KjzNa.thumb.700_0.gif)\n" + \
           "1. 图片链接1\n" + \
           "2. 图片链接2\n"
    response = client.send_markdown(token, '[Ambari Alert]', text)
    print(response)


def test_single_actioncard():
    text = "### I am the header\n" + \
           "#### This is a test message, do not worry.\n" + \
           "![girl](https://c-ssl.duitang.com/uploads/item/201605/08/20160508134621_KjzNa.thumb.700_0.gif)\n" + \
           "1. 图片链接1\n" + \
           "2. 图片链接2\n"
    response = client.send_single_actioncard(token, '[Ambari Alert]', text, '点击阅读全文',
                                             'https://ding-doc.dingtalk.com/doc#/serverapi2/qf2nxq')
    print(response)


def test_multi_actioncard():
    text = "### I am the header\n" + \
           "#### This is a test message, do not worry.\n" + \
           "![girl](https://c-ssl.duitang.com/uploads/item/201605/08/20160508134621_KjzNa.thumb.700_0.gif)\n"
    btns = [
        ActionCardButton('好看', 'https://ding-doc.dingtalk.com/doc#/serverapi2/qf2nxq'),
        ActionCardButton('点赞', 'https://ding-doc.dingtalk.com/doc#/serverapi2/qf2nxq'),
        ActionCardButton('打赏', 'https://ding-doc.dingtalk.com/doc#/serverapi2/qf2nxq')
    ]
    response = client.send_multi_actioncard(token, '[Ambari Alert]', text, btns)
    print(response)


def test_feedcard():
    links = [
        FeedCardLink('[Ambari Alert]好看', 'https://ding-doc.dingtalk.com/doc#/serverapi2/qf2nxq',
                     'https://c-ssl.duitang.com/uploads/item/201605/08/20160508134621_KjzNa.thumb.700_0.gif'),
        FeedCardLink('点赞', 'https://ding-doc.dingtalk.com/doc#/serverapi2/qf2nxq',
                     'https://c-ssl.duitang.com/uploads/item/201605/08/20160508134621_KjzNa.thumb.700_0.gif'),
        FeedCardLink('打赏', 'https://ding-doc.dingtalk.com/doc#/serverapi2/qf2nxq',
                     'https://c-ssl.duitang.com/uploads/item/201605/08/20160508134621_KjzNa.thumb.700_0.gif')
    ]
    response = client.send_feedcard(token, links)
    print(response)


if __name__ == '__main__':
    # test_text()
    # test_link()
    # test_markdown()
    # test_single_actioncard()
    # test_multi_actioncard()
    test_feedcard()
