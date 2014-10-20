import scrapy, re
from khan_classes.items import KhanClassesItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

class KlassSpider(CrawlSpider):
  name = "klass"
  allowed_domains = ["www.khanacademy.org"]
  start_urls = ["https://www.khanacademy.org/library"]
  rules = (Rule(LinkExtractor(allow=(r'/math/'),
    restrict_xpaths=('//a[@class="topic-list-item"]')
    ), callback="parse_next_page", follow=True),)


  def parse_start_url(self, response):
    self.log("\n\n Starting to crawl ... \n\n")
    items = response.css('li.subjects-row-first div').xpath('./table/tr/td/a').extract()
    for item_data in items:
      item = self.process_data(item_data)
      yield scrapy.Request(item['link'], callback=self.create, meta={'item': item})

  def process_data(self, data):
    href = re.search( r'/(?:(?!").)*', data).group()
    subject = re.search( r'>(?:(?!<).)*', data).group()
    domain = re.search( r'/(?:(?!/).)*', href).group()

    return {
      'subject': subject[1:],
      'domain': domain[1:18] if domain.startswith('/e') else domain[1:],
      'link': "https://www.khanacademy.org"+href
    }

  def create(self, response):
    item = response.meta['item']
    lessons = response.xpath('//h4[@class="topic-title"]/text()').extract()
    images = self.process_images(response)
    for index, lesson in enumerate(lessons):
      klass = KhanClassesItem()
      klass['subject'] = item['subject']
      klass['domain'] = item['domain']
      klass['lesson'] = lesson
      klass['link'] = item['link']
      klass['image_urls'] = [images[index]]
      yield klass

  def process_images(self, response):
    images = response.xpath('//div[@class="icon-with-progress"]/@data-icon-url').extract()
    if not images:
      thumbs = response.xpath('//div[@class="thumb"]/img/@src').extract()
      return thumbs
    return images










  # -------- RULES ------- #
  # From what I can tell, this is useful if you have items on the first page
  # that are not connected to items on the second page.  In other words,
  # the items on the second page are just a continuation of the list as a
  # whole, and contain item information that can stand independently of item
  # information from the first page.
  #
  # rules = (Rule(LinkExtractor(allow=(r'/math/'),
    # restrict_xpaths=('//a[@class="topic-list-item"]')
    # ), callback="parse_second_page", follow=False),)

  # def parse_second_page(self, resposnse):
  #   print "Link from Part 3:", response.url
  # ---------------------- #
