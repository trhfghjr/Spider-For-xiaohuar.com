#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib import request
from bs4 import BeautifulSoup
import re
import time
from gevent import monkey
import gevent
monkey.patch_all()





#获取图片
def parser(html):
    try:
        # listURL="http://www.xiaohuar.com/list-1-1.html"
        soup = BeautifulSoup(html, 'html.parser', from_encoding='gbk')
        # 根据src找到对应的图片
        images = soup.find_all('img', src=re.compile(r'/d/file/\d+/\w+\.jpg'))
        return images
    except:
        print("ERROR Parser")
        return None
#保存图片
def save_img(path,data):
    try:
        with open(path,'wb') as f:
            f.write(data)
    except:
        print("ERROR Save")
        return None

#打开网址
def download(url):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    try:
        req = request.Request(url=url, headers=header)
        response = request.urlopen(req,timeout=10)
        return response.read()
    except :
        print("ERROR Download")

def spider():
    # 大学校花页面
    UnURL = "http://www.xiaohuar.com/list-1-%s.html"
    glist = []
    images=[]
    for i in range(2):#爬取两页图片
        html=download(UnURL % i)
        try:
            if html:
                temp=parser(html)
            if temp!=[]:
                images+=temp
            Start_time=time.time()
            if images!=[]:
                for image in images:
                    data=download("http://www.xiaohuar.com%s"%image['src'])
                    g=gevent.spawn(save_img,'%s.jpg'%image['alt'],data)
                    glist.append(g)
                    # save_img('%s.jpg'%image['alt'],data)
                gevent.joinall(glist)
                End_time = time.time()
                print("下载时间:%s" % (End_time-Start_time))
            else:
                print("images is none")
        except:
            print("ERROR Save in Disk")



if __name__ == '__main__':
    spider()


