import sys,re,json
def makeSentDict(sentFile="AFINN-111.txt"):
    scores = {} 
    with open(sentFile) as afinnfile:
        for line in afinnfile:
            term, score  = line.split("\t")  
            scores[term] = int(score)  
    return scores
def computeScore(tweet,sd):
    words = tweet["text"].split()
    score = 0
    for word in words:
        try: points = sd[word]
        except KeyError: points = 0
        score += points
    return score
def simplifyTweet(tweet):
    return {'text':tweet['text'],'score':None}
def tweetFile2dict(tweetfile,scoreDict={}):
    tweetList = []
    for line in tweetfile:
        tweet = json.loads(line)
        info = simplifyTweet(tweet)
        info['score'] = computeScore(tweet,scoreDict)
        tweetList.append(info)
    return tweetList
def splitTweet(text,scoreDict={}):
    words = text.split()
    return filter(lambda x: x.lower() not in scoreDict, words) 
def wordScore(tweetDict,scoreDict={}):
    scores = {}
    for tweet in tweetDict:
        for word in splitTweet(tweet['text'],scoreDict): 
            try: 
                scores[word]['sumTweetScores'] += tweet['score']
                scores[word]['nTweets'] += 1
            except KeyError: 
                scores[word] = {'sumTweetScores':tweet['score'],'nTweets':1}
    return scores
def getScores(sentFileName,tweetFileName):
    scoreDict = makeSentDict(sentFile=sentFileName)
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
