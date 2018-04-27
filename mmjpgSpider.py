#!/usr/bin/env python3
# -*- coding:UTF-8 -*-

import os
import time
import requests
from lxml import etree
from selenium import webdriver

# 将Chrome设置不加载图片的无界面的运行状态
CHROME_OPTIONS = webdriver.ChromeOptions()
PREFS = {"profile.managed_default_content_setting.images": 2}
CHROME_OPTIONS.add_experimental_option("prefs", PREFS)
CHROME_OPTIONS.add_argument("--headless")
CHROME_PATH = os.path.join(os.getcwd(), 'chromedriver')
# 设置图的存储路径
PICTURE_PATH = os.path.join(os.getcwd(), 'picture/')

# 设置headers
HEADERS = {
    'User-Agent': "Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.1)\
     Chorme/66.0.3359.139 Safari/537.36", 'Referer': 'http://www.mmjpg.com'
}

class Spider(object):
    '''
    定义爬虫类
    '''
    def __init__(self, page_num):
        self.page_num = page_num
        self.page_urls = ['http://www.mmjpg.com']
        self.girl_urls = []
        self.girl_name = ''
        self.pic_urls = []

    def get_girl_urls(self):
        '''
        获取妹子的url方法
        '''
        for page_url in self.page_urls:
            html = requests.get(page_url).content
            selector = etree.HTML(html)
            self.girl_urls += (selector.xpath('//span[@class="title"]/a/@href'))

    def get_pic_urls(self):
        '''
        获取图片的url的方法
        '''
        driver = webdriver.Chrome(CHROME_PATH, chrome_options=CHROME_OPTIONS)
        for girl_url in self.girl_urls:
            driver.get(girl_url)
            time.sleep(3)
            driver.find_element_by_xpath('//em[@class="ch all"]').click()
            time.sleep(3)
            html = driver.page_source
            selector = etree.HTML(html)
            self.girl_name = selector.xpath('//div[@class="article"]/h2/text()')
            self.pic_urls = selector.xpath('//div[@class="content"]/img/@data-img')
            try:
                self.download_pic()
            except Exception as e:
                print("{}保存失败！".format(self.girl_name) + str(e))
    
    def download_pic(self):
        '''
        下载图片的方法
        '''
        try:
            os.mkdir(PICTURE_PATH)
        except:
            pass
        girl_path = PICTURE_PATH + self.girl_name
        try:
            os.mkdir(girl_path)
        except Exception as e:
            print("{}已存在".format(self.girl_name))
        img_name = 0
        for pic_url in self.pic_urls:
            img_name += 1
            img_data = requests.get(pic_url, headers=HEADERS)
            pic_path = girl_path + '/' + str(img_name) + '.jpg'
            if os.path.isfile(pic_path):
                print("{}第{}张图片已存在".format(self.girl_name, img_name))
            else:
                with open(pic_path, 'wb') as f:
                    f.write(img_data.content)
                    print("正在保存{}第{}张".format(self.girl_name, img_name))
        return

    def get_page_urls(self):
        '''
        获取页面url的方法
        '''
        if int(page_num) > 1:
            for n in range(2, int(page_num)+1):
                page_url = 'http://www.mmjpg.com/home/' + str(n)
                self.page_urls.append(page_url)
        elif int(page_num) == 1:
            pass

    def start(self):
        '''
        爬虫的启动方法，按照爬虫的逻辑依次调用方法
        '''
        self.get_page_urls()
        self.get_girl_urls()
        self.get_pic_urls()

if __name__ == '__main__':
    page_num = input("请输入页码：")
    mmjpg_spider = Spider(page_num)
    mmjpg_spider.start()
