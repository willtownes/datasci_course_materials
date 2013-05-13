'''Compute the top ten hashtags from a tweetstream (arg1)'''
import sys,json

def makeTweetStream(tweetFile):
    '''given an open file of tweets, makes an iterator of tweet objects'''
    for line in tweetFile:
        yield json.loads(line)

def makeHashTags(tweetStream):
    '''iterate through a list of tweet objects and return a dictionary of hashTag:frequencyCount'''
    tagDict = {}
    for tweet in tweetStream:
        try: tags = tweet['entities']['hashtags']
        except KeyError: continue
        if len(tags) == 0: continue
        else:
            tags = [t['text'] for t in tags]
            for tag in tags:
                try: tagDict[tag] += 1
                except KeyError: tagDict[tag] = 1
    return tagDict
    
def main():
	with open(sys.argv[1]) as tweetfile:
		tags = makeHashTags(makeTweetStream(tweetfile))
        topTags = sorted(tags, key=lambda x: tags[x])[:10]
	for tag in topTags:
		print('%s %f'%(tag.encode('utf-8'),float(tags[tag])))
		
if __name__ == "__main__":
	main()