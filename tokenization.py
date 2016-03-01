# -*- coding: utf-8 -*-
from filters.text import NonAlphaFilter


class Tokenizer(object):

    def __init__(self, filter=None, pre_normalizer=None, post_normalizer=None):
        self._filter = filter or (lambda x: x)
        self._pre_normalizer = pre_normalizer or (lambda x: x)
        self._post_normalizer = post_normalizer or (lambda x: x)

    def __call__(self, *args, **kwargs):
        return self.tokenize(*args, **kwargs)

    def _split(self, text):
        return text.split()

    def tokenize(self, text, *args, **kwrags):
        for token in self._filter(self._split(self._pre_normalizer(text))):
            yield self._post_normalizer(token)


class AlphaTokenizer(Tokenizer):
    """
    Tokenize input text removing all non alpha characters and replacing punctuation chars with a space.
    Input is assumed to be unicode and further filters can be chained by passing a filter to the constructor
    """
    def __init__(self, keep_digits=False, filter=None, pre_normalizer=None, post_normalizer=None):
        super(AlphaTokenizer, self).__init__(filter, pre_normalizer, post_normalizer)
        self._keep_digits = keep_digits
        self._alpha_filter = NonAlphaFilter(keep_digits=self._keep_digits, punct_replacement=' ')

    def _split(self, text):
        return self._alpha_filter.filter(text).split()


