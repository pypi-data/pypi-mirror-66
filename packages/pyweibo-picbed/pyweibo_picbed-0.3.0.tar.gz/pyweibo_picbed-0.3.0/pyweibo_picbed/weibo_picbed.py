#! /usr/bin/env python
# -*- coding: utf-8 -*-

import time
import os
import base64
from AppKit import NSPasteboard, NSPasteboardTypePNG, NSPasteboardTypeTIFF, NSPasteboardTypeString
from pycookiecheat import chrome_cookies
import os
import sys
import sqlite3
import requests
import random
import re


def get_img_file_from_mac_clipboard():
    """
    在MacOS系统中，读取剪切板图片并保存为文件，返回文件路径
    若剪切板无图片，返回None
    """
    pb = NSPasteboard.generalPasteboard()
    data_type = pb.types()
    
    time_stamp = int(time.time() * 1000)
    
    if NSPasteboardTypePNG in data_type:
        # png 格式
        data = pb.dataForType_(NSPasteboardTypePNG)
        filepath = "/tmp/%s.png" % time_stamp
        ret = data.writeToFile_atomically_(filepath, False)
        if ret:
            return filepath
    elif NSPasteboardTypeTIFF in data_type:
        # tiff 格式
        data = pb.dataForType_(NSPasteboardTypeTIFF)
        filepath = "/tmp/%s.tiff" % time_stamp
        ret = data.writeToFile_atomically_(filepath, False)
        if ret:
            return filepath
    elif NSPasteboardTypeString in data_type:
        # string todo, recognise url of png
        pass
    return None


def get_img_base64_from_clipboard():
    """
    读取剪切板图片并返回图片的Base64编码
    """
    # 判断系统类型
    if sys.platform == 'darwin':
        get_img_file_from_clipboard = get_img_file_from_mac_clipboard
    elif sys.platform == 'win32':
        # TODO
        raise Error('not implemented!')
    elif sys.platform == 'linux':
        raise Error('not supported!')
    
    img_filepath = get_img_file_from_clipboard()
    if img_filepath is None:
        return None
    
    with open(img_filepath, 'rb') as f:
        img_base64 = base64.b64encode(f.read())
    # 删除该文件
    os.remove(img_filepath)
    return img_base64


def is_weibo_login(cookies=None):
    """
    根据传入的cookies判断微博是否登陆，从而判断cookies是否有效
    """
    check_url='https://account.weibo.com/set/index?topnav=1&wvr=6'
    login_resp = requests.get(check_url, cookies=cookies)
    return login_resp.url == check_url


def upload_screenshot_to_weibo():
    """
    上传剪切板中的截图到微博图床中
    """
    # 从 Chrome 读取微博的 Cookies
    weibo_cookies = chrome_cookies('https://weibo.com')
    # 判断 Cookies 是否有效
    if not is_weibo_login(weibo_cookies):
        return False, 'not logged in!'
    
    image_url = 'https://picupload.weibo.com/interface/pic_upload.php?ori=1&mime=image%2Fjpeg&data=base64&url=0&markpos=1&logo=&nick=0&marks=1&app=miniblog'

    img_base64 = get_img_base64_from_clipboard()
    if img_base64 is None:
        return False, 'no imgs in clipboard!'
    
    # 开始上传
    data = {
        "b64_data": img_base64, 
    }

    try:
        response = requests.post(image_url, data=data, cookies=weibo_cookies)
        image_id = re.findall('"pid":"(.*)"', response.text)[0]
        zones = ['wx{}'.format(i) for i in range(1, 5)] + \
                ['ww{}'.format(i) for i in range(1, 5)]
        
        img_url = 'http://{}.sinaimg.cn/large/{}.jpg'.format(random.choice(zones), image_id)
        return True, img_url
    except Exception:
        return False, 'upload failed!'


def get_html_type_img_url(img_url):
    return r'<img src="{}"/>'.format(img_url)


def get_markdown_type_img_url(img_url, img_name='img'):
    return r'![{}]({})'.format(img_name, img_url)


if __name__=='__main__':
    state, msg = upload_screenshot_to_weibo()
    if state:
        print(msg)
    else:
        print("error: %s" % msg)
