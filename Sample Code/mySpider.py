class MySpider(CrawlSpider):
    name = "myspider"
    allowed_domains = ["myspider.com", "myspider.co"]
    start_urls = [
        "http://www.myspider.com/offers/myCity/typeOfAd/?search=fast",
    ]

    #Pagination
    rules = (
        Rule (
            SgmlLinkExtractor()
           , callback='parse_start_url', follow= True),
    )

    #1st page
    def parse_start_url(self, response):

        hxs = HtmlXPathSelector(response)

        next_page = hxs.select("//a[@class='pagNext']/@href").extract()
        offers = hxs.select("//div[@class='hlist']")

        for offer in offers:
            myItem = myItem()

            myItem['url'] = offer.select('.//span[@class="location"]/a/@href').extract()[0]
            myItem['thumb'] = oferta.select('.//div[@class="itemFoto"]/div/a/img/@src').extract()[0]

            request = Request(myItem['url'], callback = self.second_page)
            request.meta['myItem'] = myItem

            yield request

        if next_page:
            yield Request(next_page[0], callback=self.parse_start_url)


    def second_page(self,response):
        myItem = response.meta['myItem']

        loader = myItemLoader(item=myItem, response=response)

        loader.add_xpath('address', '//span[@itemprop="streetAddress"]/text()') 

        return loader.load_item()