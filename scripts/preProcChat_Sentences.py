# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import glob
import codecs
import re
import argparse
import sys
import os
import nltk
import string
from textblob import TextBlob

__author__ = 'luisdhe'

dictReplacements = {
    "i'm" : "i am",
    "don't" : "do not",
    "it's" : "it is",
    "you're" : "you are",
    "that's" : 'that is',
    "he's" : 'he is',
    # "i'll" : "i will",
    "can't" : 'can not',
    "didn't" : "did not",
    "gonna" : "going to",
    # "we're" : "we are",  # ToDo: take into account the context
    "i've" : "i have",
    "what's" : "what is",
    "there's" : 'there is',
    "she's" : "she is",
    "let's" : 'let us',
    # "they're" : 'they are',  # ToDo: take into account the context
    # "i'd" : "i would",  # ToDo: take into account the context
    "you've" : 'you have',
    "won't" : 'will not',
    "doesn't" : "does not",
    "isn't" : 'is not',
    "we'll" : 'we will',
    "you'll" : 'you will',
    "i ain't" : 'i am not',
    "ain't" : "is not",
    "wouldn't" : 'would not',
    "wasn't" : 'was not',
    "we've" : 'we have',
    "'em " : 'them ',
    "you'd" : 'you would',
    "haven't" : 'have not',
    "couldn"'t' : 'could not',
    "who's" : 'who is',
    "aren't" : 'are not',
    "where's" : 'where is',
    "he'll" : 'he will',
    "they'll" : 'they will',
    "'cause" : 'because',
    "it'll" : 'it will',
    "how's" : 'how is',
    "c'mon" : "come on",
    "here's" : 'here is',
    "shouldn't" : 'should not',
    # "he'd" : 'he had',  # ToDo: Take into account the context
    # "she'd" : 'she had',  # ToDo: Take into account the context
    # "we'd" : 'we had',  # ToDo: Take into account the context
    "weren't" : 'were not',
    "they've" : 'they have',
    "goin'" : 'going',
    "doin'" : 'doing',
    "nothin'" : 'nothing',
    " 'ave " : ' have ',
    "ma'am" : 'madam',
    "an'" : 'and',
    "she'll" : 'she will',
    "hasn't" : 'has not',
    # "how'd" : 'how would',  # ToDo: Take into account the context
    # "what'd" : 'what would',  # ToDo: Take into account the context
    "y'know" : 'you know',
    "'bout" : 'about',
    # "they'd" : 'they would', # ToDo: Take into account the context
    "what're" : 'what are',
    "somethin'" : 'something',
    "hadn't" : "had not",
    "talkin'" : 'talking',
    "gettin'" : 'getting',
    # "where'd" : 'where would',  # ToDo: Take into account the context
    "that'll" : 'that will',
    "would've" : "would have",
    "lookin'" : 'looing',
    "comin'" : 'comming',
    "could've" : 'could have',
    # "why'd" : 'why did',  # ToDo: Take into account the context
    # "it'd" : 'it had',  # ToDo: Take into account the context
    "must've" : 'must have',
    "'til" : 'until',
    "y'all" : 'you all',
    "should've" : 'should have',
    "d'you" : 'did you',
    # "who'd" : 'who had',  # ToDo: Take into account the context
    "tryin'" : 'trying',
    "thinkin'" : 'thinking',
    # "that'd" : 'that had', # ToDo: Take into account the context
    "tellin'" : 'telling',
    "sayin'" : 'saying',
    "there'll" : 'there will',
    "workin'" : 'working',
    "why's" : "why is",
    "jus'" : 'just',
    "makin'" : 'making',
    "takin'" : 'taking',
    "bein'" : 'being',
    "how're" : 'how are',
    "ya'" : 'you all',
    "mornin'" : 'morning',
    "when's" : 'when is',
    "what'll" : 'what will',
    "this'll" : 'this will',
    "mustn't" : 'must not',
    "havin'" : 'having',
    "darlin'" : 'darling',
    "runnin'" : 'running',
    "waitin'" : 'waiting',
    "'course" : 'of course',
    "playin'" : 'playing',
    "callin'" : 'calling',
    "askin'" : 'asking',
    "who'll" : 'who will',
    "'bye" : 'goodbye',
    "kiddin'" : 'kidding',
    "'kay" : "okay",
    "there'd": "there had",
    "givin'": "giving",
    "'round": 'around',
    "might've": 'might have',
    "feelin'": 'feeling',
    "wanna": "want to",
}

