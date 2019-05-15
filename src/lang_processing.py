#!-*- coding: utf8 -*-
from sklearn.naive_bayes import MultinomialNB

import pandas
import nltk
import os


class NLTK:
    def __init__(self, model):
        self.dataFrame = pandas.read_csv(os.path.abspath(os.getcwd() + os.sep + os.pardir + '/data/dataset.csv'), sep=';')
        self.stopwords = nltk.corpus.stopwords.words("portuguese")
        self.stemmer = nltk.stem.RSLPStemmer()

        self.xDF = self.dataFrame['phrase']
        self.yDF = self.dataFrame['answer']

        self.lowerText = self.xDF.str.lower()
        self.nxDF = [nltk.tokenize.word_tokenize(i) for i in self.lowerText]

        self.model = model()

    def cleaning_dict(self):
        dictionary = set()

        for i in self.nxDF:
            valid_words = [self.stemmer.stem(nxDF) for nxDF in i if nxDF not in self.stopwords]
            dictionary.update(valid_words)

        tuples = zip(dictionary, range(len(dictionary)))

        return {word: i for word, i in tuples}

    def vectorise(self, txt, librarian):
        vectorized_array = [0] * len(librarian)
        for word in txt:
            if len(word) > 0:
                stem = self.stemmer.stem(word)
                if stem in librarian:
                    position = librarian[stem]
                    vectorized_array[position] += 1

        return vectorized_array

    def fit(self, librarian):
        x = [self.vectorise(txt, librarian) for txt in self.nxDF]
        y = self.yDF

        return self.model.fit(x, y)

    def pred(self, model, phrase, librarian):
        phrase_ = self.vectorise(nltk.tokenize.word_tokenize(phrase), librarian)
        x = model.predict([phrase_])

        return x[0]


if __name__ == '__main__':
    o = NLTK(MultinomialNB)
    librarian = o.cleaning_dict()
    multinomial = o.fit(librarian)

    while True:
        phrase = input('Insira uma frase: ')
        print(o.pred(multinomial, phrase, librarian))
