import os
import shutil
import subprocess
import re
import sys
from os import getcwd, chdir
from sys import exit
import platform

from contextlib import contextmanager
from .constants import WINDOWS, LINUX


class EnvironmentVariables(object):
    """
    Proxy for environment variables
    """
    def getenv(self, name, defaultvalue=""):
        if name in os.environ:
            return os.environ[name]
        return defaultvalue

    def __repr__(self):
        lines = []
        for name in sorted(os.environ):
            lines.append("{}={}".format(name, self.getenv(name)))
        return "\n".join(lines)

    def __getitem__(self, item):
        return self.getenv(item)

    def __getattr__(self, item):
        return self.getenv(item)

    def __setattr__(self, key, value):
        os.environ[key] = str(value)


ENV = EnvironmentVariables()


def hr():
    """
    Print a horizontal line
    :return:
    """
    print("-" * 80)


def cd(path=None):
    """
    Wrap os.chdir
    :param path:
    :return:
    """
    if path:
        os.chdir(path)

    return getcwd()


def ls(path=None):
    """
    Return a list of files and folders
    :param path:
    :return:
    """
    if not path:
        path = getcwd()
    return os.listdir(path)


def delete(path):
    """
    Recursivley remove the given path
    :param path:
    :return:
    """
    if os.path.exists(path):
        shutil.rmtree(path)


def touch(path):
    """
    Touch a file
    :param path:
    :return:
    """
    open(path, "a").close()


def mkdir(path):
    """
    Make a directory if it doesn't exist
    :param path:
    :return:
    """
    if not os.path.isdir(path):
        os.makedirs(path)


def call(*args):
    """
    Wrap subprocess.check_call()
    :param args:
    :return:
    """
    subprocess.check_call(args, shell=False, cwd=getcwd())


def start(*args):
    """
    Wrap subprocess.Popen()
    :param args:
    :return:
    """
    return subprocess.Popen(args, shell=False)


def capture(*args, **kwargs):
    """
    Wrap subprocess.check_output()
    :param args:
    :param raise_errors:
    :param decode:
    :param strip: if True, and if decode, strip off trailing and leading whitespace
    :return:
    """

    try:
        result = subprocess.check_output(args, **kwargs)
    except subprocess.CalledProcessError as cpe:
        if not kwargs.get("raise_errors", True):
            result = cpe.output
        else:
            raise

    if kwargs.get("decode", True):
        result = result.decode()
        if kwargs.get("strip", True):
            result = result.strip()

    return result


def cp(source, dest):
    """
    wrapper around shutil.copy()
    :param source: original file or folder,
    :param dest: new location, if it exists, source is copied inside, else the copy is named dest
    :return:
    """
    shutil.copy(source, dest)


def grep(filename, pattern, inverse=False):
    """
    Filter the file for lines that match pattern
    :param filename:
    :param pattern:
    :param inverse: negate matches

    If data is a string, it is split into lines before grepping
    :return:
    """
    result = []

    with open(filename, "r") as infile:
        for line in infile:
            line = line.rstrip()
            found = re.search(pattern, line)
            if found and not inverse or inverse and not found:
                result.append(line)

    return result


@contextmanager
def block(title=""):
    print(("Begin " + title).center(80, "-"))
    try:
        yield
        print(("Ended " + title).center(80, "-"))
    except Exception:
        print(("Failed " + title).center(80, "-"))
        sys.stdout.flush()
        raise
