def parse_start_url(self, response):
    item = CompanyItem()
    company_id = response.xpath('//something').extract()
    locations_selector = response.xpath('//locations').extract()

    return self.fetchLocations(locations_selector, company_id, item)

def fetchLocations(self, locations, company_id, item): #response):
    for location in locations:
        if len(location)>1:
            yield Request("http://site.com.au/MVC/Offer/GetLocationDetails/?locationId="+location+"&companyId="+company_id,
            callback=self.parseLocation,
                meta={'company_id': company_id, 'item': item})

def parseLocation(self,response):
    hxs = HtmlXPathSelector(response)
    item = response.meta['item']

    dl = hxs.select("//dl")
    if len(dl)>0:
        address = hxs.select("//dl[1]/dd").extract()
        loc = {'address':remove_entities(replace_escape_chars(replace_tags(address[0], token=' '), replace_by=''))}
        yield loc

    locations_select = hxs.select("//select/option/@value").extract()
    if len(locations_select)>0:
        yield self.fetchLocations(locations_select, response.meta['company_id'], item)