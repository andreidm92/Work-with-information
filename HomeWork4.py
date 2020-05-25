from lxml import html
from pprint import pprint
import requests
from pymongo import MongoClient

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}
main_link = 'https://yandex.ru/news/'
response = requests.get(main_link, headers = header)
dom = html.fromstring(response.text)

name1 = dom.xpath("//h2[@class='story__title']//text()")
link1 = dom.xpath("//h2[@class='story__title']/a/@href")
source1 = dom.xpath("//div[@class='story__date']//text()")

yandex_news = []
for i in range(len(name1)):
    data = {}
    data['date'] = source1[i][-5:]
    data['name'] = name1[i]
    data['link'] = link1[i]
    data['source'] = source1[i][:-6]

    yandex_news.append(data)

client = MongoClient('localhost', 27017)
db = client['News']
yn1 = db.yn1
ln = db.ln
yn1.insert_many(yandex_news)
for yn in yn1.find({}):
    pprint(yn)


# lenta.ru

#//div[@class='item']/a/time[@class='g-time']
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}
main_link = 'https://lenta.ru/'
response = requests.get(main_link, headers = header)
dom = html.fromstring(response.text)

blocks = dom.xpath("//div[@class='span4']/div[@class='item']")
lenta_news = []
for block in blocks:
    data = {}
    data['date'] = block.xpath('.//@title')
    data['name'] = block.xpath('.//text()')[1].replace('\xa0','')
    data['link'] = block.xpath('./a/@href')
    data['source'] = 'www.lenta.ru'
    lenta_news.append(data)
#pprint(lenta_news)

client = MongoClient('localhost', 27017)
db = client['News']
ln = db.ln
ln.insert_many(lenta_news)
for ln in ln.find({}):
    pprint(ln)

#Mail.news"

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}
main_link = 'https://news.mail.ru/?from=menu'
response = requests.get(main_link, headers = header)
dom = html.fromstring(response.text)

blocks = dom.xpath("//div[@class='cols__inner']")
mail_news = []
for block in blocks:
    data = {}
    data['date'] = block.xpath('.//span[@class="newsitem__param js-ago"]/@datetime')
    data['name'] = block.xpath('.//a[@class="newsitem__title link-holder"]//text()')[0].replace('\xa0','')
    data['link'] = block.xpath('.//a[contains(@class,"newsitem__title")]/@href')
    data['source'] = block.xpath('.//span[@class="newsitem__param"]//text()')
    mail_news.append(data)

client = MongoClient('localhost', 27017)
db = client['News']
mn = db.mn
mn.insert_many(mail_news)
for mn in mn.find({}):
    pprint(mn)

