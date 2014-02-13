# The Once And Future Visualizer
# Document Storage Class
# Author: Dylan Nugent

import re
from numpy import mean

from nltk.corpus import PlaintextCorpusReader
from nltk.corpus import stopwords
from nltk.probability import FreqDist

class Document(object):
    """
    A container object for a set of chapters.

    This allows us to keep track of document frequencies when computing them the
    first time so we don't repeat computations for common words. It also handles
    the PlaintextCorpusReader functions for us.
    """

    def __init__(self, chapter_paths):
        """
        Create a new Document.

        chapter_paths - A list of the paths for chapters in the document.
        """
        self.corpus = PlaintextCorpusReader("", chapter_paths)
        self.chapter_lists = self._sanitize_chapters()
        self.chapter_dists = [(FreqDist(chapter), chapter) for chapter in
                self.chapter_lists]
        self.words = {}

    def get_chapters(self):
        return self.chapter_lists

    def average_chapter_frequency(self, word):
        freqs = []
        if word in self.words:
            return self.words[word]
        else:
            for (dist, wordlist) in self.chapter_dists:
                freqs.append(dist[word]/float(len(wordlist)))

            # Store and return the average frequency
            avg_frq = mean(freqs)
            self.words[word] = avg_frq
            return avg_frq

    def _sanitize_chapters(self):
        # Sanitize the wordlists and return them
        lists = [self.corpus.words(file_id) for file_id in
                self.corpus.fileids()]

        new_lists = []

        for word_list in lists:
            # Convert everything to lowercase (e.g. so "the" and "The" match)
            word_list = [word.lower() for word in word_list]
            # Remove any punctuation
            word_list = [re.sub('\p{P}','',word) for word in word_list]
            # Remove stopwords, punctuation, and any empty word
            stops = stopwords.words('english')
            stops.append('')
            stops.append('said')
            word_list = [word for word in word_list if (word not in stops and
                word.isalpha())]

            new_lists.append(word_list)

        return new_lists
