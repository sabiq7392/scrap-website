import scrapy
import uuid
import json
import os
random_uuid = uuid.uuid4()

class SindonewsSpider(scrapy.Spider):
	name = "sindonews"
	allowed_domains = ["search.sindonews.com"]
	base_url = "https://search.sindonews.com/go"
	start_urls = [
		"https://search.sindonews.com/go?q=kericuhan&type=artikel",
		"https://search.sindonews.com/go?q=teroris&type=artikel",
		"https://search.sindonews.com/go?q=demo&type=artikel",
		"https://search.sindonews.com/go?type=artikel&q=bom"
	]

	def parse(self, response):
		print('🧭 Scrapping ' + self.name + ': ' + response.url)
		TAG = 'parse'
		result = {
			'url_scrapped': response.url,
			'data': [],
		}
		script_dir = os.path.dirname(os.path.abspath(__file__))
		dump_dir = os.path.abspath(os.path.join(script_dir, '../../../dumps'))
		file_path = f'{dump_dir}/{self.name}_{response.url.split("/")[-1]}.json'
		
		items = response.css('.news > ul.news-search > li')
		pagination_next_page = response.css('.news > .paging > ul > li > a > i.fa-angle-right')
		pagination_prev_page = response.css('.news > .paging > ul > li > a > i.fa-angle-left')
		pagination_current_page = response.css('.news > .paging > ul > li.current')
		pagination_current_next_page = response.css('.news > .paging > ul > li.current + li')
		pagination_current_next_href_page = pagination_current_next_page.css('a').attrib['href']

		for item in items: 
			result['data'].append({
				'id': str(random_uuid),
				'category': item.css('.news-content > .news-channel > .channel::text').get(),
				'link_to': item.css('.news-pict > a').attrib['href'],
				'image': item.css('.news-pict > a > img').attrib['data-src'],
				'title': item.css('.news-content > .news-title > a::text').get(),
				'description': item.css('.news-content > .news-summary::text').get(),
				'date': item.css('.news-content > .news-channel > .news-date::text').get(),
			})


		with open(file_path, 'w') as json_file:
			json.dump(result, json_file, indent=2)

		if (pagination_next_page is not None):
			print('✅ redirect to', pagination_current_next_href_page)

			yield response.follow(
				pagination_current_next_href_page, 
				callback=self.parse,
			)

		print('✅ Scrapped ' + self.name + ': ' + response.url)
		return result

