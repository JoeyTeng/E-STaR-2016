import re
import sys
import subprocess

import bs4


def time_convert(string):
    """
    Receieve a string follows pattern r'[\d]{2}:[\d]{2}:[\d]{2},[\d]{3}'
    Return an int, represents time passed fromt he begining of the movie, in second.
    """
    string = re.search(r'[\d]{2}:[\d]{2}:[\d]{2},[\d]{3}', string).group(0)
    hour, minute, second, millisecond = [
        int(number) for number in re.findall(r'[\d]{2,3}', string)]
    time = (hour * 3600 + minute * 60 + second) * 1000 + millisecond

    return time


def process(xml):
    """
    Receieve whole content from a opus xml file
    Return a list of tuples (start time, end time, sentence)
        start time: int, time passed from the begining of the movie, in second
        end time: same as above
        sentence: str, without '\n' in the end.
    """

    soup = bs4.BeautifulSoup(xml, 'lxml-xml')
    sentences = []
    sentence_buffer = []
    start_time = None
    for tag in soup.document.descendants:
        if not tag.name:
            continue
        elif tag.name == 's':
            sentence_buffer.append(tag.get_text(strip=True))
        elif tag.name == 'time':
            id_ = tag.get('id')
            if id_[-1] == 'S':
                start_time = tag.get('value')
            elif id_[-1] == 'E':
                end_time = tag.get('value')
                sentences += [(start_time, start_time, sentence)
                              for sentence in sentence_buffer[:-1]]
                sentences += [(start_time, end_time, sentence_buffer[-1])]
                start_time = None
                sentence_buffer = []

    sentences = [(time_convert(s[0].encode('utf-8')), time_convert(s[1].encode('utf-8')), s[2].encode('utf-8'))
                 for s in sentences]

    return sentences


def separate(parsed_dialog, threshold=2000, iterable=True):
    def separator(parsed_dialog, threshold):  # A iterator
        last_time = parsed_dialog[0][0]
        dialog = []
        for sentence in parsed_dialog:
            # Exceed threshold time, a dialog has completed
            if not (abs(sentence[0] - last_time) < threshold):
                yield dialog
                dialog = []
            # check for multiple sentence with -, separate and remove -.
            sentences = [s[2:] for s in re.findall(
                r'(?:^|(?<= ))- .*?(?:(?= -)|$)', sentence[2])]
            if sentences:
                dialog += sentences
            else:
                dialog.append(sentence[2])
            last_time = sentence[1]

    if iterable:
        return separator(parsed_dialog, threshold)
    else:
        return [dialog for dialog in separator(parsed_dialog, threshold)]


def main(input_handle, output_handle):
    content = input_handle.read()
    parsed_dialog = process(content)
    for dialog in separate(parsed_dialog):
        output_handle.writelines(['%s\n' % sentence for sentence in dialog])
        output_handle.write('\n')


if __name__ == '__main__':
    if sys.argv[1] == '-i':
        files = [path.replace('\n', '')
                 for path in open(sys.argv[2], 'rb').readlines()]
    else:
        files = sys.argv[1:]

    for path in files:
        try:
            print path
            main(open(path, 'rb'), open('%s.processed' % path, 'wb'))
        except AttributeError:
            print 'processed : ', path
            subprocess.call(['rm', '%s.processed' % path])
            continue
        except Exception as e:
            print e
            new_file = '%s.%s' % (path[path.rfind('/', 0, path.rfind('/')) + 1:path.rfind('/')], path[path.rfind('/') + 1:])
            subprocess.call(['mv', path, '/root/data/exception/%s' % new_file])
        subprocess.call(['mv', '%s.processed' % path, path])
