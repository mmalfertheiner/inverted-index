import nltk
import files


def loadBookText(filename):
    return open(filename, 'rU').read()


def getTokenizedList(inputStr):
    #uses nltk word_tokenizer to gain all tokens, removes punctuation and converts remaining tokens to lower case
    origTokenList = nltk.word_tokenize(inputStr)
    # isalpha() - test if s is non-empty and all characters in s are alphabetic
    modifiedTokenList = [token.lower() for token in origTokenList if token.isalpha()]
    return modifiedTokenList


def getNoOfTerms(tokens):
    return len(tokens)


def getNoOfUniqueTerms(tokens):
    return len(set(tokens))


def getNmostFrequentTerms(tokens, n):
    #calculates the frequency for all the given tokens and returns the n most common
    #frequency distribution tells us the frequency of each vocabulary item in the text.
    freqency = nltk.FreqDist(tokens)
    return freqency.most_common(n)


def printFrequencyTerms(termList):
    #prints the list of terms and their according frequency on console
    for elem in termList:
        print(elem[0] + "\t\t[ " + str(elem[1]) + " ]")


## Main programm
path = "books/"
books = files.loadBooksFromFolder(path)


for book in books:
    text = loadBookText(book)
    text = getTokenizedList(text)
    print("Total # of terms: " + str(getNoOfTerms(text)))
    print("Total # of unique terms: " + str(getNoOfUniqueTerms(text)))
    frequency = getNmostFrequentTerms(text, 50)
    print("50 most frequent terms: ")
    printFrequencyTerms(frequency)
