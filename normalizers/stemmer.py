# -*- coding: utf-8 -*-
from nltk.stem.snowball import SpanishStemmer as NLTKSpanishStemmer
from base import Normalizer


class SpanishStemmer(Normalizer):

    def __init__(self, next_normalizer=None):
        super(SpanishStemmer, self).__init__(next_normalizer)
        self._stemmer = NLTKSpanishStemmer()

    def _apply_normalizer(self, data):
        stem_word = lambda x: self._stemmer.stem(x)
        stem_word_list = lambda xl: [stem_word(w) for w in xl]
        return stem_word(data) if not isinstance(data, (list, tuple)) else stem_word_list(data)


