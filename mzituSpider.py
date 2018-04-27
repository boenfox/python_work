#!/usr/bin/env python3
# -*- coding:UTF-8 -*-

import os
import requests
from bs4 import BeautifulSoup

HOSTREFERER = {
    'User-Agent': 'Mozilla/5.0(compatible; MSIE6.0; Windows NT 5.1)',
    'Referer': 'http://www.mzitu.com/'
}

PICREFERER = {
    'User-Agent': 'Moxilla/5.0(compatible; MSIE 5.0; Windows NT 5.1',
    'Referer': 'http://i.meizitu.net/'
}


def get_page_name(url):
    '''/home/zj/python_work/mzituSpider.py
    获取妹子名
    '''
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    span = soup.findAll('span')
    title = soup.find('h2', class_="main-title")
    return span[10].text, title.text

def get_html(url):
    '''
    获取页面html内容
    '''
    req = requests.get(url, headers=HOSTREFERER)
    html = req.text
    return html

def get_img_url(url, name):
    '''
    获取图片的链接
    '''
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    img_url = soup.find('img', alt=name)
    return img_url['src']

def save_img(img_url, count, name):
    '''
    保存图片
    '''
    req = requests.get(img_url, headers=PICREFERER)
    with open(name+'/'+str(count)+'.jpg', 'wb') as f:
        f.write(req.content)

def main():
    '''
    主程序入口
    '''
    old_url = "http://www.mzitu.com/131458"
    page, name = get_page_name(old_url)
    os.mkdir(name)
    for i in range(1, int(page)+1):
        url = old_url+'/' + str(i)
        img_url = get_img_url(url, name)
        save_img(img_url, i, name)
        print('保存第'+str(i)+'张图片成功！')


main()
