from bs4 import BeautifulSoup
import requests


def crawlWeb(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
    return soup


def crawlImg(soup):
    links = soup.find_all('a', {'class': 'js-photo-link'})
    img_urls = []
    for i in links:
        img_urls.append(i.find('img')['src'])
    return img_urls


def download(img_urls):
    for n in img_urls:
        name = n.split('/')[-2]
        with open('./pics/%s' %name, 'wb') as f:
            f.write(requests.get(n).content)


if __name__ == '__main__':
    url = ''
    download(crawlImg(crawlWeb(url)))
    print('Done')