replacement_patterns = [
# (r'won\'t', 'will not'),
(r'can\'t', 'cannot'),
(r'i\'m', 'i am'),
(r'ain\'t', 'is not'),
# (r'(\w+)\'ll', '\g<1> will'),
(r'(\w+)n\'t', '\g<1> not'),
(r'(\w+)\'ve', '\g<1> have'),
# (r'(\w+)\'s', '\g<1> is'),
(r'(\w+)\'re', '\g<1> are'),
(r'(\w+)\'d', '\g<1> would'),
(r'(\w+)in\'', '\g<1>ing'),
]
patterns = [(re.compile(regex), repl) for (regex, repl) in replacement_patterns]

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
        if line.startswith("#"):
            next
        line = fntPreprocessLine(line)
        if len(line) > min_size:
            dictionary.append(line)
    return dictionary


def tokenize(text):
    #starting quotes
    text = re.sub(r'^\"', r'``', text)
    text = re.sub(r'(``)', r' \1 ', text)
    text = re.sub(r'([ (\[{<])"', r'\1 `` ', text)

    #punctuation
    text = re.sub(r'([:,])([^\d])', r' \1 \2', text)
    text = re.sub(r'\.\.\.', r' ... ', text)
    text = re.sub(r'[;@#$%&]', r' \g<0> ', text)
    text = re.sub(r'([^\.])(\.)([\]\)}>"\']*)\s*$', r'\1 \2\3 ', text)
    text = re.sub(r'[?!]', r' \g<0> ', text)

    text = re.sub(r"([^'])' ", r"\1 ' ", text)

    #parens, brackets, etc.
    text = re.sub(r'[\]\[\(\)\{\}\<\>]', r' \g<0> ', text)
    text = re.sub(r'--', r' -- ', text)

    #add extra space to make things easier
    text = " " + text + " "

    #ending quotes
    text = re.sub(r'"', " '' ", text)
    text = re.sub(r'(\S)(\'\')', r'\1 \2 ', text)

    #text = re.sub(r"([^' ])('[sS]|'[mM]|'[dD]|') ", r"\1 \2 ", text)
    text = re.sub(r"([^' ])('ll|'LL|'re|'RE|'ve|'VE|n't|N'T) ", r"\1 \2 ",
                  text)

    return text.split()


def word_tokenize(text, language='english'):
    """
    Return a tokenized copy of *text*,
    using NLTK's recommended word tokenizer
    (currently :class:`.TreebankWordTokenizer`
    along with :class:`.PunktSentenceTokenizer`
    for the specified language).

    :param text: text to split into sentences
    :param language: the model name in the Punkt corpus
    """
    return [token for sent in nltk.sent_tokenize(text, language)
            for token in tokenize(sent)]


