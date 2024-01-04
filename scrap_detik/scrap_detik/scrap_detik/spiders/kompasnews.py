import scrapy
import uuid

random_uuid = uuid.uuid4()

class KompasnewsSpider(scrapy.Spider):
	name = "kompasnews"
	allowed_domains = ["nasional.kompas.com"]
	start_urls = ["https://nasional.kompas.com/"]

	def parse(self, response):
		headline_national_news = self.get_headline_national_news(response)
		latest_national_news = self.get_latest_national_news(response)

		return [
			{
				'title': 'Headline National News',
				'data': headline_national_news,
			},
			{
				'title': 'Latest National News',
				'data': latest_national_news,
			}
		];	
	
	def get_headline_national_news(self, response):
		TAG = 'get_headline_national_news'
		result = []
		items = response.css('div.article__wrap__grid--flex > div')
		
		for item in items:
			result.append({
				'id': random_uuid,
				'category': item.css('div.article__grid > div.article__boxsubtitle > div.article__subtitle::text').get(),
				'link_to': item.css('div.article__grid > div.article__asset > a').attrib['href'],
				'image': item.css('div.article__grid > div.article__asset > a > img').attrib['data-src'],
				'title': item.css('div.article__grid > div.article__box > h3 > a::text').get(),
				'description': item.css('div.article__grid > div.article__box > div.article__lead::text').get(),
				'date': item.css('div.article__grid > div.article__box > div.article__date::text').get(),
			})

		# print('✅ ' + TAG + ' > result', result)
		return result
	
	def get_latest_national_news(self, response):
		TAG = 'get_latest_national_news'
		result = []
		items = response.css('div.latest--news > div.article__list')

		for item in items:
			result.append({
				'category': item.css('div.article__list__info > div.article__subtitle::text').get(),
				'link_to': item.css('div.article__list__title > h3 > a').attrib['href'],
				'title': item.css('div.article__list__title > h3 > a::text').get(),
				'image': item.css('div.article__list__asset > div.article__asset > a > img').attrib['data-src'],
				'description': None,
				'date': item.css('div.article__list__info > div.article__date::text').get(),
			})

		print('✅ ' + TAG  + ' > result', result)
		return result



	# name = "detikspider"
	# allowed_domains = ["books.toscrape.com"]
	# start_urls = ["https://books.toscrape.com"]

	# def parse(self, response):
	# 	books = response.css('article.product_pod')

	# 	for book in books:
	# 		yield {
	# 			'name': book.css('h3 a::text').get(),
	# 			'price': book.css('.product_price .price_color::text').get(),
	# 			'url': book.css('h3 a').attrib['href'],
	# 		}

	# 	next_page = response.css('li.next a::attr(href)').get()

	# 	if (next_page is not None):
	# 		if ('catalogue/' in next_page):
	# 			next_page_url = 'https://books.toscrape.com/' + next_page
	# 		else:
	# 			next_page_url = 'https://books.toscrape.com/catalogue/' + next_page
	# 		yield response.follow(next_page_url, callback=self.parse)

	# 	pass
