import scrapy
import re
from ..items import Student

class MySpider(scrapy.Spider):
    name = 'kma-students'

    def start_requests(self):
        return [scrapy.FormRequest(
            'http://my.ukma.edu.ua/checklogin.php',
            formdata={'cmd': '', 'login': '', 'password': ''},
            callback=self.logged_in)]

    def logged_in(self, response):
        self.logger.info('logged_in method response.url: %s', response.url)
        logged_in = response.url == 'http://my.ukma.edu.ua/index.php'
        if logged_in:
            self.logger.info('logged_in method auth: ok')
            return scrapy.Request('http://my.ukma.edu.ua/?menuitem=students',
                                  callback=self.parse)
        else:
            self.logger.info('logged_in method auth: not ok')
            return []

    def parse(self, response):
        self.logger.info('parse method: processing a singe page...')
        div = response.xpath('//div[contains(@class, "col-xs-9")]')
        data = div.extract_first()
        #processing of the page could have been elegant
        #if the author of the web site had written better html page
        #replacing special characters is done to ease subsequent regex matching
        data = data.replace('\r\n', '') \
                   .replace('\t', '')
        #web resourse was modified recently, the line below in unwanted
        #data = data[ data.index('</form>') : ]
        if 'page' in response.url:
            response.meta['my-data'] = data
            for student in self.parse_students(response):
                yield student
        pages_selector = div.xpath('.//a[contains(@class, "pages")]')
        links_to_pages = pages_selector.xpath('./@href').extract()
        if not links_to_pages:
            self.logger.info('parse method: the last page has been reached!')
        else:
            self.logger.info('parse method: current page %s', response.url)
            for link in links_to_pages:
                yield scrapy.Request(response.urljoin(link), callback=self.parse)

    def parse_students(self, response):
        data = response.meta['my-data']
        pattern = r'<strong>((.*?)</strong>(.*?)<a href=\"(.*?)\">(.*?)</a>(.*?))<br>'
        #omitting first item is done due to peculiar way the web site is written
        #if this is not done, the first found item would be invalid
        omit_current = True
        for match in re.finditer(pattern, data):
            if omit_current:
                omit_current = False
                continue
            name, year_and_specialty, plan_link, credits = match.group(2, 3, 4, 6)
            yield Student(
                full_name          = name.replace('.', '').strip(),
                year_and_specialty = year_and_specialty.strip(),
                plan_link          = response.urljoin(plan_link.replace('&amp;', '&')),
                credits            = credits.strip())
