#!/usr/bin/python
# -*- coding: utf-8 -*-
import string


class Tokenizer(object):

    def __init__(self, filters=None):
        self._filters = filters or []

    def __call__(self, *args, **kwargs):
        return self.tokenize(*args, **kwargs)

    def _split(self, text):
        return text.translate(dict.fromkeys(map(ord, string.punctuation))).split()

    def tokenize(self, text, *args, **kwrags):
        for token in self._split(text):
            for filt in self._filters:
                token = filt.filter(token)

            yield token


class TokenNormalizer(object):

    def __call__(self, *args, **kwargs):
        return self.normalize(*args, **kwargs)

    def normalize(self, token, *args, **kwrags):
        return token
