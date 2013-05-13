'''
Using sentiment index from (arg1), examine twitterstream file (arg2) and output a dictionary of state:happiness scores
'''
import sys,re,json
_states=('AL','AK','AZ','AR','CF','CL','CT','DL','FL','GA','HA','ID','IL','IN','IA','KA','KY','LA','ME','MD','MS','MC','MN','MI','MO','MT','NB','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VT','VA','WN','WV','WS','WY')

class TweetParseError(Exception):
    '''base exception to raise if error in parsing a tweet'''
    pass
    
class NoTextError(TweetParseError):
    '''exception to raise if no text found for a tweet'''
    pass

class LocationError(TweetParseError):
    '''exception to raise if no location found for a tweet'''
    pass
    
def makeSentDict(sentFile="AFINN-111.txt"): ##copied from tweet_sentiment.py
    '''create the sentiment dictionary from file'''
    scores = {} 
    with open(sentFile) as afinnfile:
        for line in afinnfile:
            term, score  = line.split("\t")  
            scores[term] = int(score)  
    return scores

def computeScore(tweet,sd): ##copied from tweet_sentiment.py with slight modification
    '''compute score of a tweet'''
    try: words = tweet["text"].split()
    except KeyError: raise NoTextError("Tweet had no text field")
    else:
        score = 0
        for word in words:
            try: points = sd[word]
            except KeyError: points = 0
            score += points
        return score
    
def computeLocation(tweet,states):
    '''return the location of a tweet. If no location, raise NoLocationError'''
    try: locText = tweet['place']['full_name']
    except (KeyError,TypeError): #case where tweet['place'] is null or case where 'place' is not a key.
        raise LocationError("Tweet had no location info") 
    else:
        location = locText.split(', ')[-1]
        if location in states: return location #success
        else: raise LocationError("Tweet's location (%s) not in list of states"%location.encode('utf-8'))
    
    
def getScores(sentFile,tweetFile,states=_states):
    '''return dictionary of state:sentiment scores'''
    sentiments = makeSentDict(sentFile)
    stateScores = dict((s,0) for s in states) #initialize score dictionary
    with open(tweetFile) as twf:
        for line in twf:
            tweet = json.loads(line)
            try: 
                score = computeScore(tweet,sentiments)
                state = computeLocation(tweet,states)
            except TweetParseError:
                continue
            else:
                stateScores[state] += score
    return stateScores
    
def main():
    print(max(getScores(sys.argv[1],sys.argv[2])))
        
if __name__ == '__main__':
    main()