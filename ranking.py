class RankedResult:

    rankedResult = None

    def __init__(self):
        self.rankedResult = []


    def addRankedResultItem(self, rankedResultItem):
        self.rankedResult.append(rankedResultItem)


    def getSortedResult(self):
        return sorted(self.rankedResult, key=lambda rankedResultItem: rankedResultItem.getRank(), reverse=True)


class RankedResultItem:

    doc = None
    rank = None
    queryResultItem = None

    def __init__(self, doc, rank, queryResultItem):
        self.doc = doc
        self.rank = rank
        self.queryResultItem = queryResultItem


    def getRank(self):
        return self.rank


    def getDocument(self):
        return self.doc


class RankProvider:

    @staticmethod
    def provideRank(queryResultItem, numberOfQueryTerms):
        return len(queryResultItem.getMatches()) / numberOfQueryTerms