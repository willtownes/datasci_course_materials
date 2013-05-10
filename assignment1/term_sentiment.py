'''
Given a file containing sentiment scores for known words (first arg) and a file containing tweets (second arg), 
Compute and return sentiment scores for all words in the tweets that were not found in the known word dictionary
'''

import sys,re,json
#from tweet_sentiment import makeSentDict,computeScore

########This code is copied from tweet_sentiment.py, since the autograder doesn't allow imports#######
def makeSentDict(sentFile="AFINN-111.txt"):
    scores = {} # initialize an empty dictionary
    with open(sentFile) as afinnfile:
        for line in afinnfile:
            term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
            scores[term] = int(score)  # Convert the score to an integer.
    return scores
    
def computeScore(tweet,sd):
    '''take a tweet object and compute its sentiment score based on a given sentiment dictionary (sd)'''
    words = tweet["text"].split() #split text by spaces and return list of words
    score = 0
    for word in words:
        try: points = sd[word]
        except KeyError: points = 0
        score += points
    return score
###################################################End Copied Code block################################

def simplifyTweet(tweet):
    '''given a tweet object, return a dictionary containing the text and a placeholder None score to facilitate easier processing downstream'''
    return {'text':tweet['text'],'score':None}

def tweetFile2dict(tweetfile,scoreDict={}):
    '''takes a readable file object containing tweets, simplifies each tweet and returns a list of {text,score} dictionaries'''
    tweetList = []
    for line in tweetfile:
        tweet = json.loads(line)
        info = simplifyTweet(tweet)
        info['score'] = computeScore(tweet,scoreDict)
        tweetList.append(info)
    return tweetList

def splitTweet(text,scoreDict={}):
    '''takes the text of a tweet, splits into words (removing punctuation), and returns a list of only those words not appearing in the reference dictionary, and not containing numbers or underscores.'''
    pattern = re.compile(r'''
    \w+       #match one or more alphanumeric characters
    '{0,1}    #match zero or one apostrophe
    \w+       #match one or more alphanumeric characters
    ''',flags=re.VERBOSE+re.UNICODE)
    words = re.findall(pattern,text) #list of unicode strings, some of which may contain numbers or underscores
    words = map(lambda x: x.lower(), words) #convert all words to lower case
    badWordPattern = re.compile(r'[0-9_]')
    def keepWord(word):
        '''helper function determines whether to keep the word or not. If the word contains numbers or underscore, False. Otherwise, True'''
        return (re.search(badWordPattern,word) is None) and (word not in scoreDict)
    return filter(keepWord, words) #returns only those words for which keepWord is True

def wordScore(tweetDict,scoreDict={}):
    '''Iterate through the list of tweets in tweetDict, extract all words not in scoreDict, and return nested dictionary of form {word:{nTweets,sumTweetScores}} where nTweets is the number of tweets in tweetDict containing the word and sumTweetScores is the sum of their sentiment scores'''
    scores = {}
    for tweet in tweetDict:
        for word in splitTweet(tweet['text'],scoreDict): #might wrap the iterable in set() to exclude double counting repeated words in single tweet.
            try: #case where word already exists in new dictionary
                scores[word]['sumTweetScores'] += tweet['score']
                scores[word]['nTweets'] += 1
            except KeyError: #new word, add to the dictionary
                scores[word] = {'sumTweetScores':tweet['score'],'nTweets':1}
    return scores

def getScores(sentFileName,tweetFileName):
    '''top level function yields an iterator over unique word,score tuples for all words found in tweets of tweetFile but not already in reference dictionary sentFile. Score is a float. Word's sentiment score = sum(scores of tweets containing the word)/count(tweets containing the word)'''
    scoreDict = makeSentDict(sentFile=sentFileName) #dictionary of {word:score} pairs.
    with open(tweetFileName) as tweetfile:
        tweetDict = tweetFile2dict(tweetfile,scoreDict)
    newScores = wordScore(tweetDict,scoreDict)
    for word in newScores:
        yield word,float(newScores[word]['sumTweetScores'])/newScores[word]['nTweets']
        
        
def main():
    for w in getScores(sys.argv[1],sys.argv[2]):
        print("%s %f"%(w[0].encode('utf-8'),w[1]))

if __name__ == '__main__':
    main()
