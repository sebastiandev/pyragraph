# -*- coding: utf-8 -*-

from collections import Counter
from pyragraph.tokenization import AlphaTokenizer
from itertools import chain, starmap, repeat


class CorpusCounter(Counter):
    """
    Extends the standard Counter adding the numbers of docs where each word appeared. Input can be any iterable.
    Since its intended for documents, iterable items are considered documents.

    If passed a string each word will be considered as a doc. For counting chars use the regular Counter.

    A particular tokenizer and token normalizer can be specified to customize the way words/tokens are treated and
    formatted before counting. Both can inherit from :class Tokenizer: or :class Normalizer: or can also be a lambda
    function or a simple class which implements __call__ to tokenize/normalize the tokens

    Default implementation uses AlphaTokenizer which uses NonAlphaFilter to remove all non alpha characters.

    Using a custom method:
     > CorpusCounter(iterable, tokenizer=lambda x: x.split())

    Using a method class:
     > from functools import partial
       CorpusCounter(iterable, tokenizer=partial(cls_method, cls_instance))

    Using a tokenizer with filters:
     > CorpusCounter(iterable, tokenizer=AlphaTokenizer(filter=StopWordFilter(stopwords, CustomFilter())))

       Here it uses an AlphaTokenizer with a StopWordFilter chained with another custom filter

    """
    def __init__(self, iterable=[], tokenizer=None):
        self.default_factory = lambda: {'count': 0, 'docs': 0}
        self._tokenizer = tokenizer or AlphaTokenizer()
        super(CorpusCounter, self).__init__(iterable)

    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)

        self[key] = new_value = self.default_factory()
        return new_value

    def __add__(self, other):
        if not isinstance(other, CorpusCounter):
            return NotImplemented

        result = CorpusCounter()
        for elem, val in self.items():
            result[elem]['count'] = val['count'] + other[elem]['count']
            result[elem]['docs'] = val['docs'] + other[elem]['docs']

        for elem, val in other.items():
            if not elem in result:
                self._update_elem(result[elem], val['count'], val['docs'])

        return result

    def __sub__(self, other):
        if not isinstance(other, CorpusCounter):
            return NotImplemented

        result = CorpusCounter()
        for elem, val in self.items():
            result[elem]['count'] = val['count'] - other[elem]['count']
            result[elem]['docs'] = val['docs'] - other[elem]['docs']

        for elem, val in other.items():
            if not elem in result:
                self._update_elem(result[elem], val['count'], val['docs'], how='subtract')

        return result

    def __or__(self, other):
        if not isinstance(other, CorpusCounter):
            return NotImplemented

        result = CorpusCounter()
        for elem, val in self.items():
            other_val = other[elem]
            newval = other_val if val['count'] < other_val['count'] else val

            if newval['count'] > 0:
                result[elem] = newval

        for elem, val in other.items():
            if elem not in self and val['count'] > 0:
                result[elem] = val

        return result

    def __and__(self, other):
        if not isinstance(other, CorpusCounter):
            return NotImplemented

        result = CorpusCounter()
        for elem, val in self.items():
            other_val = other[elem]
            newcount = val if other_val['count'] < val['count'] else other_val

            if newcount > 0:
                result[elem] = newcount

        return result

    def _update_elem(self, elem, count=0, docs=0, how='add'):
        if 'add' == how:
            elem['count'] += count
            elem['docs'] += docs
        else:
            elem['count'] -= count
            elem['docs'] -= docs

    def _modify_elems(self, iterable=None, how='add', **kwds):
        if iterable:
            if isinstance(iterable, CorpusCounter):
                for k in iterable:
                    self._update_elem(self[k], iterable[k]['count'], iterable[k]['docs'], how)
            else:
                for doc in iterable:
                    c = Counter(w for w in self._tokenizer(doc))
                    for k, v in iter(c.items()):
                        self._update_elem(self[k], v, 1, how)

        for k, v in iter(kwds.items()):
            if 'count' in v:
                self._update_elem(self[k], v['count'], 0, how)

            if 'docs' in v:
                self._update_elem(self[k], 0, v['docs'], how)

            if 'count' not in v and 'docs' not in v:
                self._update_elem(self[k], 1, 0, how)

    def update(self, iterable=None, **kwds):
        self._modify_elems(iterable, how='add')

    def subtract(self, iterable=None, **kwds):
        self._modify_elems(iterable, how='subtract')

    def elements(self):
        return chain.from_iterable(starmap(repeat, [(k, v['count']) for k, v in self.iteritems()]))

