#!/usr/bin/python
# -*- coding: utf-8 -*-
import unicodedata as ud


def skip_empty_data(method):
    def _wrapper(*args):
        if len(args) == 1 or not args[1]:
            return None

        return method(*args)

    return _wrapper


def ensure_list_input(method):
    def _wrapper(*args):
        list_data = args[1]

        if type(list_data) not in [list, set]:
            if type(list_data) is str:
                list_data = list_data.split()
            else:
                raise Exception("Filter input data must be of type list,set or str")

        return method(args[0], list_data)

    return _wrapper


class Filter(object):
    """
      Filters data. A filter always return the same data type as the input
    """

    def filter(self, data):
        raise NotImplementedError()


class NonAlphaFilter(Filter):

    def __init__(self, keep_spaces=True, keep_digits=False):
        valid_categories = {'Lu', 'Ll'}

        if keep_spaces:
            valid_categories.add('Zs')

        if keep_digits:
            valid_categories.add('Nd')

        self._all = ''.join(unichr(i) for i in xrange(65536))
        self._letters = set(''.join(c for c in self._all if ud.category(c) in valid_categories))
        self._not_letters = ''.join(c for c in self._all if ud.category(c) not in valid_categories)
        self._not_letters_map = dict.fromkeys(map(ord, self._not_letters))

    @skip_empty_data
    def filter(self, text):
        return text.translate(self._not_letters_map)


class StopwordFilter(Filter):
    """
      Filters stop words from the input tokens. Input is expected to be a list
    """
    def __init__(self, stopwords):
        self._stopwords = set(stopwords)  # sets lookup works as a dict and makes search time O(1)

    @skip_empty_data
    @ensure_list_input
    def filter(self, tokens):
        return [t for t in tokens if t not in self._stopwords]
