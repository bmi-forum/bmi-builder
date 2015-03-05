#! /usr/bin/env python
import os
import textwrap
from string import Template


def implement_this(msg=None):
    buffer = '/* Implement this'
    if msg is not None:
        buffer += ': ' + msg.strip()
    return buffer + ' */'


def strip_blank_lines(lines):
    lines = lines.split(os.linesep)
    while lines and not lines[0]:
        del lines[0]
    return os.linesep.join(lines)


def code_block(block, level=0, tab=4):
    return indent(textwrap.dedent(strip_blank_lines(block)), level=level,
                  tab=tab)


def indent(block, level=0, tab=4):
    return block.replace(os.linesep, os.linesep + ' ' * tab * level)


def if_block(first=True, level=0, tab=4):
    block = code_block("""
        if (${expr}) {
            ${block}
        }""")

    if not first:
        block = ' else ' + block

    return Template(indent(block, level=level, tab=tab))


def if_else_blocks(exprs, default=None):
    first, buffer = True, ''
    for expr, block in exprs:
        buffer += if_block(first=first, level=1).substitute(
            expr=expr, block=block)
        first = False

    if default:
        buffer += ' ' + Template(code_block("""
            else {
                ${default}
            }""", level=1)).substitute(default=default)

    return buffer


def if_strcmp_block(first=True, level=0, tab=4):
    block = if_block(first=first, level=level, tab=tab)
    return Template(block.safe_substitute(expr='strcmp(name, "${name}") == 0'))


def if_strcmp_blocks(named_blocks, default=None):
    first, buffer = True, ''
    for name, block in named_blocks:
        buffer += if_strcmp_block(first=first, level=1).substitute(
            name=name, block=block)
        first = False

    if default:
        buffer += ' ' + Template(code_block("""
            else {
                ${default}
            }""", level=1)).substitute(default=default)

    return buffer


