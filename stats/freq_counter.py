#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import Counter
from tokenization import Tokenizer, TokenNormalizer
from itertools import chain, starmap, repeat

# CorpusCounter(source,
#               tokenizer=partial(some_method, instance),
#               token_normalizer=partial(some_method, instance)

# CorpusCounter(source, tokenizer=tokenizer, token_normalizer=normalizer


class CorpusCounter(Counter):

    def __init__(self, iterable, tokenizer=None, token_normalizer=None):
        self.default_factory = lambda: {'count': 0, 'docs': 0}
        self._tokenizer = tokenizer or Tokenizer()
        self._normalizer = token_normalizer or TokenNormalizer()
        super(CorpusCounter, self).__init__(iterable)

    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)

        self[key] = new_value = self.default_factory()
        return new_value

    def __add__(self, other):
        if not isinstance(other, Counter):
            return NotImplemented

        result = Counter()
        for elem, val in self.items():
            result[elem]['count'] = other[elem]['count']
            result[elem]['docs'] = other[elem]['docs']

        for elem, val in other.items():
            self._update_elem(result[elem], val['count'], val['docs'])

        return result

    def __sub__(self, other):
        if not isinstance(other, Counter):
            return NotImplemented

        result = Counter()
        for elem, count in self.items():
            newcount = count - other[elem]
            if newcount > 0:
                result[elem] = newcount
        for elem, count in other.items():
            if elem not in self and count < 0:
                result[elem] = 0 - count
        return result

    def __or__(self, other):
        if not isinstance(other, Counter):
            return NotImplemented
        result = Counter()
        for elem, count in self.items():
            other_count = other[elem]
            newcount = other_count if count < other_count else count
            if newcount > 0:
                result[elem] = newcount
        for elem, count in other.items():
            if elem not in self and count > 0:
                result[elem] = count
        return result

    def __and__(self, other):
        if not isinstance(other, Counter):
            return NotImplemented
        result = Counter()
        for elem, count in self.items():
            other_count = other[elem]
            newcount = count if count < other_count else other_count
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
                    c = Counter(self._normalizer(w) for w in self._tokenizer(doc))
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

