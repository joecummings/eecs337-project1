class Predicate(object):

    def __init__(self, name):
        self.name = name
        self.include = list()
        self.exclude = list()
        self.pred = lambda x: x
    
    def makePred(self):
        l1 = list(map(lambda x: lambda y: x in y,self.include))
        l2 = list(map(lambda x: lambda y: x not in y,self.exclude))
        self.pred = lambda x: all([f(x) for f in l1 + l2])
