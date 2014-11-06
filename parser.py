import nltk
from enum import Enum
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from query import Query


class ParserType(Enum):
    simple = 1
    wordprocessing = 2


class Parser:

    type = None
    stemmer = None
    lemmatizer = None
    stopWords = None

    def __init__(self, type):
        self.type = type
        if self.type == ParserType.wordprocessing:
            self.stemmer = PorterStemmer() #set stemmer
            self.lemmatizer = WordNetLemmatizer() #set lemmatizer
            self.stopWords = stopwords.words("english") #english stop words def


    def parseTokensFromText(self, text):
        tokenList = nltk.word_tokenize(text)

        if self.type == ParserType.wordprocessing:
            parsedTokenList = [self.applyTextProcessing(token.lower()) for token in tokenList if (token.isalpha()) and (not token.lower() in self.stopWords)]
        else:
            parsedTokenList = [token.lower() for token in tokenList if token.isalpha()]

        return parsedTokenList


    def parseQuery(self, queryInput):
        #Split query by + operator
        rawQueries = queryInput.split(sep="+")
        parsedQueries = []

        for rawQuery in rawQueries:
            searchTokens = []
            excludedTokens = []
            for token in rawQuery.strip().split(sep=" "):
                token.lower()
                if self.type == ParserType.wordprocessing:
                    if not token in self.stopWords: #omit stop words
                        #exclude terms with a - operator
                        if(token.startswith('-')):
                            excludedToken = self.applyTextProcessing(token[1:])
                            excludedTokens.append(excludedToken)
                        else:
                            searchTokens.append(self.applyTextProcessing(token))
                else:
                    if(token.startswith('-')):
                        excludedTokens.append(token[1:])
                    else:
                        searchTokens.append(token)
            parsedQueries.append(Query(searchTokens, excludedTokens))

        return parsedQueries


    def applyTextProcessing(self, token):
        stemmedToken = self.applyStemming(token)
        return self.applyLemmatization(stemmedToken)

    def applyStemming(self, token):
        """applies the stemming algorithm to the given token"""
        return self.stemmer.stem(token)

    def applyLemmatization(self, token):
        return self.lemmatizer.lemmatize(token)