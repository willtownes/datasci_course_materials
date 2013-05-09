'''
Prints out first ten pages of tweets about a particular keyword.
'''
import urllib,json

def getTweets(term,pages=10):
    '''fetch and yield unicode text of tweets pertaining to the search term'''
    for page in xrange(1,pages+1):
        response = urllib.urlopen("http://search.twitter.com/search.json?q=%s&page=%d"%(term,page))
        results = json.load(response)["results"]
        for tweet in results:
            yield tweet["text"]
        
def main():
    '''print out the tweets'''
    for j in getTweets("microsoft"):
        print(j.encode("utf-8"))
        
if __name__ == "__main__":
    main()