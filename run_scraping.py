import codecs
import os
import sys

from django.db import DatabaseError

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"

import django

django.setup()

from scraping.parsers import *
from scraping.models import Vacancy, City, Language

parsers = (
    (hh,
     'https://rostov.hh.ru/search/vacancy?text=python&salary=&clusters=true&area=76&ored_clusters=true&enable_snippets=true'),
    (fl, 'https://www.fl.ru/search/?type=projects&search_string=python&action=search')
)

city = City.objects.filter(slug='rostov-na-donu').first()
language = Language.objects.filter(slug='python').first()

jobs, errors = [], []
for func, url in parsers:
    j, e = func(url)
    jobs += j
    errors += e

for job in jobs:
    v = Vacancy(**job, city=city, language=language)
    try:
        v.save()
    except DatabaseError:
        pass

h = codecs.open('work.txt', 'w', 'utf-8')
h.write(str(jobs))
h.close()
