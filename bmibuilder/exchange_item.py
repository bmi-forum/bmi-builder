#! /usr/bin/env python
import yaml


class ExchangeItem(object):
    def __init__(self, name, grid=-1, type='double', units='-',
                 intent='in'):
        if intent not in ['in', 'inout', 'out']:
            raise ValueError('intent not understood')

        if type not in ['float', 'double', 'int', 'long', 'boolean']:
            raise ValueError('data type not understood')

        self._name = name
        self._grid = grid
        self._type = type
        self._units = units
        self._intent = intent

    @classmethod
    def from_dict(clazz, d):
        name = d.pop('name')
        item = clazz(name, **d)
        d['name'] = name
        return item

    @property
    def isinput(self):
        return self._intent.startswith('in')

    @property
    def isoutput(self):
        return self._intent.endswith('out')

    @property
    def isinout(self):
        return self._intent == 'inout'

    @property
    def name(self):
        return self._name

    @property
    def grid(self):
        return self._grid

    @property
    def type(self):
        return self._type

    @property
    def units(self):
        return self._units

    @property
    def intent(self):
        return self._intent


class ExchangeItemList(object):
    def __init__(self, items):
        self._items = dict([(i.name, i) for i in items])

    @classmethod
    def from_path(clazz, path):
        with open(path, 'r') as fp:
            items = yaml.load(fp)

        if isinstance(items, dict):
            items =  items['exchange_items']

        return clazz.from_dicts(items)

    @classmethod
    def from_dicts(clazz, dicts):
        return clazz([ExchangeItem.from_dict(d) for d in dicts])

    @property
    def items(self):
        return self._items.values()

    @property
    def names(self):
        return [item.name for item in self.items]

    @property
    def types(self):
        return [item.type for item in self.items]

    @property
    def units(self):
        return [item.units for item in self.items]

    @property
    def grids(self):
        return [item.grid for item in self.items]

    @property
    def input_items(self):
        return [item for item in self._items.values() if item.isinput]

    @property
    def output_items(self):
        return [item for item in self._items.values() if item.isoutput]

    @property
    def inout_items(self):
        return [item for item in self._items.values() if item.isinout]

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        for item in self._items:
            yield item
