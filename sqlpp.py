#!/usr/bin/env python

import os, sys, shutil
import sqlparse
from optparse import OptionParser
import tempfile

def pprint(reader, writer):
    writer.write(sqlparse.format(reader.read(), reindent=True, keyword_case='upper'))

def pprint_inplace(file):
    temp = tempfile.NamedTemporaryFile(mode="wb", suffix=".buf")
    with open(file) as f:
        pprint(f, temp)
    shutil.copyfile(temp.name, file)
    temp.close()

def main():
    parser = OptionParser()
    parser.add_option("-i", "--in-place", action="store_true", default=False)
    (options, files) = parser.parse_args()

    # sqlpp < infile > outfile
    if len(files) == 0:
        pprint(sys.stdin, sys.stdout)
        return

    if options.in_place:
        # sqlpp -i infile1, infile2, ...
        for file in files:
            pprint_inplace(file)
    else:
        # sqlpp infile1, infile2, ...
        for file in files:
            with open(file) as f:
                pprint(f, sys.stdout)

    # sqlpp -i dir1, dir2, ...

if __name__ == '__main__':
    main()
