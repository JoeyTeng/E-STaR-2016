from __future__ import unicode_literals
__author__ = 'luisdhe'
# This program is intended to clean the names in the dictionaries of female and male names. The idea is to avoid words with a double meaning (i.e. nouns but at the same time verbs, adjectives, etc). To do this we use POS tags from two different sources: NLTK and BlobText

import re
import codecs
import argparse
from textblob import TextBlob
from nltk import pos_tag

#Remove unwanted spaces and numbers at the beginning of the dictionary
def fntPreprocessLine(line):
    line = line.strip('\n')
    line = re.sub('\s+', ' ', line)
    line = line.strip()
    line = line.lower()
    return line

# Loads the dictionary
def load_dict(file_in, min_size=0):
    dictionary = []
    for line in file_in.readlines():
        line = fntPreprocessLine(line)
        if len(line) > min_size and not line.startswith('#'):
            dictionary.append(line)
    return dictionary

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('female_names', help='Dictionary of female names')
    parser.add_argument('male_names', help='Dictionary of male names')
    args = parser.parse_args()

    dict_in = codecs.open(args.female_names, 'r', encoding='utf-8')
    dictionary_female_names = load_dict(dict_in, min_size=0)
    dict_in.close()

    dict_in = codecs.open(args.male_names, 'r', encoding='utf-8')
    dictionary_male_names = load_dict(dict_in, min_size=0)
    dict_in.close()

    # Search for repetitions
    for candidate_name in dictionary_female_names:
        if candidate_name in dictionary_male_names:
            print 'REPEATED: ' + candidate_name


    for dictionary in [ dictionary_male_names, dictionary_female_names]:
        for candidate_name in dictionary:
            candidate_name_titled = candidate_name.title()
            print candidate_name + ' ' + candidate_name_titled

            tokens = (re.sub('\W', ' ', candidate_name)).split()
            blob = TextBlob(candidate_name)
            pos_sent = pos_tag(tokens)

            tokens_titled = (re.sub('\W', ' ', candidate_name_titled)).split()
            blob_titled = TextBlob(candidate_name_titled)
            pos_sent_titled = pos_tag(tokens_titled)

            print 'NLTK: ' + str(pos_sent) + ' ' + str(pos_sent_titled)

            bUseBlob = False
            if len(blob.tags) == len(pos_sent):
                print 'BLOB: ' + str(blob.tags)
                bUseBlob = True

            for i, word in enumerate(tokens):
                if bUseBlob is False:
                    if pos_sent[i][1].lower().startswith('n'):
                        bUse = True
                    else:
                        bUse = False
                else:
                    if not pos_sent[i][1].lower().startswith('n') and not blob.tags[i][1].lower().startswith('n'):
                        bUse = False
                    else:
                        bUse = True

            bUseBlob = False
            if len(blob_titled.tags) == len(pos_sent_titled):
                print 'BLOB_TITLED: ' + str(blob_titled.tags)
                bUseBlob = True

            for i, word in enumerate(tokens_titled):
                if bUseBlob is False:
                    if pos_sent_titled[i][1].lower().startswith('n'):
                        bUse = True
                    else:
                        bUse = False
                else:
                    if not pos_sent_titled[i][1].lower().startswith('n') and not blob_titled.tags[i][1].lower().startswith('n'):
                        bUse = False
                    else:
                        bUse = True

                count = 0
                if pos_sent_titled[i][1].lower().startswith('n'):
                    count += 1

                if pos_sent[i][1].lower().startswith('n'):
                    count += 1

                if blob_titled.tags[i][1].lower().startswith('n'):
                    count += 1
                if blob.tags[i][1].lower().startswith('n'):
                    count +=1
                if count >= 4:
                     bUse = True
                else:
                    bUse = False

            if bUse is True:
                print 'ALLOWED: ' + candidate_name
            else:
                print 'REJECTED: ' + candidate_name

