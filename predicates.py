class Predicate(object):

    def __init__(self, name):
        self.name = name
        self.include = list()
        self.exclude = list()
        self.pred = lambda x: x

    
    def makePred(self):
        anyFunctions = []
        for local_or_string in self.include
            anyFunctions.append(lambda x: any(map(lambda y: lambda x: y in x,local_or_string.split(','))))
        for local_or_string in self.exclude            
            anyFunctions.append(lambda x: any(map(lambda y: lambda x: y not in x,local_or_string.split(','))))
        self.pred = lambda x: all(f(x) for f in anyFunctions)


        # for each thing needs to return a function that has to return True
        #     those functions ask or
        # string

        # each string becomes an any function
        # all the any functions become one big and function
        # for local_or in local_or_string.split(',')

        #     for local_or_string in self.include for local_or in local_or_string.split(',')

        #     for 
        # l1 = list(map(lambda x: lambda y: x in y,self.include))
        # l2 = list(map(lambda x: lambda y: x not in y,self.exclude))
        # self.pred = lambda x: all([f(x) for f in l1 + l2])
