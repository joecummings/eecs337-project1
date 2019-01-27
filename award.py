class Award(object):
    
    def __init__(self, name):
        self.name = name
        self.relevant_tweets = list()
        self.predicate = lambda x: x
        self.nominees = list()
        self.winner = ""

    def makePred(self,l1,l2):
        localPreds = map(lambda x: lambda y: x in y,l1) + map(lambda x: lambda y: x not in y,l2)
        self.predicate = lambda x: if all([f(x) for f in localPreds]) self.relevant_tweets.append(x)

    def mostCommonString(self, regexPattern):
        self.winner = self.mostCommon([filteredString for tweet in self.relevant_tweets for filteredString in re.findall(regexPattern, tweet)])

    def mostCommon(self, lst):
        return max(lst,key=lst.count)