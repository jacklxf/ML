from bs4 import BeautifulSoup
import requests
import re

book_links = []
book_libraries = []
for n in range(2, 100):
    url = 'http://www.allitebooks.com/page/%s/' % n
    print(url)
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
    # print(soup)
    links = soup.find_all('div', {'class': 'entry-body'})

    for i in links:
        book_urls = i.find('a')['href']
        book_names = i.find('a', {'rel': 'bookmark'}).text.strip()
        book_links.append(book_urls)
        book_libraries.append(book_names)

print(book_libraries)
print(len(book_libraries))

for m in book_links:
    html = requests.get('%s' % m).text
    soup = BeautifulSoup(html, 'lxml')
    links = soup.find('span', {'class': 'download-links'})
    a = links.find('a')['href']
    name = m.split('/')[-2]
    with open('./books_download/%s' % name, 'wb') as f:
        f.write(requests.get(a).content)

print('done')