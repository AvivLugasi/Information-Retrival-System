# Required for downloading the stopwords corpus #
# import nltk
# nltk.download()

from Utils.System import System


class LinguisticProcessor(System):

    def __init__(self):
        """
        Init the stop words set
        """
        self.stop_words_set = set()
        # open stop words file
        self.log("Opening stop words file")
        stop_words_file = self.readFile("Utils/stop_words_english.txt", 'r')

        # read file
        while True:
            # read line
            line = stop_words_file.readline()
            line = line.strip()
            # if reached EOF
            if not line:
                break
            # add stop word
            self.stop_words_set.add(line)

        self.log("Closing stop words file")
        stop_words_file.close()

    def preform_processing(self, tokens_dict=dict, case_folding=True, remove_punctuation=True,
                           remove_stop_words=True, perform_stemming=True):
        """
        Perform a series of linguistic operations on a tokens
         list and return the new terms list that was created from it
        :param perform_stemming: preform if True, else does not preform. By default - it preforms.
        :param remove_punctuation: preform if True, else does not preform. By default - it preforms.
        :param case_folding: preform if True, else does not preform. By default - it preforms.
        :param remove_stop_words: preform if True, else does not preform. By default - it preforms.
        :param tokens_dict : list of pairs (token, token frequency in specific doc)
        """
        # terms list
        terms_dict = {}
        for token in tokens_dict:
            init_token = token
            # perform case folding
            if case_folding: token = self._case_folding(token)
            # remove punctuations
            if remove_punctuation: token = self._remove_punctuation(token)
            # remove stop words
            if remove_stop_words: token = self._remove_stop_words(token)
            # if not a stop word
            if token:
                # perform stemming
                if perform_stemming: term = self._perform_stemming(token)
                # append to terms_dict
                terms_dict[term] = terms_dict[term] + 1 if term in terms_dict else 1

        # return terms list
        return terms_dict

    # ================================================================================================== #
    #                                          Helper Functions                                          #
    # ================================================================================================== #

    def _case_folding(self, token: str):
        """
        Convert a token to lower case and return it
        """
        # lower case
        return token.lower()

    def _remove_punctuation(self, token: str):
        """
        Remove all punctuations from a given token and return it
        """
        import string
        # removing punctuations
        return token.translate(str.maketrans('', '', string.punctuation))

    def _remove_stop_words(self, token: str):
        """
        Remove stop words from token.
         if all the words in the token were stop words it returns None
         else the new token in case that token is longer then one word
        """

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

    def _perform_stemming(self, token: str):
        """
        Perform porter stemming algorithm on a token and return the new term
        """
        from nltk.stem import PorterStemmer
        # porter stemmer
        ps = PorterStemmer()
        term = ""
        # perform stemming on each word in the token in case that token is longer then one word
        for word in token.split():
            term = term + ps.stem(word)
        return term
