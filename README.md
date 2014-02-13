#The Once and Future Visualization
Project by Dylan Nugent &lt;dylnuge@gmail.com&gt;  
University of Illinois at Urbana-Champaign

## Description

A visualization of chapters from "The Once and Future King," by T. H. White.
This repository contains both the code for generating the visualization input
given the text files for the document and the code for the visualization itself.
For copyright reasons, the input text is not included here.

## Instructions

### Parser

The parser is a Python 2.x program using the NLTK library for text processing.
To set up an environment for it and run it on input files (assuming you are
starting in the `parser` directory):

1. Run `virtualenv env` to create a new virtual environment. If you have Python
   3 as your default virtualenv target, modify this command to make a python2
   virtual environment.
2. Run `source env\bin\activate` to activate the environment.
3. Run `pip install -r requirements.txt` to install NLTK.
4. Run `python parser.py` with the list of chapters as your arguments, seperated
   by spaces. For instance, to run on four chapters of The Once and Future King
   named `ofk1.txt` through `ofk4.txt` run `python parser.py ofk{1,2,3,4}.txt`.

### Visualizer

The visualizer is entirely static HTML and JavaScript code that expects a file
called "vis\_in.json" to be present in the data directory. To run it, simply
open `index.html` in a browser that supports D3 (should be pretty much all of
them).

## Collaborators

Created by Dylan Nugent at the University of Illinois at Urbana-Champaign for CS
398VL (Visualizing Literature) in the Spring 2014 semester.

## Licence/Legal

Copyright 2014 Dylan Nugent. All Rights Reserved.

I intend in the future to release this under an open source license.
