# encoding:utf-8

import requests
import urllib
from bs4 import BeautifulSoup
import os
import threading

BASE_PAGE_URL = 'https://www.doutula.com/photo/list/?page='
# 页面url列表
PAGE_URL_LIST = []
# 所有表情url列表
FACE_URL_LIST = []
# 全局锁
gLock = threading.Lock()
for x in range(1, 996):
    url = BASE_PAGE_URL + str(x)
    PAGE_URL_LIST.append(url)


# 下载图片
# 指定图片下载路径
# 给图片分配一个名字
# def download_image(url):
#     split_list = url.split('/')
#     filename = split_list.pop()
#     path = os.path.join('images', filename)  # 保证路径在不同系统下都行的通
#     urllib.urlretrieve(url, filename=path)


# def get_page(page_url):
#     response = requests.get(page_url)
#     content = response.content
#     soup = BeautifulSoup(content, 'lxml')
#     img_list = soup.find_all('img', attrs={'class': 'img-responsive lazy image_dta'})
#     for img in img_list:
#         url = img['data-original']
#         download_image(url)


def producer():
    while True:
        gLock.acquire()
        if len(PAGE_URL_LIST) == 0:
            gLock.release()
            break
        else:
            page_url = PAGE_URL_LIST.pop()
            gLock.release()
            response = requests.get(page_url)
            content = response.content
            soup = BeautifulSoup(content, 'lxml')
            img_list = soup.find_all('img', attrs={'class': 'img-responsive lazy image_dta'})
            gLock.acquire()
            for img in img_list:
                img_url = img['data-original']
                FACE_URL_LIST.append(img_url)
            gLock.release()


def customer():
    while True:
        gLock.acquire()
        if len(FACE_URL_LIST) == 0:
            gLock.release()
            continue
        else:
            face_url = FACE_URL_LIST.pop()
            gLock.release()
            split_list = face_url.split('/')
            filename = split_list.pop()
            path = os.path.join('images', filename)  # 保证路径在不同系统下都行的通
            urllib.urlretrieve(face_url, filename=path)


def main():
    # for page_url in PAGE_URL_LIST:
    #     get_page(page_url)

    # 创建3个多线程作为生产者，爬取表情的url
    for x in range(3):
        th = threading.Thread(target=producer)
        th.start()

    # 创建5个线程作为消费者，把表情图片下载下来
    for x in range(5):
        th = threading.Thread(target=customer)
        th.start()


if __name__ == "__main__":
    main()
