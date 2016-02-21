# -*- coding: utf-8 -*-


class TextCollection(object):

    def __init__(self, iterable_engine, text_field, text_getter=None):
        self._engine = iterable_engine
        self._text_field = text_field
        self._text_getter = text_getter

    def __iter__(self):
        return self.iter_text()

    def iter_docs(self, skip=0, limit=0):
        return self._engine.stream(projection=[self._text_field], skip=skip, limit=limit)

    def iter_text(self, skip=0, limit=0):
        for doc in self._engine.stream(projection=[self._text_field], skip=skip, limit=limit):
            yield self.text_from_doc(doc)

    def text_from_doc(self, doc):
        return self._text_getter(doc) if self._text_getter else doc[self._text_field] if self._text_field in doc else ''

    def size(self):
        return self._engine.size()

