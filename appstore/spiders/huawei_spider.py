import scrapy
import re
from scrapy.selector import Selector
from appstore.items import AppstoreItem
from scrapy_splash import SplashRequest

class HuaweiSpider(scrapy.Spider):
	name = "huawei"
	allowed_domains = ["huawei.com"]
	def start_requests(self):
		# headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
		start_urls = ["http://appstore.huawei.com/more/all"]
		for url in start_urls:
			# yield scrapy.Request(url=url, headers=headers)
			# yield SplashRequest(url, args={'wait': 0.5}, 
			#	'endpoint': 'render.html',
			# })
			yield scrapy.Request(url=url)


	def parse(self, response):
		page = Selector(response)
		hrefs = page.xpath('//h4[@class="title"]/a/@href')
		# add one user agent to avoid block is enough for huawei appstore
		# headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'} 
		count = 0
		for href in hrefs:
			if count > 2:
				return 
			url = href.extract()
			# yield scrapy.Request(url=url, headers=headers, callback=self.parse_item)
			yield scrapy.Request(url=url, callback=self.parse_item)


		## get next pages: scrapy can gaurantee no duplicate url is requested
		## next page is dynamic code so we need to render javascript
		# page_ctrl = page.xpath('//div[@class="page-ctrl ctrl-app"]')
		# hasNextPage = page_ctrl.xpath('.//em[@class="arrow-grey-lt"]').extract()
		
		# PAGES_WANT = 3
		
		# if hasNextPage:
		# 	current_page = int(page_ctrl.xpath('./span[not(@*)]/text()').extract_first())
		# 	print "####### current page number:", current_page

		# 	if current_page >= PAGES_WANT:#get first (PAGES_WANT - 1) pages
		# 		return 
		# 	next_page = str(current_page + 1)
		# 	next_url = self.start_urls[0] + "/" + next_page

		# 	request = scrapy.Request(url=next_url, callback=self.parse, meta={
		# 		'splash':{
		# 			'endpoint': 'render.html',
		# 			'args': {'wait': 0.5}
		# 		},

		# 	})



	def parse_item(self, response): ## get details
		page = Selector(response)
		item = AppstoreItem()

		item['title'] = page.xpath('//ul[@class="app-info-ul nofloat"]/li/p/span[@class="title"]/text()').extract_first().encode('utf-8')
		item['url'] = response.url
		item['appid'] = re.match(r'http://.*/(.*)', item['url']).group(1)
		item['intro'] = page.xpath('//meta[@name="description"]/@content').extract_first().encode('utf-8')
		item['thumbnail'] = page.xpath('//ul[@class="app-info-ul nofloat"]/li[@class="img"]/img[@class="app-ico"]/@src').extract_first()

		divs = page.xpath('//div[@class="open-info"]')
		recomm = ""
		for div in divs:
			url = div.xpath('./p[@class="name"]/a/@href').extract_first()
			recommended_appid = re.match(r'http://.*/(.*)', url).group(1)
			name = div.xpath('./p[@class="name"]/a/text()').extract_first().encode('utf-8')
			recomm += "{0}:{1}\t".format(recommended_appid, name)

		item['recommened'] = recomm
		yield item
