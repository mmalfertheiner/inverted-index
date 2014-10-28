from utils import Timer
from query import QueryResult
from ranking import RankProvider
from ranking import RankedResult
from ranking import RankedResultItem

class QueryExecutor:

    index = None
    timer = None

    def __init__(self, index):
        self.index = index


    def executeQueries(self, queryList):
        self.timer = Timer()
        self.timer.start()

        queryMatchingList = []
        executedTokens = 0

        for query in queryList:
            searchTokens = query.getSearchTokens()
            excludedTokens = query.getExcludedTokens()

            searchResult = QueryResult()
            for token in searchTokens:
                executedTokens += 1
                tmpPostingsList = self.index.getDictionary().getPostingsList(token)
                searchResult.addPostingList(token, tmpPostingsList)

            excludedResult = QueryResult()
            for token in excludedTokens:
                tmpPostingsList = self.index.getDictionary().getPostingsList(token)
                excludedResult.addPostingList(token, tmpPostingsList)

            if(len(excludedResult.getItems()) > 0):
                queryMatching = QueryResult.mergeWithExclusions(searchResult, excludedResult)
            else:
                queryMatching = searchResult

            queryMatchingList.append(queryMatching)

        queryMatching = QueryResult.mergeWithIntersection(queryMatchingList)

        rankedResult = RankedResult()
        for doc, queryResultItem in queryMatching.getItems().items():
            rank = RankProvider.provideRank(queryResultItem, executedTokens)
            rankedResultItem = RankedResultItem(doc, rank, queryResultItem)
            rankedResult.addRankedResultItem(rankedResultItem)

        self.timer.stop()

        return rankedResult.getSortedResult()


    def getTimer(self):
        return self.timer
