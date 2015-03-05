#! /usr/bin/env python
from .writers.c import CWriter


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=argparse.FileType('r'), help='YAML file')
    parser.add_argument('--language', choices=('c', ), default='c',
                        help='BMI language')
    parser.add_argument('--clobber', action='store_true',
                        help='overwrite any existing files')

    args = parser.parse_args()

    w = CWriter.from_file_like(args.file)
    w.write(clobber=args.clobber)
