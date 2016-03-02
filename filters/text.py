# -*- coding: utf-8 -*-
from .base import Filter, skip_empty_data
import unicodedata as ud
import six


class NonAlphaFilter(Filter):
    """
    Filters all non alpha characters, input is assumed to be unicode.
    By default digits are skipped but can be kept if specified by parameter,
    also punctuation characters are removed but a replacement can be defined.
    """

    def __init__(self, next_filter=None, keep_spaces=True, keep_digits=False, punct_replacement=None):
        super(NonAlphaFilter, self).__init__(next_filter)

        valid_categories = {'Lu', 'Ll'}

        if keep_spaces:
            valid_categories.add('Zs')

        if keep_digits:
            valid_categories.add('Nd')

        self._all = ''.join(six.unichr(i) for i in range(65536))
        self._letters = set(''.join(c for c in self._all if ud.category(c) in valid_categories))
        self._not_letters = ''.join(c for c in self._all if ud.category(c) not in valid_categories)
        self._not_letters_map = dict.fromkeys(map(ord, self._not_letters))

        if punct_replacement:
            for k in self._not_letters:
                if ud.category(k) is 'Po':
                    self._not_letters_map[ord(k)] = punct_replacement

    @skip_empty_data(default='')
    def _apply_filter(self, text):
        return text.translate(self._not_letters_map)

