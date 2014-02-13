# The Once And Future Visualizer
# Document Storage Class
# Author: Dylan Nugent

from nltk.corpus import PlaintextCorpusReader

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
        self.chapters = chapters
        self.corpus = PlaintextCorpusReader("", chapter_paths)
        self.words = []

    def get_chapters(self):
        return [self.corpus.words(file_id) for file_id in self.corpus.fileids()]

    def compute_idf(self, word):
        pass
