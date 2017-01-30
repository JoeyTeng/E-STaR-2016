#!/usr/bin/python3.5
import subprocess
import glob
import sys

dirname = sys.argv[1]
head = r'<?xml version="1.0" encoding="utf-8"?>'.encode()

print("Scanning")
for path in glob.iglob('%s/**/*.txt' % dirname, recursive=True):
    print(path)
    if path.find('.tokenized.') == -1:
        print("Removed")
        subprocess.call(['rm', path])
    else:
        subprocess.call(['mv', path, path.replace('.txt.tokenized.txt', '.txt')])
