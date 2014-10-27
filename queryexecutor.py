from utils import Timer
from query import QueryResult

class QueryExecutor:

    index = None
    timer = None

    def __init__(self, index):
        self.index = index


    def executeQueries(self, queryList):
        self.timer = Timer()
        self.timer.start()

        queryMatchingList = []
        queryMatching = None

        for query in queryList:
            searchTokens = query.getSearchTokens()
            excludedTokens = query.getExcludedTokens()

            searchResult = QueryResult()
            for token in searchTokens:
                tmpPostingsList = self.getPostingsList(token)
                searchResult.addPostingList(token, tmpPostingsList)

            excludedResult = QueryResult()
            for token in excludedTokens:
                tmpPostingsList = self.getPostingsList(token)
                excludedResult.addPostingList(token, tmpPostingsList)

            if(len(excludedResult.getItems()) > 0):
                queryMatching = QueryResult.mergeWithExclusions(searchResult, excludedResult)
            else:
                queryMatching = searchResult

            queryMatchingList.append(queryMatching)

        queryMatching = QueryResult.mergeWithIntersection(queryMatchingList)

        #TODO: Make sort algorithm
        self.timer.stop()

        return queryMatching


    def getPostingsList(self, token):
        return self.index.getDictionary().getPostingsList(token)


    def getTimer(self):
        return self.timer
