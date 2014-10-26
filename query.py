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