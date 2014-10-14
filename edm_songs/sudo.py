
href = response.css('h2.et_pt_title').xpath('./a/@href').extract()
text = response.css('h2.domain-header').xpath('./a/text()').extract()

foo = response.xpath('//h2[@class="domain-header"]/a/text()').extract()

  s = text.split('-') #\u2013

  if s[1] contains '('
    s[1].split('(')
  elif s[1] contains '['
    s[1].split('[')
  s.flatten()

  title = s[0]
  artist = s[1]
  notes = s[2]
  link = href

response.xpath('//a[@class="subject-link"]/text()')

a = response.css('p.et_pt_blogmeta').xpath('./a[contains(@rel, "author")]/text()')
d = response.css('p.et_pt_blogmeta').xpath('./text()').re('[A-Z][a-z]{2}[\s].+')

  postAuthor = a
  postDate = d.slice(0,-4).toDateFormat()

div.wp-pagenavi > a.nextpostslink
  n = a.nextpostslink
  '[A-Z][\w]+'

print "------------",result[0],"------------------"
print "By:", result[1]
if result[2]: print "Notes:", result[2]
print "Link:", result[3]
print "Post Author:", result[4]
print "Post Date:", result[5]


class MySpider(CrawlSpider):
  name = 'example.com'
  allowed_domains = ['example.com']
  start_urls = ['http://www.example.com']

  rules = (
    # Extract links matching 'category.php' (but not matching 'subsection.php')
    # and follow links from them (since no callback means
    # follow=True by default).
    Rule(LinkExtractor(allow=('category\.php', ), deny=('subsection\.php', ))),

    # Extract links matching 'item.php' and parse them with the
    # spider's method parse_item
    Rule(LinkExtractor(allow=('item\.php', )), callback='parse_item'),
  )

  def parse_item(self, response):
    self.log('Hi, this is an item page! %s' % response.url)
    item = scrapy.Item()
    item['id'] = response.xpath('//td[@id="item_id"]/text()').re(r'ID: (\d+)')
    item['name'] = response.xpath('//td[@id="item_name"]/text()').extract()
      temp = response.xpath('//td[@id="item_description"]/text()').extract()
    item['description'] = temp
    return item