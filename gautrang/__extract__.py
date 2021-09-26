import string
from json import dump, load
from re import search, sub
from html import unescape
from unicodedata import normalize

def clean_title(title):
	return sub(r'\s\s+', ' ', clean_filename(sub(r'[^a-zA-Z0-9]+', ' ', unescape(title).replace('&', 'and')))).strip()

def clean_filename(filename):
	cleaned_filename = normalize('NFKD', filename).encode('ASCII', 'ignore').decode()
	valid_filename_chars = "%s %s" % (string.ascii_letters, string.digits)
	return ''.join(c for c in cleaned_filename if c in valid_filename_chars)

def main():
	b, c = [], []
	with open('result/__all__.json', encoding='utf-8') as file:
		a = load(file)

	for i in a:
		url = search(r"https://storage\.googleapis\.com/.+?/(.+?)\.mp4'", i['url'])
		if url is None:
			print(i['route'])
		else:
			slug = url.group(1)
			title = clean_title(i['title']).lower()
			if i['image'] != '' and not 'no_thumbnail' in i['image'] and '.jpg' in i['image']:
				img = i['image'].split('/')[::-1]
				urljpg = 'https://img.himovies.to/resize/10000x10000/%s/%s/%s/%s' % (img[3], img[2], img[1], img[0])
				jpg = img[0].replace('.jpg', '')[::-1]
				b.append({'title': title, 'url': slug, 'poster': jpg, 'year': i['release'][:4]})
				c.append('%s\n out=%s.jpg\n dir=/img/posters' % (urljpg, jpg))

	with open('result/$-$-3.json', 'w', encoding='utf-8') as file:
		dump(b, file, indent=4, ensure_ascii=False)
	with open('result/img.txt', 'w', encoding='utf-8') as file:
		for i in c:
			file.write(i + '\n')

if __name__ == '__main__':
	main()