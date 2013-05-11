import sys,json

def main():
	hist = {}
	total = 0
	with open(sys.argv[1]) as tweetfile:
		for line in tweetfile:
			words = json.loads(line)['text'].split()
			total += len(words)
			for word in words:
				try: hist[word] += 1 #existing word
				except KeyError: hist[word] = 1 #new word
	total = float(total)
	for word in hist:
		print('%s %f'%(word.encode('utf-8'),hist[word]/total))
		
if __name__ == "__main__":
	main()