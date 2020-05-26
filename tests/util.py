"helper methods for testing"
import os
import textwrap
from collections import namedtuple

from py.error import EEXIST

File = namedtuple("File", "name, contents")


def make_files_and_cd(tmpdir, files):
    "makes files and moves to that directory"
    for file in files:
        t = make_file(tmpdir, file)
        assert t.check()
    os.chdir(tmpdir)


def make_file(tmpdir, file):
    "makes files for testing"
    directories = file.name.split("/")
    filename = directories.pop()
    t = tmpdir
    for directory in directories:
        t = t.join(directory)
        try:
            t.mkdir()
        except EEXIST:
            pass
    t = t.join(filename)
    t.write(textwrap.dedent(file.contents))
    return t
