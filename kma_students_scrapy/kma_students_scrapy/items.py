# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field
from scrapy import Item

class Student(Item):
    full_name = Field()
    year_and_specialty = Field()
    plan_link = Field()
    credits = Field()
