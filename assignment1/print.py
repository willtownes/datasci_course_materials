'''
Prints out first ten pages of tweets about a particular keyword.
'''
import urllib,json

def getTweets(term,pages=10):
    '''fetch and yield (in json) tweets pertaining to the search term'''
    for page in xrange(1,pages+1):
        response = urllib.urlopen("http://search.twitter.com/search.json?q=%s&page=%d"%(term,page))
        yield json.load(response)
        
def main():
    '''print out the tweets'''
    for j in getTweets("microsoft"):
        print(j)
        
if __name__ == "__main__":
    main()