# process.py
# --coding:utf-8--

import os
import re

import bs4


def files(path):
    def record(arg, dirname, fnames):
        for f in fnames:
            if f[-5:] == '.html':
                arg.append(f)

    files = []
    os.path.walk(path, record, files)

    return files


def process(filename, content):
    moviename = filename[:filename.rfind('.')].replace('-', ' ')
    print ("Processing file: %s\n           movie: %s" %(filename, moviename))

    soup = bs4.BeautifulSoup(content.replace('<br>', '\r\n'), 'lxml')
    text = soup.html.body.find_all(class_='scrtext')[0].getText().encode('utf-8').strip() 
    pattern = r'%s\nWriters.*?Genres.*?User Comments.*?Back to IMSDb' %moviename

    return re.sub(pattern, '', text, count=0, flags=re.S)


def main():
    pages = files('.')

    for page in pages:
        open('%s.processed' % page, 'wb').write(
            process(page, open(page, 'rb').read()))

if __name__ == '__main__':
    main()
