# -*- coding: utf-8 -*-
from pymongo import MongoClient


class MongoIterator(object):

    def __init__(self, uri, db, collection, skip=0, limit=0):
        self._collection = MongoClient(uri)[db][collection]
        self._skip = skip
        self._limit = limit

    def __iter__(self):
        return self.stream()

    def stream(self, conditions=None, projection=None, skip=None, limit=None):
        proj = {k: 1 for k in projection} if projection else {}

        if proj:
            proj.update({'_id': False})  # skip internal id

        return self._collection.find(conditions, proj or None, skip=skip or self._skip, limit=limit or self._limit)

    def size(self):
        return self._collection.count()

