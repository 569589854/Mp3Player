# -*- coding: utf-8 -*-
# @Author: 56958
# @Date:   2018-07-23 13:26:18
# @Last Modified by:   56958
# @Last Modified time: 2018-08-02 14:02:44
# -*- coding:utf-8 -*-
from Tkinter import *
import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pyvirtualdisplay import Display
import tkMessageBox
import urllib
import json
import sys
import random
sys.path.append('F:\Python27\Lib')
import mp3play
import time
import threading

global play_or_not

# chrome_options = Options()
# chrome_options.add_argument('--headless')
# driver = webdriver.Chrome()

#不打开浏览器测试
option = webdriver.ChromeOptions()
option.add_argument("headless")
driver = webdriver.Chrome(chrome_options=option)



def getSongId(url):
    song_list = []
    driver.get(url)
    driver.switch_to.frame(0)
    soup = BeautifulSoup(driver.page_source,'html.parser')
    songs = soup.select('body > div.g-bd > div > div:nth-of-type(2) > div.ztag > div > div > div > div.td.w0 > div > div > a:nth-of-type(1)')
    artists = soup.select('body > div.g-bd > div > div:nth-of-type(2) > div.ztag > div > div > div > div.td.w1 > div > a:nth-of-type(1)')
    titles = soup.select('body > div.g-bd > div > div:nth-of-type(2) > div.ztag > div > div > div > div.td.w0 > div > div > a:nth-of-type(1) > b')
  
    for song,artist,title in zip(songs,artists,titles):
        # for n in range(10):
        song_id_ = song.get('href').split('=')[1]
        artist_ = artist.get_text()
        title_ = title.get('title')
        data = {
            'id':song_id_,
            'title':title_,
            'artist':artist_
        }
        # print data
        song_list.append(data)

        # 取前10首歌作为显示
        if(len(song_list)>=10): break
    # print song_list
    return song_list


def music():
    if entry.get() == "":
        tkMessageBox.showinfo('错误','请输入歌曲名或歌手名再搜索！')
        return
    listbox.delete(0, listbox.size())
    name = entry.get().encode('utf-8')#获取文本框的内容赋值给name这个变量
    url = "https://music.163.com/#/search/m/?s={}&type=1".format(name)
    print name
    songs = getSongId(url)
    global link
    global mlist
    mlist = []
    for i in range(len(songs)):
        listbox.insert(i, songs[i]['title'] + "(" + songs[i]['artist'] + ")")
        link = 'http://music.163.com/song/media/outer/url?id={}.mp3'.format(songs[i]['id'])

        mlist.append(link)
        print link #歌曲地址

global last_id
last_id = []

def pl(e):
    play_or_not = True
    #print listbox.get(listbox.curselection(),last=None)  # 打印列表框现行选中项的文本
    sy = listbox.curselection()[0]
    song_name = random.randint(0,999)
    while(song_name in last_id):
        song_name = random.randint(0,999)
    last_id.append(song_name)

    var1.set(u"正在加载  " + listbox.get(listbox.curselection(), last=None))
    urllib.urlretrieve(mlist[int(sy)], "%d.mp3"%int(song_name))
    var1.set(u"正在播放  " + listbox.get(listbox.curselection(), last=None))
    filename = r"%d.mp3" % int(song_name)
    global mp3
    mp3 = mp3play.load(filename)
    # mp2 = mp3play.load(r"103.mp3")
    mp3.play()
    # mp2.play()
        # time.sleep(mp3.seconds()+5)
 
        
    # print min(1, mp3.seconds(time.sleep(10)))

# def play(event):
#     a = threading.Thread(target=pl)
#     a.start()
#     # time.sleep(2)
#     b = threading.Thread(target=pl)
#     b.start()

def stop():
    mp3.stop()
    play_or_not = False
    var1.set(u"歌曲 " + listbox.get(listbox.curselection(), last=None) + u" 已停止播放  ")

def pause():
    mp3.pause()
    var1.set(u"歌曲 " + listbox.get(listbox.curselection(), last=None) + u" 已暂停播放  ")

def con_tinue():
    mp3.unpause()
    var1.set(u"正在播放  " + listbox.get(listbox.curselection(), last=None))

root1 = Tk()
root1.title("Young's MusicPlayer")
root1.geometry('+800+200')#固定窗口位置
entry = Entry(root1)
entry.grid(row=0,column=0,columnspan=5)
button = Button(root1,text = '搜索',command = music)
button2 = Button(root1,text = '暂停',command = pause)
button3 = Button(root1,text = '继续', command = con_tinue)
button.grid(row=0,column=4,sticky=W)
button2.grid(row=1,column=2)
button3.grid(row=1,column=3,sticky=W,pady=3)
var2 = StringVar()
listbox = Listbox(root1,width = 50,listvariable = var2)
listbox.bind('<Double-Button-1>',pl)
listbox.grid(row=3,columnspan=5,rowspan=5)
var1 = StringVar()
label = Label(root1,textvariable = var1,fg = 'Red')
var1.set('欢迎使用!')
label.grid(row=12,column=0,columnspan=5)
root1.mainloop()

