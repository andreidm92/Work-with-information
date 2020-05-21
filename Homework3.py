from bs4 import BeautifulSoup as bs
import requests
from pymongo import MongoClient
from pprint import pprint

# 1) Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и
# реализовать функцию, записывающую собранные вакансии в созданную БД

i = 0
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.104',
    'Accept': '*/*'}
main_link = 'https://hh.ru'

while True:
    params = {'clusters': 'true',
              "area": 1,
              'enable_snippets': 'true',
              'salary': '',
              'st': 'searchVacancy',
              'text': 'python',
              'page': i}
    html = requests.get(main_link + '/search/vacancy', headers=header, params=params).text
    soup = bs(html, 'lxml')
    vacancy_block = soup.find('div', {'class': 'vacancy-serp'})
    vacancy_list = vacancy_block.findAll('div', {
        'data-qa': ['vacancy-serp__vacancy vacancy-serp__vacancy_premium', 'vacancy-serp__vacancy']})
    vacancies = []
    for vacancy in vacancy_list:
        vacancy_data = {}
        vacancy_link = \
        vacancy.find('a', {'class': 'bloko-link HH-LinkModifier', 'data-qa': 'vacancy-serp__vacancy-title'})['href']
        vacancy_name = vacancy.find('a', {'class': 'bloko-link HH-LinkModifier',
                                          'data-qa': 'vacancy-serp__vacancy-title'}).getText()
        vacancy_site = main_link
        d = vacancy.find('div', {'class': 'vacancy-serp-item__sidebar'}).findChildren(recursive=False)
        if len(d) > 0:
            vacancy_salary1 = vacancy.find('span', {'class': 'bloko-section-header-3 bloko-section-header-3_lite',
                                                    'data-qa': 'vacancy-serp__vacancy-compensation'}).getText()
            vacancy_salary = vacancy_salary1.replace("\xa0", "")
            vacancy_salary = vacancy_salary.split()
            if vacancy_salary[0] == 'до':
                vacancy_data['salary_max'] = int(vacancy_salary[1])
                vacancy_data['salary_min'] = None
                vacancy_data['currency'] = vacancy_salary[2]
            elif vacancy_salary[0] == 'от':
                vacancy_data['salary_max'] = None
                vacancy_data['salary_min'] = int(vacancy_salary[1])
                vacancy_data['currency'] = vacancy_salary[2]
            else:
                vacancy_salary2 = vacancy_salary[0].split('-')
                vacancy_data['salary_max'] = int(vacancy_salary2[1])
                vacancy_data['salary_min'] = int(vacancy_salary2[0])
                vacancy_data['currency'] = vacancy_salary[1]

        else:
            vacancy_data['salary_max'] = None
            vacancy_data['salary_min'] = None
            vacancy_data['currency'] = None

        vacancy_data['name'] = vacancy_name
        vacancy_data['link'] = vacancy_link
        vacancy_data['site'] = vacancy_site
        vacancies.append(vacancy_data)
    cont = soup.find('a', {'class': 'bloko-button HH-Pager-Controls-Next HH-Pager-Control'})
    if cont is None:
        break
    # cont_elem = cont.getText()
    i += 1

#pprint(vacancies)


client = MongoClient('localhost', 27017)
db = client['InfoReq']
hh = db.hh
sj = db.sj

hh.insert_many(vacancies)
for hh in hh.find({}):
    pprint(hh)

# 2) Написать функцию, которая производит поиск и выводит на экран вакансии с
# заработной платой больше введенной суммы

for search in hh.find( { "$or": [ {'salary_min': { "$gte": 150000 }}, {'salary_max': { "$gte": 150000 }} ] }, {'name':1,'link':1, 'salary_min':1, 'salary_max':1,'_id':0} ):
    pprint(search)








