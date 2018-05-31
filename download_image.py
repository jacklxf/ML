from bs4 import BeautifulSoup
import requests

url='https://wall.alphacoders.com/search.php?search=landscape'
html=requests.get(url).text
soup=BeautifulSoup(html,'lxml')
links=soup.find_all('img')
img_urls=[]
for i in links:
    img_urls.append(i['src'])








'''
html = requests.get(url).text
soup = BeautifulSoup(html, 'lxml')

links = soup.find_all('img', {'class': 'img-responsive'})

img_urls = []
for i in links:
    img_urls.append(i['src'])

for n in img_urls:
    name = n.split('/')[-2]
    with open('C:/Users/xiaofeng.li/Documents/ML/pics/%s.jpg' %name, 'wb') as f:
        f.write(requests.get(n).content)

print('Done')
'''