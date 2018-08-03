# -*- coding: utf-8 -*-
# @Author: 56958
# @Date:   2018-07-19 09:32:26
# @Last Modified by:   56958
# @Last Modified time: 2018-07-19 13:57:24
import requests
import time
from bs4 import BeautifulSoup

def get_true_gender(class_name):
    if class_name.find("boy"):
            gender_ = "男"
    else:
        gender_ = "女"
    return gender_

def get_links(url):
    wb_data = requests.get(url)
    Soup = BeautifulSoup(wb_data.text,'lxml')
    # print Soup
    links = Soup.select('#page_list > ul > li > a')
    print links
    for link in links:
        href = link.get('href')
        get_detail_info(href)
        time.sleep(2)


def get_detail_info(url):
    wb_data = requests.get(url)
    Soup = BeautifulSoup(wb_data.text,'lxml')

    titles = Soup.select('body > div.wrap.clearfix.con_bg > div.con_l > div.pho_info > h4 > em')
    addresses = Soup.select('body > div.wrap.clearfix.con_bg > div.con_l > div.pho_info > p > span')
    prices = Soup.select('#pricePart > div.day_l > span')
    house_imgs = Soup.select('#curBigImage')
    host_imgs = Soup.select('#floatRightBox > div.js_box.clearfix > div.member_pic > a > img')
    genders = Soup.select('#floatRightBox > div.js_box.clearfix > div.w_240 > h6 > span')
    names = Soup.select('#floatRightBox > div.js_box.clearfix > div.w_240 > h6 > a')
    # print titles
    house_info = []
    for title,address,price,house_img,host_img,gender,name in zip(titles,addresses,prices,house_imgs,host_imgs,genders,names):
        

        data = {
            'title':title.get_text(),
            'address':address.get_text(),
            'price':price.get_text(),
            'house_img':house_img.get('src'),
            'host_img':host_img.get('src'),
            'gender':get_true_gender(gender.get('class')),
            'name':name.get_text(),
        }
        house_info.append(data)
        print data



url = ['http://bj.xiaozhu.com/search-duanzufang-p{}-0/'.format(number) for number in range(1,10)]
for single_url in url:
    get_links(single_url)
