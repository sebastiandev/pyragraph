#!/usr/bin/python
# -*- coding: utf-8 -*-


# A good heuristic for identifying such words is to:
#  - remove those that occur in more than 5-10% of documents (most common)
#  - remove those that occur fewer than 5-10 times in the entire corpus (least common)
# word_freq = word_freq_and_doc_count(docs)
# vocabulary = filter(lambda word: word_freq[word]['count'] > 10 and word_freq[word]['docs'] <= corpus_len/10, word_freq.keys())
