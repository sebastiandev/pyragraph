# -*- coding: utf-8 -*-
from .base import Filter, skip_empty_data, ensure_list_input


class StopWordFilter(Filter):
    """
    Filters stop words from the input tokens. Input is expected to be a list
    """
    def __init__(self, stopwords, next_filter=None):
        super(StopWordFilter, self).__init__(next_filter)
        self._stopwords = set(stopwords)  # sets lookup works as a dict and makes search time O(1)

    @skip_empty_data(default=[])
    @ensure_list_input
    def _apply_filter(self, tokens):
        return [t for t in tokens if t not in self._stopwords]

