import re
import sys
import nltk
import codecs

class Tokenizer(object):
    def __init__(self, text=None, language=None):
        self.text = text
        self.language = language or 'english'

    def Main(self, text=None, language=None):
        return self.word_tokenize(text or self.text, language or self.language)

    @classmethod
    def tokenize(cls, text):
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

    @classmethod
    def word_tokenize(cls, text, language='english'):
        """
        Return a tokenized copy of *text*,
        using NLTK's recommended word tokenizer
        (currently :class:`.TreebankWordTokenizer`
        along with :class:`.PunktSentenceTokenizer`
        for the specified language).

        :param text: text to split into sentences
        :param language: the model name in the Punkt corpus
        """
        # return [token for sent in nltk.sent_tokenize(text, language)
        #         for token in cls.tokenize(sent)]
        return [' '.join([token for token in cls.tokenize(sent)])
                for sent in nltk.sent_tokenize(text, language)]
        # return [sent for sent in nltk.sent_tokenize(text, language)]


def files(argv):
    if argv[1] == '-i':
        files = [path.replace('\n', '')
                 for path in open(argv[2], 'rb').readlines()]
    else:
        files = argv[1:]

#    for path in files:
#        try:
#            print path
#            main(open(path, 'rb'), open('%s.processed' % path, 'wb'))
#        except AttributeError:
#            print 'processed : ', path
#            subprocess.call(['rm', '%s.processed' % path])
#            continue
#        except Exception as e:
#            print e
#            new_file = '%s.%s' % (path[path.rfind('/', 0, path.rfind('/')) + 1:path.rfind('/')], path[path.rfind('/') + 1:])
#            subprocess.call(['mv', path, '/root/data/exception/%s' % new_file])
#        subprocess.call(['mv', '%s.processed' % path, path])
    return files

if __name__ == "__main__":
    for path in files(sys.argv):
        print path
        text = codecs.open(path, 'rb', encoding='utf-8').readlines()
        file_out = codecs.open('%s.tokenized.txt' % path, 'wb', encoding='utf-8')
        tokenizer = Tokenizer()
        file_out.writelines(['%s\n' % line for sent in text
                            for line in tokenizer.Main(text=sent)])
