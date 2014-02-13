# The Once And Future Visualizer
# Chapter Data Parser
# Author: Dylan Nugent

import re

from nltk.corpus import stopwords
from nltk.probability import FreqDist

from document import Document

import sys
import argparse

def generate_document_data(chapter_paths, word_count):
    """
    Generate visualization data for a set of chapters.

    Given input chapters we want to find both the unique words being used inside
    of each chapter and how frequent they are within the text as a whole.

    chapter_paths - A list of paths to chapters
    word_count - The number of most frequent words to grab for each chapter

    Returns a list looking like this:
    [
        [
            {
                "word": wart
                "freq": .7
                "uniqueness": .5
                "pos": .1
            }
        ],
    ]

    This is a list of chapters, where each chapter is a list of word
    dictionaries and each word dictionary has the word itself, the frequency of
    the word in that chapter, the uniqueness of the word overall, and the first
    position the word is observed. All of the latter three values are scaled
    from 0-1 with respect to the chapter (the most frequent word receives a 1,
    for instance).
    """
    document = Document(chapter_paths)
    return [generate_chapter_data(word_list, word_count) for word_list in
            document.get_chapters()]

def generate_chapter_data(word_list, word_count):
    """
    Given a specific chapter, return the word/freq/uniqueness/pos data.

    word_list - A raw wordlist for a chapter
    word_count - The number of words to return

    Returns the chapter component of the JSON document described in
    generate_document_data.
    """
    # Step 1: Find the top word_count words.
    top_words = get_top_words(word_list, word_count)

    # Step 2: Find the uniqueness of each word

    # Step 3: Scale the freq, pos, and uniqueness values to the chapter.
    # Since the visualizer will treat 0 as nothing, let's use .1 as a minimum
    top_words = scale_raw_values(top_words, 'pos', .1, 1)
    top_words = scale_raw_values(top_words, 'freq', .1, 1)

    return top_words

def get_top_words(word_list, word_count):
    """
    Get the top words used in a chapter.

    word_list - The raw word list to get top words from
    word_count - The number of words to return

    Returns a list of most frequent words, their frequencies, and the first time
    they were seen.
    """
    # Step 1: Sanitize the word list
    # Convert everything to lowercase (e.g. so "the" and "The" match)
    word_list = [word.lower() for word in word_list]
    # Remove any punctuation
    word_list = [re.sub('\p{P}','',word) for word in word_list]
    # Remove stopwords, punctuation, and any empty word
    stops = stopwords.words('english')
    stops.append('')
    word_list = [word for word in word_list if (word not in stops and
        word.isalpha())]

    # Step 2: Find and return most frequent words
    dist = FreqDist(word_list)
    # We want the word, freq, and pos to be set here. Frequency and position
    # will be scaled relative to each other later, and uniqueness will be
    # calculated later.
    table = [dict(word=w, freq=dist[w], pos=word_list.index(w)) for w in dist]

    return table[:word_count]

def scale_raw_values(value_set, key_name, scale_min, scale_max):
    """
    Scale raw values to be within a range from min_val to max_val.

    value_set - List of dictionary of values to be scaled.
    key_name - The name of the key in each dictionary with the value.
    scale_min - The low end of the scaling range.
    scale_max - The high end of the scaling range.

    Returns the value_set modified with the scaled values.
    """
    # Step 1: Compute the range being scaled from
    values = [item[key_name] for item in value_set]
    act_min = min(values)
    act_max = max(values)
    act_range = act_max - act_min
    scale_range = scale_max - scale_min

    # Step 2: Update values to the scaled range
    for item in value_set:
        value = item[key_name]
        prescale = (value - act_min)/float(act_range)
        scaled = (prescale * scale_range) + (scale_min)
        item[key_name] = scaled

    return value_set

def write_json_outfile(data, path):
    """
    """
    pass

if __name__ == '__main__':
    # Script is being run standalone, use the argument parser
    pass
