from utils import Timer

class QueryExecutor:

    index = None
    timer = None

    def __init__(self, index):
        self.index = index


    def executeQueries(self, queryList):
        self.timer = Timer()
        self.timer.start()

        queryMatchings = []
        for run,query in enumerate(queryList):
            searchTokens = query.getSearchTokens()
            excludedTokens = query.getExcludedTokens()

            postingsListSearchTok = []
            for token in searchTokens:
                tmpPostingsList = self.getPostingsList(token)
                postingsListSearchTok.extend(tmpPostingsList.getSortedPostingsList())

            postingsListExcludedTok = []
            for token in excludedTokens:
                tmpPostingsList = self.getPostingsList(token)
                postingsListExcludedTok.extend(tmpPostingsList.getSortedPostingsList())

            postingsList = self.removeExcludedTokensFromResult(postingsListSearchTok, postingsListExcludedTok)

            if run == 0:
                queryMatchings.extend(postingsList)
            else:
                queryMatchings = self.mergeLogicalANDOperationPostings(queryMatchings, postingsList)

        self.timer.stop()

        return queryMatchings


    def getPostingsList(self, token):
        return self.index.getDictionary().getPostingsList(token)


    def mergeLogicalANDOperationPostings(self, list1, list2):
        resultList = []
        i = 0
        j = 0

        while(i<len(list1) and j < len(list2)):
            posting1 = list1[i]
            posting2 = list2[j]
            if posting1.getPath() == posting2.getPath():
                resultList.append(posting1)
                i += 1
                j += 1
            elif posting1.getPath() < posting2.getPath():
                i += 1
            else:
                j += 1

        return resultList


    def removeExcludedTokensFromResult(self, search, exclude):
        resultPostings = search
        i = 0
        j = 0

        while(i<len(search) and j < len(exclude)):
            posting1 = search[i]
            posting2 = exclude[j]
            if posting1.getPath() == posting2.getPath():
                resultPostings.pop(i)
                i += 1
                j += 1
            elif posting1.getPath() < posting2.getPath():
                i += 1
            else:
                j += 1

        return resultPostings


    def getTimer(self):
        return self.timer
