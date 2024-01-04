import scrapy
import uuid
import json

random_uuid = uuid.uuid4()

class SindonewsSpider(scrapy.Spider):
	name = "sindonews"
	allowed_domains = ["search.sindonews.com"]
	base_url = "https://search.sindonews.com/go"
	start_urls = [
		"https://search.sindonews.com/go?q=kericuhan&type=artikel",
		"https://search.sindonews.com/go?q=teroris&type=artikel",
	]

	def parse(self, response):
		print('🧭 Scrapping ' + self.name + ': ' + response.url)
		TAG = 'parse'
		result = {
			'url_scrapped': response.url,
			'data': [],
		}
		items = response.css('.news > ul.news-search > li')
		paginationNextPage = response.css('.news > .paging > ul > li > a > i.fa-angle-right')
		paginationPrevPage = response.css('.news > .paging > ul > li > a > i.fa-angle-left')
		paginationCurrentPage = response.css('.news > .paging > ul > li.current')
		paginationCurrentNextPage = response.css('.news > .paging > ul > li.current + li')
		paginationCurrentNextHrefPage = paginationCurrentNextPage.css('a').attrib['href']

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


		with open(f'{self.name}_{response.url.split("/")[-1]}.json', 'w') as json_file:
			json.dump(result, json_file, indent=2)

		
		print('👀 paginationNextPage', paginationNextPage)
		print('👀 paginationCurrentNextPage', paginationCurrentNextPage)
		if (paginationNextPage is not None):
			print('✅ redirect to', paginationCurrentNextHrefPage)

			yield response.follow(
				paginationCurrentNextHrefPage, 
				callback=self.parse,
			)

		# print('✅ Scrapped ' + self.name + ': ' + response.url)
		return result

