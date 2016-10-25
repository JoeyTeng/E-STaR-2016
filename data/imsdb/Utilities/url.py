import re
import sys

import bs4

def extract(html):
    link = re.search(r'<a href="(.+?)">[ \n]*?Read ([^<>]+?) Script[ \n]*?</a>', html, re.M).group(1)

    return 'wget "http://www.imsdb.com%s"\n' %link

cmd = []
for name in sys.argv[1:]:
    print('Processing %s' %name)
    try:
        cmd.append(extract(open(name, 'rb').read()))
    except AttributeError as errinfo:
        print "Error when processing %s: %s" %(name, errinfo)
        open('err.log', 'ab').write('%s\n' %name)

open('script.dl.sh', 'wb').writelines(cmd)

