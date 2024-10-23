# Synthetic Note Generator #
This system is designed to generate synthetic clinical notes without exposing any Protected Health Information (PHI). Below is a brief description of the source files.

## note_generator.py ##
This is main file for generating notes and the `num_notes` variable can be changed to the desired number of notes. This program outputs a JSON file containing an array of dictionaries with the note free text and its discerete values.

## note.py ##
This files contains classes for individiaul note types, initially just a base class and a more specific consult note.

## data_elements.py ##
This files is a series of classes that represent different types of data elements that could be inserted in the notes. These classes set the initial randomized discrete values and contains the logic for producing the appropriate text representations.

## utils.py ##
Some global utility functions and an initial probability map for generating individual data elements.

## constants.py ##
This contains arrays of values that can be sampled when generating some of the data values.
