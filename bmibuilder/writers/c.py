#! /usr/bin/env python
import os
from string import Template

import yaml

from . import cfuncs
from ..exchange_item import ExchangeItemList


class CWriter(object):
    def __init__(self, name, exchange_items=None, grids=None, time=None):
        self._name = name
        self._exchange_items = exchange_items or {}
        self._grids = grids or {}
        self._time = time or {}
        self._items = ExchangeItemList.from_dicts(self._exchange_items)

    @classmethod
    def from_file_like(clazz, file_like):
        desc = yaml.load(file_like)
        if desc.pop('language') != 'c':
            raise ValueError('language mismatch')
        name = desc.pop('name')
        _ = desc.pop('description')
        return clazz(name, **desc)

    @classmethod
    def from_path(clazz, path):
        with open(path, 'r') as fp:
            return clazz.from_file_like(fp)

    @property
    def h_file_name(self):
        return 'bmi_%s.h' % self._name

    @property
    def c_file_name(self):
        return 'bmi_%s.c' % self._name

    def write(self, clobber=False):
        if os.path.isfile(self.h_file_name) and not clobber:
            raise ValueError('file exists: %s', self.h_file_name)

        if os.path.isfile(self.c_file_name) and not clobber:
            raise ValueError('file exists: %s', self.c_file_name)

        with open(self.h_file_name, 'w') as fp:
            fp.write(self.h_file())

        with open(self.c_file_name, 'w') as fp:
            fp.write(self.c_file())

    def h_file(self):
        return self.header()

    def c_file(self):
        return (os.linesep * 3).join([
            self.prologue(),

            self.get_component_name(),

            self.decl_input_var_names(),
            self.get_input_var_name_count(),
            self.get_input_var_names(),
            self.decl_output_var_names(),
            self.get_output_var_name_count(),
            self.get_output_var_names(),

            self.get_start_time(),
            self.get_end_time(),
            self.get_current_time(),
            self.get_time_step(),
            self.get_time_units(),

            self.initialize(),
            self.update_frac(),
            self.update(),
            self.update_until(),
            self.finalize(),

            self.get_var_type(),
            self.get_var_units(),
            self.get_var_nbytes(),
            self.get_var_itemsize(),
            self.get_var_grid(),

            self.get_grid_type(),
            self.get_grid_rank(),
            self.get_grid_size(),

            self.get_grid_shape(),
            self.get_grid_spacing(),
            self.get_grid_origin(),

            self.get_value_ptr(),
            self.get_value(),
            self.get_value_at_indices(),

            self.set_value(),
            self.set_value_at_indices(),

            self.register_bmi(),
        ])

    def header(self):
        return cfuncs.header(self._name)

    def prologue(self):
        return Template(cfuncs.code_block("""
            #include <stdio.h>
            #include <stdlib.h>
            #include <string.h>
            #include <float.h>

            #include "bmi.h"

            ${includes}""")).substitute(
                includes=cfuncs.implement_this('Add model-specific includes'))

    def get_start_time(self):
        return cfuncs.get_start_time(self._time['start'])

    def get_end_time(self):
        return cfuncs.get_end_time()

    def get_current_time(self):
        return cfuncs.get_current_time()

    def get_time_units(self):
        return cfuncs.get_time_units(self._time['units'])

    def get_time_step(self):
        return cfuncs.get_time_step()

    def initialize(self):
        return cfuncs.initialize()

    def update_frac(self):
        return cfuncs.update_frac()

    def update(self):
        return cfuncs.update()

    def update_until(self):
        return cfuncs.update_until()

    def finalize(self):
        return cfuncs.finalize()

    def decl_input_var_names(self):
        return cfuncs.decl_input_var_names(self._items)

    def get_input_var_name_count(self):
        return cfuncs.get_input_var_name_count()

    def get_input_var_names(self):
        return cfuncs.get_input_var_names()

    def decl_output_var_names(self):
        return cfuncs.decl_output_var_names(self._items)

    def get_output_var_name_count(self):
        return cfuncs.get_output_var_name_count()

    def get_output_var_names(self):
        return cfuncs.get_output_var_names()

    def get_var_units(self):
        return cfuncs.get_var_units(self._items)
                        
    def get_var_type(self):
        return cfuncs.get_var_type(self._items)
                        
    def get_var_itemsize(self):
        return cfuncs.get_var_itemsize(self._items)
                        
    def get_var_nbytes(self):
        return cfuncs.get_var_nbytes()
                        
    def get_var_grid(self):
        return cfuncs.get_var_grid(self._items)
                        
    def get_grid_type(self):
        ids = [grid['id'] for grid in self._grids]
        types = [grid['type'] for grid in self._grids]
        return cfuncs.get_grid_type(zip(ids, types))
                        
    def get_grid_rank(self):
        ids = [grid['id'] for grid in self._grids]
        ranks = [grid['rank'] for grid in self._grids]
        return cfuncs.get_grid_rank(zip(ids, ranks))

    def get_grid_shape(self):
        ids = [grid['id'] for grid in self._grids]
        ranks = [grid['rank'] for grid in self._grids]
        return cfuncs.get_grid_shape(zip(ids, ranks))

    def get_grid_spacing(self):
        ids = [grid['id'] for grid in self._grids]
        ranks = [grid['rank'] for grid in self._grids]
        return cfuncs.get_grid_spacing(zip(ids, ranks))

    def get_grid_origin(self):
        ids = [grid['id'] for grid in self._grids]
        ranks = [grid['rank'] for grid in self._grids]
        return cfuncs.get_grid_origin(zip(ids, ranks))

    def get_grid_size(self):
        return cfuncs.get_grid_size()

    def get_value_ptr(self):
        return cfuncs.get_value_ptr(self._items)

    def get_value(self):
        return cfuncs.get_value()

    def get_value_at_indices(self):
        return cfuncs.get_value_at_indices()

    def set_value(self):
        return cfuncs.set_value()

    def set_value_at_indices(self):
        return cfuncs.set_value_at_indices()

    def get_component_name(self):
        return cfuncs.get_component_name(self._name)

    def register_bmi(self):
        return cfuncs.register_bmi(self._name)
