# -*- coding: utf-8 -*-


class TextCollection(object):
    """
    An interface to iterate text collections. It makes it easy to iterate a collection (handled by an interable engine)
    by defining a text_field the engine will be asked to project the results to, and it will
    yield that text field only or it can receive a custom method as a text_getter that will be passed the yielded doc
    as parameter to return the desired data/field.

    The expected iterable_engine should implement 'stream' and 'size' methods
    """
    def __init__(self, iterable_engine, text_field, text_getter=None):
        self._engine = iterable_engine
        self._text_field = text_field
        self._text_getter = text_getter

    def __iter__(self):
        return self.iter_text()

    def iter_docs(self, skip=0, limit=0):
        return self._engine.stream(skip=skip, limit=limit)

    def iter_text(self, skip=0, limit=0):
        for doc in self._engine.stream(projection=[self._text_field], skip=skip, limit=limit):
            yield self.text_from_doc(doc)

    def text_from_doc(self, doc):
        return self._text_getter(doc) if self._text_getter else doc[self._text_field] if self._text_field in doc else ''

    def size(self):
        return self._engine.size()

