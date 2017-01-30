#!/usr/bin/python3.5
import subprocess
import glob
import sys

dirname = sys.argv[1]
head = r'<?xml version="1.0" encoding="utf-8"?>'.encode()

print("Scanning")
for path in glob.iglob('%s/**/*.xml' % dirname, recursive=True):
    print(path)
    if open(path, 'rb').read().startswith(head):
        print("Removed")
        subprocess.call(['mv', path, '/root/data/exception/%s' % path[path.rfind('/') + 1:]])
    else:
        subprocess.call(['mv', path, path.replace('.xml', '.txt')])