def processLine(line_orig):
    aSentences = []
    if line_orig.startswith("DIALOGUE"):
        aSentences.append("\n" + line_orig + "\n")
        return aSentences
    else:
        if len(line_orig) > 0:
            aLine = line_orig.split('|')
            if len(aLine) == 3:
                (name, dummy, line) = aLine
                name = re.sub('[%s]' % re.escape(string.punctuation), '', name)
                name = re.sub('[%s]' % re.escape(string.digits), '', name).strip()
            else:
                print("ERROR: " + line_orig)
                return aSentences

            blob = TextBlob(line)
            for sent in blob.sentences:
                line = sent.raw
                bNoSwear = 1
                line = re.sub(r'(\w+)[\.]{3,}(\w+|$)', '\g<1> ... \g<2>', line.strip())  # Separate ... in the middle of a word
                line = re.sub(r'^(\w+)[\.]{3,}$', '\g<1> ... ', line)  # Separate ... at the end of a word
                line = re.sub(r'^[\.]{3,}(\w+)$', '... \g<1>', line)  # Separate ... at the end of a word
                line = re.sub(r'(\w+)[\.]\s+([A-Z]+)(\w*)', '\g<1> . \g<2>\g<3>', line)  # Separate the dot if it is only one and next word starts with capital letter

                line = line.lower()
                line = re.sub('(.+)\s+(\w+)(\.|\"|\')$', '\g<1> \g<2> \g<3>', line)  # Separate the dot at the end of a sentence
                for word in dictReplacements:
                    line = re.sub(word, dictReplacements[word], line)

                for (pattern, repl) in patterns:
                    (line, count) = re.subn(pattern, repl, line)

                #tokens = nltk.word_tokenize(line.strip())
                tokens = word_tokenize(line.strip())
                new_tokens = []
                for token in tokens:
                    if len(token) == 1:
                        token = re.sub(r'[^\?\,\!\.:a-zA-Z0-9]', '', token)  # Remove almost all one-letter words

                    token = re.sub(r'(\w+)(\,|\!|\:|\?|\"+)', '\g<1> \g<2>', token)  # Separate punctuation
                    token = re.sub(r'(\,|\!|\:|\?|\"+)(\w+)', '\g<1> \g<2>', token)  # Separate punctuation
                    token = re.sub(r'^(.+\w)[\-\']+$', '\g<1>', token)  # Remove -, ' at the end of words
                    token = re.sub(r'^[\-\']{1,}(\w+)$', '\g<1>', token)  # Remove -, ' at the beginning of words
                    token = re.sub(r'^[\-]{1,}$', '', token)  # Remove - at the beginning of words
                    token = re.sub(r'^(.+\w)[\-]{2,}(.+\w)$', '\g<1> \g<2>', token)  # Remove - in the middle of a word, only if there are several of them

                    token = re.sub(r'([a-z])\1{2,}', r'\1', token)  # Remove repeated characters more than 2 times
                    if len(token) > 0:
                        if token in dictSpellings:
                            sys.stderr.write("Found " + token + " replaced for " + dictSpellings[token] + '\n')
                            token = re.sub(token, dictSpellings[token], token)
                        if token in dictionary_swearwords_single:
                            bNoSwear = 0
                            token = '<swear> ' + token + ' </swear>'
                        new_tokens.append(token)

                new_sent = ' '.join(new_tokens)
                for multi_sw in dictionary_swearwords_multi:
                    count = line.count(multi_sw)
                    if count > 0:
                        bNoSwear = 0
                        new_sent = re.sub(r'\b' + multi_sw + r'\b', ' <swear> ' + multi_sw + ' </swear> ', new_sent, flags=re.I)

                sTB = TextBlob(new_sent)

                if len(name) > 0:
                    new_sent = re.sub(name, '<name-self>', new_sent, flags=re.I)
                for candidate_name in dictionary_female_names:
                    if candidate_name in new_sent:
                        new_sent = re.sub(r'\b' + candidate_name + r'\b', ' <f-name-other> ', new_sent, flags=re.I)

                for candidate_name in dictionary_male_names:
                    if candidate_name in new_sent:
                        new_sent = re.sub(r'\b' + candidate_name + r'\b', ' <m-name-other> ', new_sent, flags=re.I)

                aSentences.append("%s | %s | %s | %f | %f | %d\n" % (name, dummy, new_sent, sTB.sentiment.polarity, sTB.sentiment.subjectivity, bNoSwear))
            return aSentences

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('misspelling', help='Wikipedia misspelling file')
    parser.add_argument('dictionary_single', help='Dictionary of swear words. One word per line')
    parser.add_argument('dictionary_multi', help='Dictionary of swear words. Several words per line')
    parser.add_argument('female_names', help='Dictionary of female names')
    parser.add_argument('male_names', help='Dictionary of male names')
    args = parser.parse_args()

    if not os.path.exists(args.misspelling):
        raise "The Wikipedia misspelling file does not exists"

    if not os.path.exists(args.dictionary_single):
        raise "The dictionary of single swear words does not exists"

    if not os.path.exists(args.dictionary_multi):
        raise "The dictionary of multi-word swear words does not exists"

    dict_in = codecs.open(args.dictionary_single, 'r', encoding='utf-8')
    dictionary_swearwords_single = load_dict(dict_in)
    dict_in.close()

    dict_in = codecs.open(args.dictionary_multi, 'r', encoding='utf-8')
    dictionary_swearwords_multi = load_dict(dict_in)
    dict_in.close()

    dict_in = codecs.open(args.female_names, 'r', encoding='utf-8')
    dictionary_female_names = load_dict(dict_in, min_size=3)
    dict_in.close()

    dict_in = codecs.open(args.male_names, 'r', encoding='utf-8')
    dictionary_male_names = load_dict(dict_in, min_size=3)
    dict_in.close()

    # To correct common misspellings using the dictionary of common misspellings of Wikipedia
    dictSpellings = {}
    with codecs.open(args.misspelling, 'r', 'utf-8') as fin:
        for line in fin.readlines():
            aWords = line.split("->")
            word = aWords[0]
            aOptions = aWords[1].split(",")
            dictSpellings[word] = aOptions[0].strip()  # Take the first option always

    num_movies = 0
    line_new = processLine("DWAYNE | - | Hey, don't just take this scientist's word for it. The proof...")


    for file in sorted(glob.glob("./txt_files/*.txt")):
        print "Processing file " + file
        with codecs.open(file, 'r', 'utf-8') as h_file_in, codecs.open(file.replace('.txt', '.proc3'), 'w', 'utf-8') as h_file_out:
            for line_orig in h_file_in.readlines():
                line_orig = line_orig.strip()
                if len(line_orig) > 0:
                    aSentences = processLine(line_orig)
                    for line_new in aSentences:
                        if len(line_new) > 0:
                            h_file_out.write(line_new)
