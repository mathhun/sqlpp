#!/usr/bin/env python

import os, sys, shutil
import sqlparse
from optparse import OptionParser
import tempfile

def pprint(reader, writer):
    writer.write(sqlparse.format(reader.read(), reindent=True, keyword_case='upper'))

def pprint_inplace(file):
    temp = tempfile.NamedTemporaryFile(suffix=".sqlpp.tmp", delete=False)
    with open(file, "r") as f:
        pprint(f, temp)
    temp.flush()
    os.rename(temp.name, file)
    temp.close()

def main():
    parser = OptionParser()
    parser.add_option("-i", "--in-place", action="store_true", default=False)
    (options, files) = parser.parse_args()

    if len(files) == 0:
        pprint(sys.stdin, sys.stdout)
        return

    if options.in_place:
        for file in files:
            pprint_inplace(file)
    else:
        for file in files:
            with open(file) as f:
                pprint(f, sys.stdout)

if __name__ == '__main__':
    main()
