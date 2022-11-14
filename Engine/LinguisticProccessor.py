# Required for downloading the stopwords corpus #
## import nltk
## nltk.download()

from Utils.System import System

class Processor(System):

    def __init__(self):
        """Init the stop words set"""
        self.stop_words_set = set()
        stop_words_file = self.readFile("Utils/stop_words_english.txt", 'r')

        while True:
            line = stop_words_file.readline()
            line = line.strip()
            if not line:
                break
            self.stop_words_set.add(line)

        stop_words_file.close()

    def caseFolding(self, token: str):
        """Convert a token to lower case and return it"""
        # lower case
        return token.lower()

    def removePunctuation(self, token: str):
        """Remove all punctuations from a given token and return it"""
        import string
        # removing punctuations
        return token.translate(str.maketrans('', '', string.punctuation))

    def removeStopWords(self, token: str):
        """Remove stop words from token if all the words in the token were stop words it return None else
        the new token"""

        new_token = ""

        # loop the words in the token
        for word in token.split():
            # add word to the new token if it does not a stop word
            if word not in self.stop_words_set:
                new_token = new_token + word

        # return None if all the token's words were stop words
        if new_token == "":
            return None
        return new_token

    def performStemming(self, token: str):
        """Perform porter stemming algorithm on a token and return the new term"""
        from nltk.stem import PorterStemmer

        # porter stemmer
        ps = PorterStemmer()
        term = ""

        # perform stemming on each word in the token
        for word in token.split():
            term = term + ps.stem(word)

        return term

    def linguisticProccessing(self, token: str):
        """Perform a series of linguistic operations on a token and return the new term that was created from it"""

        # perform case folding
        token = self.caseFolding(token)
        # remove punctuations
        token = self.removePunctuation(token)
        # remove stop words
        token = self.removeStopWords(token)
        # if all the words were stop words
        if not token:
            return None
        # perform stemming
        term = self.performStemming(token)
        return term