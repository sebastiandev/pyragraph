#!/usr/bin/python
# -*- coding: utf-8 -*-


class Tokenizer(object):

    def __init__(self, filters=None):
        self._filters = filters or []

    def _split(self, text):
        return text.split()

    def tokenize(self, text):
        for token in self._split(text):
            for filt in self._filters:
                token = filt.filter(token)

            yield token
