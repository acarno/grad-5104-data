#!/usr/bin/env python3

import collections
import string

def read_and_sanitize(file_, ignore):

    with open(file_, "r") as fp:
        raw = fp.read().split()

    raw_length = len(raw)

    # Remove punctuation, possession
    raw = [_.strip(string.punctuation).lower() for _ in raw]
    words = []
    for word in raw:
        if word.endswith("'s"):
            w = word[:-2]
        else:
            w = word

        words += [w]

    # Remove useless words
    words = [w for w in words if w not in ignore]

    return raw_length, words

def analyse(su_words, bu_words):

    # Words in common
    common = []
    for word in su_words:
        if word in bu_words and word not in common:
            common += [word]

    print("Common words:")
    for word in common:
        print("\t" + word)

    # Most common words
    su_count = collections.Counter(su_words)
    bu_count = collections.Counter(bu_words)

    print("Most common words:")
    print("\tBucknell:")
    for word, count in bu_count.most_common():
        if count > 1:
            print("\t\t" + word + " (" + str(count) + ")")
    print("\tSyracuse:")
    for word, count in su_count.most_common():
        if count > 1:
            print("\t\t" + word + " (" + str(count) + ")")

    # Unique words
    su_unique, bu_unique = [], []
    for word in su_words:
        if word not in bu_words and word not in su_unique:
            su_unique += [word]
    for word in bu_words:
        if word not in su_words and word not in bu_unique:
            bu_unique += [word]
    #print("BU unique:", bu_unique)
    #print("SU unique:", su_unique)

if __name__ == "__main__":

    # Ignore corpus -- top 100 words in English language
    CORPUS_FILE = "./google-10000-english/google-10000-english-usa-no-swears.txt"
    with open(CORPUS_FILE, "r") as _fp:
        CORPUS_IGNORE = set([word.strip() for word in _fp][0:100])

    su_len, su_words = read_and_sanitize("syracuse.txt", CORPUS_IGNORE)
    bu_len, bu_words = read_and_sanitize("bucknell.txt", CORPUS_IGNORE)

    print("BU length: " + str(bu_len))
    print("SU length: " + str(su_len))

    analyse(su_words, bu_words)

