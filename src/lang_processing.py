#!-*- coding: utf8 -*-
from sklearn.naive_bayes import MultinomialNB

import pandas
import nltk
import os


class NLTK:
    """This class make the natural language processing for a given text input.

    """
    def __init__(self, model=MultinomialNB):
        self.dataFrame = pandas.read_csv(os.path.abspath(os.getcwd() + os.sep + os.pardir + '/data/dataset.csv'), sep=';')
        self.stopwords = nltk.corpus.stopwords.words("portuguese")
        self.stemmer = nltk.stem.RSLPStemmer()

        self.df_values = self.dataFrame['phrase']
        self.df_tags = self.dataFrame['answer']

        self.lowerText = self.df_values.str.lower()
        self.df_token = [nltk.tokenize.word_tokenize(i) for i in self.lowerText]

        self.model = model()

    # Used in main function
    def cleaning_dict(self):
        """This function creates and fill a set of stem valid words.

        Returns
        -------
        valid_words : dict
            Dictionary with stem valid words.

        """
        dictionary = set()
        for i in self.df_token:
            valid_words = [self.stemmer.stem(nxDF) for nxDF in i if nxDF not in self.stopwords]
            dictionary.update(valid_words)

        tuples = zip(dictionary, range(len(dictionary)))

        return {word: i for word, i in tuples}

    # Used in fit
    def vectorise(self, txt, librarian):
        """This function vectorises a text input.

        Parameters
        ----------
        txt : str
            Text input.
        librarian : dict
            Dictionary with stem valid words.
        Returns
        -------
        vectorized_array : list
            List with the frequency of the Text input.

        """
        vectorized_array = [0] * len(librarian)
        for word in txt:
            if len(word) > 0:
                stem = self.stemmer.stem(word)
                if stem in librarian:
                    position = librarian[stem]
                    vectorized_array[position] += 1

        return vectorized_array

    def fit(self, librarian):
        """This function fits the chosen model.

        Parameters
        ----------
        librarian : dict
            Dictionary with stem valid words.
        Returns
        -------
        model : sklearn.Model
            Fitted model.

        """
        x = [self.vectorise(txt, librarian) for txt in self.df_token]
        y = self.df_tags

        return self.model.fit(x, y)

    def pred(self, model, phrase, librarian):
        """This function makes prediction for the given text input.

        Parameters
        ----------
        model : sklearn.Model
            Fitted model.
        phrase : str
            Inputted text.
        librarian : dict
            Dictionary with stem valid words.
        Returns
        -------
        x[0] : str
            Answer for the given text input.

        """
        phrase_ = self.vectorise(nltk.tokenize.word_tokenize(phrase), librarian)
        x = model.predict([phrase_])

        return x[0]

    def __call__(self, *args, **kwargs):
        """Main function

        Parameters
        ----------
        args
        kwargs

        Returns
        -------

        """
        self.__init__(MultinomialNB)
        librarian = self.cleaning_dict()
        model = self.fit(librarian)

        while True:
            phrase = input('Input a phrase: ')
            print(self.pred(model, phrase, librarian))


if __name__ == '__main__':
    NLTK().__call__()
