import codecs

from scraping.parsers import *

parsers = (
    (hh,
     'https://rostov.hh.ru/search/vacancy?text=python&salary=&clusters=true&area=76&ored_clusters=true&enable_snippets=true'),
    (fl, 'https://www.fl.ru/search/?type=projects&search_string=python&action=search')
)

jobs, errors = [], []
for func, url in parsers:
    j, e = func(url)
    jobs += j
    errors += e

h = codecs.open('work.txt', 'w', 'utf-8')
h.write(str(jobs))
h.close()
