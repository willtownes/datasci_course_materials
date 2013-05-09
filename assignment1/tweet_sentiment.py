import sys,json

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

def main():
    scores = makeSentDict(sentFile=sys.argv[1])
    with open(sys.argv[2]) as tweetfile:
        for line in tweetfile:
            tweet = json.loads(line)
            print(computeScore(tweet,scores))

if __name__ == '__main__':
    main()
