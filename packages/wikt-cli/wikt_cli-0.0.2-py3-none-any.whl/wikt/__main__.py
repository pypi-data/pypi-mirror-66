from argparse import ArgumentParser
import sys
import os
import textwrap
from wiktionaryparser import WiktionaryParser
from .utils import *
from .fancyprint import Printer
import colored


def main():
    wikt = WiktionaryParser()

    argparser = ArgumentParser()
    argparser.add_argument('word', help='word to look up')
    argparser.add_argument('-d', '--definition',
                           action='store_true', help='print definition only')
    argparser.add_argument(
        '--no-color', action='store_true', default=False,
        help='disable color printing (when stdout is not a tty this is automatically on)')
    args = argparser.parse_args()

    # only use colors when user did not specify --no-color 
    # and the output is printed in a tty, i.e. console/terminal,
    # not a file/pipe.
    color_on = (not args.no_color) and sys.stdout.isatty()
    printer = Printer(color_on)

    try:
        etymologies = wikt.fetch(args.word)
        # an example etymologies dict for debug use is in ../example.py
    except KeyboardInterrupt:
        printer.red('\nAborted')
        sys.exit(1)

    for ety_no, etymology in enumerate(etymologies, 1):
        if not args.definition:
            printer.blue(f'Etymology {ety_no}:')
            printer.white(leftpad(etymology['etymology'], 4))
            print()

        printer.cyan(leftpad('Definitions:', 4))

        for definition in etymology['definitions']:
            printer.white(leftpad('({0}) {1}'.format(
                # print PoS in green if --no-color is not present
                (colored.fg(2) + definition['partOfSpeech'] + colored.attr(0)
                    if color_on else definition['partOfSpeech']),
                definition['text'][0]), 8))

            for line_no, line in enumerate(definition['text'][1:], 1):
                printer.white(leftpad(str(line_no) + '. ' + line, 12))

            print()

            if definition['examples'] and not args.definition:
                printer.yellow(leftpad('Examples:', 12))
                for ex_no, example in enumerate(definition['examples'], 1):
                    printer.white(leftpad(str(ex_no) + '. ' + example, 16))

        print()


if __name__ == '__main__':
    main()
