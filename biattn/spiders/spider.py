import scrapy

from scrapy.loader import ItemLoader

from ..items import BiattnItem
from itemloaders.processors import TakeFirst


class BiattnSpider(scrapy.Spider):
	name = 'biattn'
	start_urls = ['https://www.biat.com.tn/biat-la-une/actualites']

	def parse(self, response):
		post_links = response.xpath('//*[(@id = "block-biat-corporate-content")]//h2/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//li[@class="pager__item--next"]/a/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//*[(@id = "block-biat-corporate-breadcrumbs")]//span/text()').get()
		description = response.xpath('//*[(@id = "block-biat-corporate-content")]//p//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//*[(@id = "block-biat-corporate-content")]//*[contains(concat( " ", @class, " " ), concat( " ", "field--name-node-post-date", " " ))]/text()').get()

		item = ItemLoader(item=BiattnItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
