import nltk
import files
from collections import Counter


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


def getTermDictionary(tokens):
    return nltk.FreqDist(tokens)


def getNmostFrequentTerms(dictionary, n):
    #calculates the frequency for all the given tokens and returns the n most common
    #frequency distribution tells us the frequency of each vocabulary item in the text.
    return dictionary.most_common(n)


def printFrequencyTerms(termList):
    #prints the list of terms and their according frequency on console
    for elem in termList:
        print(elem[0] + "\t\t[ " + str(elem[1]) + " ]")


## Main programm
path = "books/"
books = files.loadBooksFromFolder(path)

dictionary = Counter()

for book in books:
    text = loadBookText(book)
    text = getTokenizedList(text)
    print(book)
    print("Total # of terms: " + str(getNoOfTerms(text)))
    print("Total # of unique terms: " + str(getNoOfUniqueTerms(text)))
    print("50 most frequent terms: ")
    temp = getTermDictionary(text)
    printFrequencyTerms(getNmostFrequentTerms(temp, 50))
    dictionary = dictionary + Counter(temp)

print("\nLenght of overall dictionary:")
print(len(dictionary.keys()))
print("\n50 most frequent terms in overall dictionary:")
printFrequencyTerms(getNmostFrequentTerms(dictionary, 50))
