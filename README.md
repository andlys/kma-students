# web crawler...
...for http://my.ukma.edu.ua/

## 2934 KMA students in a single JSON-Lines file:
`kma-students-2017-10-22T19-41-26.jsonl`

## run
install dependencies (the [Scrapy](https://github.com/scrapy/scrapy) Framework)
`pip install scrapy`
(with configured delay of 10 sec per request takes 30 mins)
`scrapy crawl kma-students`

## TODO:
Classify each student according to his/her:
* sex
* faculty
