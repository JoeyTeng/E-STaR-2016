import re
import sys
import subprocess


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


def process(srt):
    """
    Receieve whole content from a .srt file
    Return a list of tuples (start time, end time, sentence)
        start time: int, time passed from the begining of the movie, in second
        end time: same as above
        sentence: str, without '\n' in the end.
    """
    srt = re.sub(r'<[\/a-z]+>', '', srt)
    srt = srt.replace('\r', '')
    srt = srt.replace('\n', ' ')

    pattern_time = r'[\d]{2}:[\d]{2}:[\d]{2},[\d]{3}'
    pattern_connect_label = r' --> '
    pattern_timestamp = r'%s%s%s' % (
        pattern_time, pattern_connect_label, pattern_time)
    pattern_line_number = r'[\d]+ '

    # remove all line number
    srt = re.sub(r'%s(?=%s)' %
                 (pattern_line_number, pattern_timestamp), '', srt)
    sentences = re.findall((r'((?:%s).+?)(?=%s)' %
                            (pattern_timestamp, pattern_timestamp)), srt)
    sentences = [((re.search((r'(%s)' % pattern_time), sentence).group(0)),  # start time
                  (re.search((r'(?<=%s)(%s)' % (pattern_connect_label,
                                                pattern_time)), sentence).group(0)),  # end time
                  (re.search((r'(?<=%s)[ ]*(.*?)[ ]*$' % pattern_timestamp), sentence).group(1)))  # sentence
                 for sentence in sentences]
    sentences = [(time_convert(s[0]), time_convert(s[1]), s[2])
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
    for path in sys.argv[1:]:
        main(open(path, 'rb'), open('%s.processed' % path, 'wb'))
        subprocess.call(['mv', '%s.processed', '%s'])
