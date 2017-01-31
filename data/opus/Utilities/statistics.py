import sys
import nltk
import codecs
import textblob

class Statistics(object):

    def __init__(self):
        pass

    def Speaker(self, number):
        if number % 2 == 1:
            self.file['output'].write('A | - | ')
        else:
            self.file['output'].write('B | - | ')

    def Sentence(self, sentence):
        self.file['output'].write(sentence)
        self.file['output'].write(' | ')

    def Polarity_Subjectivity(self, sentence):
        sTB = textblob.TextBlob(sentence)
        self.file['output'].write(str(sTB.sentiment.polarity))
        self.file['output'].write(' | ')
        self.file['output'].write(str(sTB.sentiment.subjectivity))
        self.file['output'].write(' | ')

    def DetectSwearWords(self, sentence):
        for row in self.file['swear1']:
           if row in sentence:
                self.file['output'].write('1\n')
                return
        for row in self.file['swear2']:
            if row in sentence:
                self.file['output'].write('1\n')
                return
        self.file['output'].write('0\n')

    def Dialogue(self):
        sentence = 0
        yield # To print DIALOGUE 1
        for i, row in enumerate(self.file['input']):      #long sentence change line --> still consider as one line?
            if len(row) != 0:
                sentence += 1
                self.Speaker(sentence)
                self.Sentence(row)
                self.Polarity_Subjectivity(row.decode('utf-8'))
                self.DetectSwearWords(row)
            else:
                yield sentence
                sentence = 0

    @staticmethod
    def open_files(paths):
        file = {
        'input' : [line.strip() for line in open(paths['input'],'r')],
        'output' : open('%s.tokenized.txt' % path, 'wb'),
        'f_name' : [line.strip() for line in open('english_female_names.txt','r')],
        'm_name' : [line.strip() for line in open('english_male_names.txt','r')],
        'swear1' : [line.strip() for line in open('swear_words_multi.uniq','r')],
        'swear2' : [line.strip() for line in open('swear_words_single.uniq','r')]
        }
        return file

    def Main(self):
        length = len(self.file['input'])
        for count, num in enumerate(self.Dialogue()):
            self.file['output'].write('DIALOGUE ')
            self.file['output'].write(str(count + 1))
            self.file['output'].write('\n')

def files(argv):
    if argv[1] == '-i':
        files = [path.replace('\n', '')
                 for path in open(argv[2], 'rb').readlines()]
    else:
        files = argv[1:]
    return files

if __name__ == "__main__":
    for path in files(sys.argv):
        print path
        paths = {
                'input': path,
                'output': ('%s.statistics.txt' % path)
        }
        statistics = Statistics()
        statistics.file = statistics.open_files(paths)
        statistics.Main()
