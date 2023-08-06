import os

try:
    term_width = os.get_terminal_size()[0]
except OSError:
    term_width = 80

def leftpad(s: str, n: int, w=term_width) -> str:
    # s is the string, n is indent, w is max width including whitespace
    return '\n'.join([' ' * n + l for l in softwrap(s, w - n)])


def softwrap(s: str, width: int) -> list:
    words = s.split()
    wrapped = []
    line = ''
    for w in words:
        if len(line) + 1 + len(w) <= width:
            line += w + ' '
        else:
            wrapped.append(line)
            line = w + ' '
    wrapped.append(line)
    return wrapped
