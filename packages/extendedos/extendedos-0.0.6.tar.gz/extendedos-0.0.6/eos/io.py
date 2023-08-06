import sys


class Tee(object):

    """Write like tee

    Parameters
    ----------
    target : file
        file object
    original : file
        file object. default is sys.stdout

    Examples
    --------

    """

    def __init__(self, target, original=sys.stdout):
        self.original = original
        self.target = target

    def write(self, b):
        self.original.write(b)
        self.target.write(b)

    def __call__(self, b):
        self.write(b)


class FileWriter(object):

    """Write File io

    Parameters
    ----------
    path : str
        write file path.
    overwrite : bool
        flag of over write. If True, open with with 'w' option.
    """

    def __init__(self, path, overwrite=False):
        # self.path = pycompat.text_type(path)
        self.overwrite = overwrite

    def write(self, s):
        with open(self.path, 'w' if self.overwrite else 'a',
                  encoding='utf-8') as output_file:
            output_file.write(s)
        self.overwrite = False

    def __call__(self, s):
        self.write(s)
