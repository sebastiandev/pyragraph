# -*- coding: utf-8 -*-
from __future__ import unicode_literals


def skip_empty_data(default=None):

    def wrap(method):

        def _wrapped_f(*args):
            if len(args) == 1 or not args[1]:
                return default

            return method(*args)

        return _wrapped_f

    return wrap


def ensure_list_input(method):

    def _wrapper(*args):
        list_data = args[1]

        if type(list_data) not in [list, set]:
            if type(list_data) is str or unicode:
                list_data = list_data.split()
            else:
                raise Exception("Filter input data must be of type list, set or str")

        return method(args[0], list_data)

    return _wrapper


def ensure_str_input(method):

    def _wrapper(*args):
        str_data = args[1]

        if type(str_data) is str or unicode:
            pass

        elif type(str_data) in [list, set]:
            str_data = str_data.split()

        else:
            raise Exception("Filter input data must be of type list, set or str")

        return method(args[0], str_data)

    return _wrapper


class Filter(object):
    """
    Filters data. A filter always return the same data type as the input
    A chain or pipe of filters can be built by passing a filter to the constructor. The output of the current
    filter will be passed to the next one, and so on until there's no next filter.
    """

    def __init__(self, next_filter=None):
        self._next_filter = next_filter or (lambda x: x)

    def __call__(self, *args, **kwargs):
        return self.filter(args[0])

    def filter(self, data):
        return self._next_filter(self._apply_filter(data))

    def _apply_filter(self, data):
        raise NotImplementedError()




