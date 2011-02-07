"""
Migrate user files created prior to `git tag v2` in the good format
=> add an index at the beginning of each line
"""

from os import listdir
import os.path
import re


PROJECT_ROOT = os.path.abspath("..")
USER_DIR = os.path.join(PROJECT_ROOT, "user_files")
RE_SHARP = re.compile(r"#+")


def convert_file(file_str):
    file_path = os.path.join(USER_DIR, file_str)
    lines = open(file_path).readlines()
    _file = open(file_path, "w")
    for i, line in enumerate(lines):
        if line.startswith("#"):
            line = line.lstrip(RE_SHARP.findall(line)[0])  # trailing sharps
            line = "#%d|%s" % (i, line)
        else:
            line = "%d|%s" % (i, line)
        print line
        _file.write(line)
    _file.close()


if __name__ == "__main__":
    for file_str in listdir(USER_DIR):
        convert_file(file_str)
        print "file %s converted!" % file_str
