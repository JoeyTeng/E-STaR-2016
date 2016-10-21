from __future__ import unicode_literals
__author__ = 'luisdhe'
# This script is intended to find male and female names in the texts of the movie scripts
# The script receives a file containing all the pre-processed sentences in a single text file (one sentence per line)
# And the male and female name dictionaries. Then, it saves statistics about which names are more common in both categories
# At the end, a sorted list by frequency of names is displayed + contextual information to make easy to detect errors
# in the process of detecting names.

import argparse
import re
import codecs
from nltk.text import Text

#Remove unwanted spaces and numbers at the beginning of the dictionary
def fntPreprocessLine(line):
    line = line.strip('\n')
    line = re.sub('\s+', ' ', line)
    line = line.strip()
    line = line.lower()
    return line

# Loads the dictionary
def load_dict(file_in):
    dictionary = []
    for line in file_in.readlines():
        line = fntPreprocessLine(line)
        dictionary.append(line)
    return dictionary

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('dialogues', help='Text dialogues file. One sentence is a dialogue.')
    parser.add_argument('dictionary_male', help='Dictionary of male names.')
    parser.add_argument('dictionary_female', help='Dictionary of female names.')

    args = parser.parse_args()
    dict_in = codecs.open(args.dictionary_single, 'r', encoding='utf-8')
    dictionary_male_names = load_dict(dict_in)
    dict_in.close()

    dict_in = codecs.open(args.dictionary_multi, 'r', encoding='utf-8')
    dictionary_female_names = load_dict(dict_in)
    dict_in.close()

    dict_counts_male_names = {}
    dict_counts_female_names = {}
    all_tokens = []
    with codecs.open(args.dialogues, 'r', encoding='utf-8') as dialogues:
        max_num_names = 0
        for (num_dial, dialog_turn) in enumerate(dialogues.readlines()):

            if (num_dial % 1000) == 0:
                print('Processing ' + str(num_dial))

            line = fntPreprocessLine(dialog_turn)
            tokens = line.split()
            names_per_line = []
            all_tokens += tokens
            num_names = 0
            for tok in tokens:
                if tok in dictionary_male_names:
                    names_per_line.append(tok)
                    try:
                        dict_counts_male_names[tok] += 1
                    except:
                        dict_counts_male_names[tok] = 1
                    num_names += 1

            for tok in tokens:
                if tok in dictionary_female_names:
                    names_per_line.append(tok)
                    try:
                        dict_counts_female_names[tok] += 1
                    except:
                        dict_counts_female_names[tok] = 1
                    num_names += 1

            if num_names > max_num_names:
                max_num_names = num_names
                print('NEW_RECORD: ' + str(max_num_names) + ' SENT: ' + dialog_turn + ' LINE: ' + str(num_dial))
                print(', '.join(names_per_line))

    # Show statistics
    text = Text(all_tokens)

    for key in sorted(dict_counts_male_names, key=dict_counts_male_names.get, reverse=True):
        print('KEY: ' + key + ' VAL: ' + str(dict_counts_male_names[key]))
        print(text.concordance(key))

    for key in sorted(dict_counts_female_names, key=dict_counts_female_names.get, reverse=True):
        print('KEY: ' + key + ' VAL: ' + str(dict_counts_female_names[key]))
        print(text.concordance(key))




if __name__ == '__main__':
    main()
