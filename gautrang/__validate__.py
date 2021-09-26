from json import load, dump

def main():
	remain = []
	with open('src/__all__.json', encoding="utf-8") as file:
		all = load(file)

	with open('src/__crawled__.json', encoding="utf-8") as file:
		had = load(file)

	for movie in all:
		found = False
		for movie_ in had:
			if movie == movie_:
				found = True
				break
		if not found:
			remain.append(movie)
	remain.sort()
	remain = list(dict.fromkeys(remain))
	with open('result/__offset__.json', 'w', encoding="utf-8") as file:
		dump(remain, file, indent=4, ensure_ascii=False)

if __name__ == '__main__':
	main()