import scrapy
from khan_classes.items import KhanClassesItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

class KlassSpider(CrawlSpider):
  name = "klass"
  allowed_domains = ["www.khanacademy.org"]
  start_urls = [
    "https://www.khanacademy.org/library",
  ]
  rules = (Rule(LinkExtractor(allow=(r'/math/'),
    # restrict_xpaths=('//a[@class="subject-link"]')
    ), callback="parse_start_url", follow=False),)

  # def parse_start_url(self, response):
  #   self.log("\n\n Starting to crawl ... \n\n")

  #   klass = KhanClassesItem()
  #   klass['main_url'] = response.url
  #   request = scrapy.Request("https://www.khanacademy.org/library",
  #                            callback=self.parse_klasses)
  #   request.meta['item'] = klass
  #   return request

  def parse_start_url(self, response):
    self.log("\n\n Starting to crawl ... \n\n")
    # subject
    # link
    # domain
    response.css('li.subjects-row-first div').xpath('./table/tr/td/a').extract()
    response.css('li.subjects-row-first div').xpath('./table/tr/td/a/text()').extract()
    response.css('li.subjects-row-first div').xpath('./table/tr/td/a/@href').extract()

    for link in subjectLinks:
      print "Link from Part 1:", link
    klass = KhanClassesItem()
    klass['main_url'] = response.url
    klass['other_url'] = response.url
    request = scrapy.Request("https://www.khanacademy.org/library",
                             callback=self.parse_test)
    request.meta['item'] = klass
    yield request


  def parse_test(self, response):
    klass = response.meta['item']
    klass['other_url'] = response.url
    print "Here is Part 2", klass
    return klass

  def parse_later(self, response):
    domains = response.css('h2.domain-header').xpath('./a/text()').extract()
    subjects = response.css('li.subjects-row-first div').xpath('./table/tr/td/a/text()').extract()
    # subjects = response.xpath('//a[@class="subject-link"]')
    # return self.parse_songs(response)

    print ('\n\n Crawling %s \n\n' % response.url[20:-1])
    href = response.css('h2.et_pt_title').xpath('./a/@href').extract()
    text = response.css('h2.et_pt_title').xpath('./a/text()').extract()
    author = response.css('p.et_pt_blogmeta').xpath('./a[contains(@rel, "author")]/text()').extract()
    date = response.css('p.et_pt_blogmeta').xpath('./text()').re('[A-Z][a-z]{2}[\s].+')
    songs = []

    lesson = response.xpath('//h4[@class="topic-title"]/text()').extract()

    for i, word in enumerate(text):
      encodedText = word.encode('utf-8')
      if '\xe2\x80\x93' not in encodedText:
        href.remove(href[i])
        text.remove(text[i])
        author.remove(author[i])
        date.remove(date[i])
      else:
        # encodedText = add lines to clean content, ex: feat. to ft.
        data = self.process(encodedText)
        result = [data[0], data[1], data[2], href[i], author[i], date[i][:-4]]
        song = self.createSong(result)
        songs.append(song)

    return songs

  def process(self, encodedText):
    data = encodedText.split(' \xe2\x80\x93 ')
    if '(' in data[1]:
      titleNotes = data.pop().split(' (')
      title = titleNotes[0]
      notes = titleNotes[1][:-1]
    elif '[' in data[1]:
      titleNotes = data.pop().split(' [')
      title = titleNotes[0]
      notes = titleNotes[1][:-1]
    else:
      title = data[1]
      notes = None
    return [title, data[0], notes]

  def createSong(self, result):
    song = EdmSongsItem()
    song['title'] = result[0]
    song['artist'] = result[1]
    song['notes'] = result[2]
    song['link'] = result[3]
    song['postAuthor'] = result[4]
    song['postDate'] = result[5]
    return song

  def storeInFile(self, songs, url):
    section = url.split("/")[-2].split('-')
    filename = '_'.join([word for word in section if 'ed' not in word])
    with open(filename, 'wb') as f: # WARNING: can't write objects to file
      for song in songs: f.write(song)
