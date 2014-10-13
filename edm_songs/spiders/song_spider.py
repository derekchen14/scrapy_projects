import scrapy
from edm_songs.items import EdmSongsItem
from scrapy.contrib.spiders import CrawlSpider, Rule
# from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.linkextractors import LinkExtractor

class SongSpider(CrawlSpider):
  name = "song"
  allowed_domains = ["http://www.edmsauce.com/"]
  start_urls = [
    "http://www.edmsauce.com/best-of/best-edm-songs-of-2014/",
    # "http://www.edmsauce.com/best-of/best-edm-songs-of-2013/"
  ]
  rules = (Rule(LinkExtractor(allow=('/page/d+'),restrict_xpaths=('//a[@class="nextpostslink"]')), callback="parse_songs", follow=True),)

  # def start_requests(self):
  #   yield Request(
  #     url="http://www.edmsauce.com/best-of/best-edm-songs-of-2014",
  #     callback=self.parse_songs,
  #     dont_filter=True
  #   )

  def parse_start_url(self, response):
    self.log("\n\n\n Starting to crawl ... \n\n\n")
    return self.parse_songs(response)

  def parse_songs(self, response):
    print ('Crawling page %s' % response.url[-7:-1])
    href = response.css('h2.et_pt_title').xpath('./a/@href').extract()
    text = response.css('h2.et_pt_title').xpath('./a/text()').extract()
    author = response.css('p.et_pt_blogmeta').xpath('./a[contains(@rel, "author")]/text()').extract()
    date = response.css('p.et_pt_blogmeta').xpath('./text()').re('[A-Z][a-z]{2}[\s].+')
    songs = []

    for i, word in enumerate(text):
      encodedText = word.encode('utf-8')
      if '\xe2\x80\x93' not in encodedText:
        href.remove(href[i])
        text.remove(text[i])
        author.remove(author[i])
        date.remove(date[i])
      else:
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
