class Query:

    searchTokens = []
    excludedTokens = []


    def __init__(self, searchTokens, excludedTokens):
        self.searchTokens = searchTokens
        self.excludedTokens = excludedTokens


    def getSearchTokens(self):
        return self.searchTokens


    def getExcludedTokens(self):
        return self.excludedTokens



class QueryResultItem:

    matches = None

    def __init__(self):
        self.matches = {}


    def addMatch(self, term, count):
        self.matches[term] = count


    def getMatches(self):
        return self.matches


    @staticmethod
    def mergeQueryResultItems(queryResultItems):
        result = QueryResultItem()
        for resultItem in queryResultItems:
            for term, count in resultItem.getMatches().items():
                result.addMatch(term, count)

        return result




class QueryResult:

    items = None

    def __init__(self):
        self.items = {}


    def addPostingList(self, term, postingList):
        for posting in postingList.getPostings():
            self.addPosting(term, posting)


    def addPosting(self, term, posting):
        doc = posting.getDocument()
        if(not doc in self.items):
            self.items[doc] = QueryResultItem()

        self.items[doc].addMatch(term, posting.getCount())


    def addResultItem(self, doc, resultItem):
        self.items[doc] = resultItem


    def getItems(self):
        return self.items


    @staticmethod
    def mergeWithExclusions(searchQueryResult, excludedQueryResult):
        queryResult = QueryResult()

        for doc, searchResultItem in searchQueryResult.getItems().items():
            if(not doc in excludedQueryResult.getItems()):
                queryResult.addResultItem(doc, searchResultItem)

        return queryResult


    @staticmethod
    def mergeWithIntersection(queryMatchingList):
        queryResult = QueryResult()

        if(len(queryMatchingList) == 0):
            return queryResult
        elif(len(queryMatchingList) == 1):
            return queryMatchingList[0]

        for doc, resultItem in queryMatchingList[0].getItems().items():
            exists = True
            tempResultItemList = [resultItem]
            for i in range(1, len(queryMatchingList)):
                if(not doc in queryMatchingList[i].getItems()):
                    exists = False
                    break

                tempResultItemList.append(queryMatchingList[i].getItems()[doc])

            if(exists):
                finalQueryResultItem = QueryResultItem.mergeQueryResultItems(tempResultItemList)
                queryResult.addResultItem(doc, finalQueryResultItem)

        return queryResult



class RankedResult:

    matches = None

    def __init__(self):
        self.matches = []

    def addMatch