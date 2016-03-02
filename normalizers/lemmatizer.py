# -*- coding: utf-8 -*-
from pattern.es import lemma, tag
from pattern import text
from base import Normalizer


class SpanishLemmatizer(Normalizer):

    def __init__(self, next_normalizer=None):
        super(SpanishLemmatizer, self).__init__(next_normalizer)

    def _apply_normalizer(self, data):
        lemma_word = lambda x: lemma(x) if tag(x)[0][1] == text.VB else x
        lemma_word_list = lambda xl: [lemma_word(w) for w in xl]
        return lemma_word(data) if not isinstance(data, (list, tuple)) else lemma_word_list(data)

