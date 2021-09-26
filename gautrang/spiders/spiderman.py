import scrapy
from gautrang.items import GogoItem
from scrapy_splash import SplashRequest
from re import findall, search
from json import load, dump, dumps
from requests import get
from math import ceil

class HiMovies(scrapy.Spider):
	name = 'himovies'
	# allowed_domains = ["theshit.me", "www2.6movies.net", "www1.movieorca.com", "www1.movierot.com", "www.actvid.com", "www.tikmovies.com", "www.dopebox.net", "fboxtv.com", "tinyzonetv.to", "sflix.to", "cineb.net", "www.freshmoviestreams.net", "kk01.net", "myflixerhd.ru", "www.moviecrumbs.net", "myflixer.link", "myflixer.to", "myflixer.com", "myflixertv.to", "ainiesta.com", "www3.f2movies.to", "www1.bemovies.to", "ev01.to", "flixhd.cc", "www.iwatchfreestreams.to", "www3.musichq.net", "www1.zoechip.com", "zoechip.org", "www1.attacker.tv", "quitt.net", "www1.seeingblind.net", "fmovie.ws", "bemovies.cc", "www6.123moviesgo.tv", "moviecracker.net", "www1.ummagurau.com", "fmovieshd.vip", "moviesjoy.to", "www.ladresstina.com", "www.redbeltmovie.com", "fullmoviehd4k.com", "cataz.net", "tinyzonetv.to", "tinyzonetv.cc", "www.showboxmovies.net", "www.watch4freemovies.com", "www2.filmlicious.net", "www.fullmoviefilm.org", "www.moviekids.tv", "www.freemovies360.com/"]
	allowed_domains = ["www5.himovies.to", "www2.theshit.me", "www2.6movies.net", "www1.movieorca.com", "www1.movierot.com"]
	start_urls = []
	script = '''function main(splash, args) assert(splash:go(args.url)) while not splash:select('.dp-w-c-play') do assert(splash:wait(0.1)) end assert(splash:wait(0.5)) local title = splash:select('h2.heading-name a').node.innerHTML local image = splash:select('div[class="film-poster mb-2"]').innerHTML local description = splash:select('div.description').node.innerHTML local release = splash:select_all('div.row-line')[1].node.innerHTML assert(splash:select('.dp-w-c-play'):mouse_click()) while not splash:select('#modalshare div div div button') do assert(splash:wait(0.1)) end assert(splash:wait(5)) assert(splash:select('#modalshare div div div button'):mouse_click()) assert(splash:wait(10)) return { entries = splash:har()['log']['entries'], title = title, image = image, description = description, release = release } end'''

	def start_requests(self):
		for url in self.start_urls_from_txt():
			yield SplashRequest(url, meta={'splash': {'endpoint': 'execute', 'args': {'lua_source': self.script}}}, callback=self.parse)

	def start_urls_from_txt(self):
		routes = []
		with open('result/__offset__.json', 'r', encoding='utf-8') as file:
			routes = load(file)
		i = ceil(len(routes) / len(self.allowed_domains))
		for (domain, route) in zip(self.allowed_domains * i, routes):
			self.start_urls.append('https://%s%s' % (domain, route))
		return self.start_urls

	def parse(self, response):
		title = response.data['title']
		image = search(r'src=\"(.+?)\"', response.data['image']).group(1)
		description = response.data['description'].replace('\n', '').replace('\"', '\'').strip()
		release = search(r'(\d{4}\-\d{2}\-\d{2})', response.data['release']).group(1)
		url = ''
		for entry in response.data['entries']:
			uri = entry['request']['url']
			if 'streamrapid.ru/ajax/embed-4/getSources' in uri:
				url = get(uri).text.replace('\"', '\'')
				domain = '/movie/%s' % response.url.split('/')[4]
				print('"%s",' % domain)
				yield {
					'route': domain,
					'title': title,
					'image': image,
					'description': description,
					'release': release,
					'url': url,
				}