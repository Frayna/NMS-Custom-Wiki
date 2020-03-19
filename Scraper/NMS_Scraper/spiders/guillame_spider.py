import scrapy

from NMS_Scraper.items import NmsRessourceItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class QuotesSpider(scrapy.Spider):
    name = "NMS_Ressources"
    domain = "https://nomanssky.gamepedia.com"
    def start_requests(self):
        urls = [
            'https://nomanssky.gamepedia.com/Resource',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        links = response.css("#mw-content-text > div > table.wikitable > tbody > tr > td:nth-child(2) > a").re("\"(/[^\s]*)\"")
        for link in links:
            yield scrapy.Request(url=self.domain+link, callback=self.parseressource)

    def parseressource(self, response):
        page = response.url.split("/")[-2]
        table = response.css('#mw-content-text .infoboxtable > tbody > tr > * ::text').getall()
        ressource = NmsRessourceItem()
        imgLink = response.css('#mw-content-text .infoboxtable > tbody > tr:nth-child(2) > th > a').attrib['href']
        for i, data in enumerate(table):
            data = data.rstrip()
            if i == 0:
                ressource['name'] = data
            if data == "Symbol":
                ressource['symbol'] = table[i + 1].rstrip()
            if data == "Category":
                ressource['category'] = table[i + 1].rstrip()
            if data == "Type":
                ressource['type'] = table[i + 1].rstrip()
            if data == "Rarity":
                ressource['rarity'] = table[i + 1].rstrip()
            if data == "Blueprint Value":
                ressource['value'] = table[i + 1].rstrip()
            if data == "Used for":
                ressource['usedFor'] = table[i + 1].rstrip()
        yield scrapy.Request(url=self.domain+imgLink, callback=self.parseimg, cb_kwargs=dict(ressource=ressource))

    def parseimg(self, response, ressource):
        ressource['img'] = response.css('#file > a > img').attrib['src']
        print("test");
        print(ressource)
        yield ressource

        #print(table)
        # tablebody = response.css('#mw-content-text .infoboxtable > tbody > tr > td::text').getall()
        # print("TH".join(tablehead) + "\nTD".join(tablebody) + "\n")
        # for tr in table :
        #     print(table.css("tr").get())
        # print(repr("Name : " + response.css('#mw-content-text .infoboxtable .infoboxname::text').get().rstrip()))
        #     if(response.css('#mw-content-text .infoboxtable > tbody > tr:nth-child(3) > th::text').get().rstrip() == "Category") :
        #         print("Category : " + response.css('#mw-content-text .infoboxtable > tbody > tr:nth-child(3) > td::text').get().rstrip())
        #     else
        #         print("Category : " + "")
        # print("-------------------------------------")

        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename)
