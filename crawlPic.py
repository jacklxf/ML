from bs4 import BeautifulSoup
import requests
import os
import re
import numpy as np
import pandas as pd
os.makedirs('./picDownload/',exist_ok=True)
"""
#Download pics in one page
url='http://desk.zol.com.cn/dongman/'
html=requests.get(url).text
soup=BeautifulSoup(html,'lxml')
img_url=soup.find_all('ul',{'class':'pic-list2'})
for ul in img_url:
    imgs=ul.find_all('img')
    for link in imgs:
        img=link['src']
        print(img)
        r=requests.get(img)
        image_name=img.split('/')[-1]
        with open(image_name,'wb') as f:
            f.write(r.content)
"""

#DOWNLOAD WALLPAPER

for n in np.arange(0,9):
    url='http://desk.zol.com.cn/bizhi/5354_6618'+str(n)+'_2.html'
    html=requests.get(url).text
    soup=BeautifulSoup(html,'lxml')
    #print(soup)
        
    img_url=soup.find_all('div',{'id':'mouscroll'})
    for link in img_url:
        img=link.find_all('img')
        source=img[0]['src']
        r=requests.get(source)
        img_name=source.split('/')[-1]
        with open('./picDownload/%s' %img_name,'wb') as f:
            f.write(r.content)

url='https://www.jkforum.net/thread-8614405-1-1.html'
html=requests.get(url).text
soup=BeautifulSoup(html,'lxml')
img_url=soup.find_all('div',{'class':'t_fsz'})
for n in img_url:
    print(n.find_all('src'))


 
 
 
 
 
 
 
 
 
 
 
 
 





