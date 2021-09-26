from requests import get
from lxml import html
from json import dump

def request_movie(domain):
	all_slugs = []
	for page in range(1, 2):
		dom = html.fromstring(get('https://%s/movie' % domain, params={'page': page}).text)
		urls = dom.xpath('//div[@class="film_list-wrap"]/div[@class="flw-item"]/div[@class="film-poster"]/a/@href')
		for url in urls:
			all_slugs.append(url)

	with open('result/__all__.txt', 'w', encoding='utf-8') as file:
		dump(all_slugs, file, ensure_ascii=False, indent=4)

def request_info(domain, slug):
	dom = html.fromstring(get('https://%s%s' % (domain, slug)).text)
	urls = dom.xpath('//div[@id="iframe-embed"]')

if __name__ == '__main__':
	request_movie('www2.theshit.me')