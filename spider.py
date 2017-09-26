# encoding:utf-8

import requests
import urllib
from bs4 import BeautifulSoup
import os

BASE_PAGE_URL = 'https://www.doutula.com/photo/list/?page='
PAGE_URL_LIST = []
for x in range(1, 996):
    url = BASE_PAGE_URL + str(x)
    PAGE_URL_LIST.append(url)


# 下载图片
# 指定图片下载路径
# 给图片分配一个名字
def download_image(url):
    split_list = url.split('/')
    filename = split_list.pop()
    path = os.path.join('images', filename)  # 保证路径在不同系统下都行的通
    urllib.urlretrieve(url, filename=path)


def get_page(page_url):
    response = requests.get(page_url)
    content = response.content
    soup = BeautifulSoup(content, 'lxml')
    img_list = soup.find_all('img', attrs={'class': 'img-responsive lazy image_dta'})
    for img in img_list:
        url = img['data-original']
        download_image(url)


def main():
    for page_url in PAGE_URL_LIST:
        get_page(page_url)


if __name__ == "__main__":
    main()
