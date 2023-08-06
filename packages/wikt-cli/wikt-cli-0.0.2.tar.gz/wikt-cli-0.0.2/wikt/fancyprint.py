from colored import fg, attr
# color chart see https://pypi.org/project/colored/


class Printer:
    """ Utility to print colorful text """

    def __init__(self, color=True):
        # color: set to False to diable colors
        self._color = color

    def _colorprint(self, text, fgc):
        if self._color:
            print(f'{fg(fgc)}{text}{attr(0)}')
        else:
            print(text)

    def black(self, t):
        self._colorprint(t, 0)

    def red(self, t):
        self._colorprint(t, 1)

    def green(self, t):
        self._colorprint(t, 2)

    def yellow(self, t):
        self._colorprint(t, 3)

    def blue(self, t):
        self._colorprint(t, 4)

    def magenta(self, t):
        self._colorprint(t, 5)

    def cyan(self, t):
        self._colorprint(t, 6)

    def gray(self, t):
        self._colorprint(t, 7)

    def white(self, t):
        self._colorprint(t, 15)
