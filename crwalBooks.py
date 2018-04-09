import requests
from bs4 import BeautifulSoup
import os
import numpy as np
import pandas as pd


url='https://www.crummy.com/software/BeautifulSoup/bs4/doc/'
html=requests.get(url).text
soup=BeautifulSoup(html,'lxml')

img_url=soup.find_all('div',{'class':'body'})
print(img_url)
for img in img_url:
	p=img.find_all('p')
	print(p)


