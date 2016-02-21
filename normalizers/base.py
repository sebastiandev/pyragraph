# -*- coding: utf-8 -*-


class Normalizer(object):

    """
    Normalizes data. A normalizer always return the same data type as the input
    A chain or pipe of normalizers can be built by passing a normalizer to the constructor. The output of the current
    normalizer will be passed to the next one, and so on until there's no next normalizer.
    """

    def __init__(self, next_normalizer=None):
        self._next_normalizer = next_normalizer or (lambda x: x)

    def __call__(self, *args, **kwargs):
        return self.normalize(args[0])

    def normalize(self, data):
        return self._next_normalizer(self._apply_normalizer(data))

    def _apply_normalizer(self, data):
        raise NotImplementedError()

