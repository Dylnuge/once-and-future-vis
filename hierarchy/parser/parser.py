# The Once And Future Visualizer, Part 2
# Data Parser
# Author: Dylan Nugent

import json
import re

import nltk

from nltk.corpus import PlaintextCorpusReader
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.probability import FreqDist

import argparse
import sys

DEFAULT_OUT = "data/out.json"
WORD_COUNT = 200

def generate_document_data(file_path, word_count):
    """
    Generate part-of-speech visualization data.

    file_path - The file to generate data for.
    word_count - The number of words to include in output.

    Finds the most frequent words in the text located at file_path and
    categorizes them based on parts of speech and synonyms.

    Return format example:
    [
        {
            'word': 'award'
            'freq': 256
            'part': 'N'
            'syn_id': 'prize'
        },
    ]
    """
    ### Step 1: Process the source file into memory ###
    corpus = PlaintextCorpusReader("", file_path)
    words = corpus.words(file_path)
    word_list = sanitize_input(words)

    ### Step 2: Tag parts of speech ###
    # As stripped data (like capitals and punctuation) might be used by the part
    # of speech tagger, sanitizing the word list may cause some tags to be
    # incorrect. In sample tests this seemed to present less of an issue than
    # expected.
    pos_tags = nltk.pos_tag(word_list)

    ### Step 3: Find most frequent words, regardless of part of speech ###
    # TODO(dylnuge): This is an ugly hack. I believe it could be circumvented by
    # properly using wordnet synsets but clearly I don't understand them well
    # enough.
    dist = FreqDist(words)
    pos_dist = FreqDist(pos_tags)
    most_freq = [elem for elem in pos_dist][:word_count]
    most_freq_words = [elem[0] for elem in most_freq]

    ### Step 4: Put most frequent words and synonyms into dataset ###
    word_data = []
    word_ids = []
    repeats = set()

    for (word, pos) in most_freq:
        simple_tag = simplify_wsj_tag(pos)
        if simple_tag not in ['N', 'V', 'ADJ', 'ADV']:
            # Ignore this element, it's not one of our target parts of speech
            continue
        elif word not in repeats:
            # First append this word to the data set
            word_data.append({'word': word, 'freq': dist[word], 'syn_id': word,
                'part': simple_tag})
            word_ids.append(word)
            # Now append synonyms data using this word as ID
            synonyms = []
            # TODO(dylnuge) there is likely a cleaner way to do this
            for sysnset in wordnet.synsets(word):
                for lemma in synset.lemmas:
                    if lemma.name is not word and lemma.name not in synonyms:
                        synonyms.append(lemma.name)
            for synonym in synonyms:
                if synonym in most_freq_words:
                    # This word is also one of the most frequent grabbed. Skip
                    # it when we reach it.
                    repeats.add(synonym)
                if synonym in dist:
                    word_data.append({'word':synonym, 'freq': dist[synonym],
                        'syn_id': word, 'part': simple_tag})


    ### Step 5: Combine results and return them ###
    return word_data

def sanitize_input(word_list):
    """
    Convert words to lowercase and remove words we aren't interested in.

    word_list - The corpus to work with.

    Returns the sanitized word list.
    """
    # Remove stopwords, punctuation, and any empty word
    stops = stopwords.words('english')
    stops.append('')
    stops.append('said')

    word_list = [sanitize_word(word, stops) for word in word_list]
    # TODO(dylnuge): This line feels silly, I can do this better
    word_list = [word for word in word_list if word is not None]

    return word_list

def sanitize_word(word, stops):
    # Convert everything to lowercase (e.g. so "the" and "The" match)
    word = word.lower()
    # Remove any punctuation
    re.sub('\p{P}','',word)
    # Remove stopwords, punctuation, and any empty word
    if word in stops or not word.isalpha():
        return None

    return word

def write_json_outfile(data, path):
    """
    Write the data given to a JSON file.

    data - The data to write out
    path - The path to write to
    """
    with open(path,'w') as outfile:
        json.dump(data, outfile, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    # Script is being run standalone, use the argument parser
    parser = argparse.ArgumentParser(description="The Once and Future \
        Visualizer")
    parser.add_argument('data_file', help="Text file to use for \
        parsing data")
    parser.add_argument('--outfile', dest="outfile", default=DEFAULT_OUT,
        help="Output destination (optional)")

    args = parser.parse_args()
    data_file = args.data_file
    outfile = args.outfile

    data = generate_document_data(data_file, WORD_COUNT)
    write_json_outfile(data, outfile)
    sys.exit(0)
