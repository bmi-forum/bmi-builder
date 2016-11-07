#! /usr/bin/env python
import os

from distutils.dir_util import mkpath
from jinja2 import Environment, FileSystemLoader
import yaml


from .writers.c import CWriter


YAML_TEMPLATE = """
name: <str>
language: c
grids:
    - id: <int>
      type: <str>
      rank: <int>
time:
    units: <str>
    start: <float>
    end: <float>
exchange_items:
    - name: <str>
      grid: <id>
      type: <str>
      units: <str>
      intent: {in, out, inout}
"""

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'templates')


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=argparse.FileType('r'), help='YAML file')
    parser.add_argument('--language', choices=('c', 'cxx', 'python'),
                        default='c', help='BMI language')
    parser.add_argument('--clobber', action='store_true',
                        help='Overwrite any existing files.')

    args = parser.parse_args()

    path_to_templates = os.path.join(TEMPLATE_PATH, args.language)
    env = Environment(loader=FileSystemLoader(path_to_templates),
                     trim_blocks=True, lstrip_blocks=True)

    meta = yaml.load(args.file)
    meta['input_vars'] = [
        var for var in meta['exchange_items'] if var['intent'].startswith('in')]
    meta['output_vars'] = [
        var for var in meta['exchange_items'] if var['intent'].endswith('out')]
    meta['vars'] = meta['exchange_items']

    for name in env.list_templates():
        base, ext = os.path.splitext(name)
        template = env.get_template(name)
        if os.path.isfile(name) and not args.clobber:
            print '{name}: file exists. skipping.'.format(name=name)
        else:
            mkpath(os.path.dirname(name))
            with open(name, 'w') as fp:
                fp.write(template.render(meta))
