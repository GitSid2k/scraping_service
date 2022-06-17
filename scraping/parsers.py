from random import randint

import requests
import codecs
from bs4 import BeautifulSoup

__all__ = ('hh', 'fl')

headers = [
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:53.0) Gecko/20100101 Firefox/53.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
]


def hh(url, city=None, language=None):
    jobs = []
    errors = []
    domain = 'https://rostov.hh.ru'
    if url:
        resp = requests.get(url, headers=headers[randint(0, 2)])
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, 'html.parser')
            main_div = soup.find('div', id='a11y-main-content')
            if main_div:
                div_lst = main_div.find_all('div', attrs={"class": 'vacancy-serp-item'})
                for div in div_lst:
                    title = div.find('h3')
                    href = title.a['href']
                    content = div.find('div', attrs={"class": 'g-user-content'})
                    company = div.find('div', attrs={"class": 'vacancy-serp-item__meta-info-company'})
                    jobs.append(
                        {'title': title.text, 'url': domain + href, 'company': company.text, 'description': content.text})
            else:
                errors.append({'url': url, 'title': "Div does not exists"})
        else:
            errors.append({'url': url, 'title': "Page do not response"})

    return jobs, errors


def fl(url, city=None, language=None):
    jobs = []
    errors = []
    domain = 'https://www.fl.ru'
    if url:
        resp = requests.get(url, headers=headers[randint(0, 2)])
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, 'html.parser')
            main_div = soup.find('div', id='search-lenta')
            if main_div:
                div_lst = main_div.find_all('div', attrs={"class": 'search-item-body'})
                for div in div_lst:
                    title = div.find('h3')
                    href = title.a['href']
                    content = div.p
                    jobs.append({'title': title.text, 'url': domain + href, 'description': content.text})
            else:
                errors.append({'url': url, 'title': "Div does not exists"})
        else:
            errors.append({'url': url, 'title': "Page do not response"})

    return jobs, errors
