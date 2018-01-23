#-*- coding:utf-8 -*-
import re
import requests
from StringIO import StringIO
import cv2
import numpy as np
import os
from requests.exceptions import *
def getPage(url, keyword, page_index, images_per_page): #设定一些发送请求的参数，不同网站不一样
    # for i in range(30,30*pages+30,30):
    keyword = keyword.replace('_', ' ')
    params = {
                  'tn': 'resultjson_com',
                  'ipn': 'rj',
                  'ct': 201326592,
                  'is': '',
                  'fp': 'result',
                  'queryWord': keyword,
                  'cl': 2,
                  'lm': -1,
                  'ie': 'utf-8',
                  'oe': 'utf-8',
                  'adpicid': '',
                  'st': -1,
                  'z': '',
                  'ic': 0,
                  'word': keyword,
                  's': '',
                  'se': '',
                  'tab': '',
                  'width': '',
                  'height': '',
                  'face': 0,
                  'istype': 2,
                  'qc': '',
                  'nc': 1,
                  'fr': '',
                  'pn': page_index,
                  'rn': images_per_page,
                  'gsm': '1e',
                  '1488942260214': ''
              }
    result = requests.get(url, params=params)
        # print requests.get(url, params=i).json().get('data')
    return result

def downloadPic(url,keyword, pages, images_per_page, path):
    if(not os.path.exists(path+keyword)):
        os.system('mkdir ' + path + keyword)
    f = open(path+keyword+'/urls.txt', 'w') #存放下载的所有图片的源地址
    i = 0 #图片序号
    print '找到关键词:'+keyword+'的图片，现在开始下载图片...'
    for page_index in range(images_per_page, images_per_page*pages+images_per_page, images_per_page):
        try:
            result = getPage(url, keyword, page_index, images_per_page)
        except (ConnectionError, ChunkedEncodingError, BaseHTTPError,
                ContentDecodingError, HTTPError, Timeout, SSLError,
                MissingSchema, TooManyRedirects, RequestException,
                InvalidSchema, InvalidURL, URLRequired, ProxyError):
            print keyword+"获取本页内容失败，请重新获取"
            break
        pic_url = re.findall('"thumbURL":"(.*?)",',result.text,re.S) #字符串匹配，百度在网页源码上放了多个不同尺寸的图片地址，thumbURL是百度统一压缩过的，储存在百度自己的服务器上，爬的比较快。
        print '本页共有' + str(len(pic_url)) + '张图片'
        if len(pic_url) == 0:
            print "本页下载完成"
            break
        for each in pic_url:
            f.write(each+'\n')
            print '正在下载第'+str(i+1)+'张图片，图片地址:'+str(each)
            try:
                pic= requests.get(each, timeout=100)
            except (ConnectionError, ChunkedEncodingError, BaseHTTPError,
                ContentDecodingError, HTTPError, Timeout, SSLError,
                MissingSchema, TooManyRedirects, RequestException,
                    InvalidSchema, InvalidURL, URLRequired, ProxyError):
                print '【错误】当前图片无法下载'
                continue
            #resolve the problem of encode, make sure that chinese name could be store
            #fp = open(string.decode('utf-8').encode('cp936'),'wb')
            #fp.write(pic.content)
            #fp.close()
            image = cv2.imdecode(np.fromstring(pic.content, np.uint8), -1)
            if(image is None):
              continue
            h = (image.shape)[0]
            w = (image.shape)[1]
            max_length = w if w > h else h
            if max_length >= 300: #图片长边必须大于300
                cv2.imwrite(path+keyword+'/'+keyword+'_'+str(i)+'.jpg', image)
                i+=1
    f.close()



if __name__ == '__main__':
    url = 'https://image.baidu.com/search/acjson' #对应网站的图片搜索url
    keyword_list = ['zipai'] #此处加入搜索的关键词
    pages = 1000 #一般图片网站以页为单位，一页几十张图片，选择你要下载多少页图片
    images_per_page = 30 #根据网站，设定每页多少张图
    path = '/Users/dingchenwei/Downloads/Pickup-master/pictures/baidu/' #图片储存路径

    if(not os.path.exists(path)):
        os.system('mkdir ' + path)
        
    for keyword in keyword_list:
    	downloadPic(url, keyword, pages, images_per_page, path)

 