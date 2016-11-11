#! /usr/bin/env python
"""Basic Model Interface implementation."""
from collections import defaultdict, namedtuple
import types

import numpy as np

from basic_modeling_interface import Bmi

{{ includes }}


Var = namedtuple('Var', ['name', 'grid', 'units'])
Grid = namedtuple('Grid', ['id', 'rank', 'type',
                           'shape', 'spacing', 'origin'])


class Bmi{{ name|title }}(Bmi):

    _name = {{ long_name }}
    _input_var_names = (
        {% for var in input_vars %}
        '{{ var.name }}',
        {% endfor %}
    )
    _output_var_names = (
        {% for var in output_vars %}
        '{{ var.name }}',
        {% endfor %}
    )

    def __init__(self):
        """Initialize static data."""
        self._values = {}

        self._vars = {
        {% for var in vars %}
            '{{ var.name }}': Var(
                name='{{ var.name }}',
                grid={{ var.grid }},
                units='{{ var.units }}'),
        {% endfor %}
        }

        self._grids = {
        {% for grid in grids %}
            '{{ grid.id }}': Grid(
                id={{ grid.id }},
                rank={{ grid.rank }},
                type='{{ grid.type }}',
                shape=np.full({{ grid.rank }}, -1, dtype=int),
                spacing=np.full({{ grid.rank }}, -1., dtype=float),
                origin=np.full({{ grid.rank }}, 0., dtype=float),
            )
        {% endfor %}
        }

        self._grids = defaultdict(set)
        for var, grid in self._var_grid:
            self._grids[grid].add(var)

    def initialize(self, filename=None):
        """Initialize the Heat model.

        Parameters
        ----------
        filename : str, optional
            Path to name of input file.
        """
        # Implement this: Create and initialize a model handle.
        raise NotImplementedError('initialize')

        self._values = {
        {% for var in vars %}
            '{{ var.name }}': None,
        {% endfor %}
        }

    def update(self):
        """Advance model by one time step."""
        self.update_frac(1.)

    def update_frac(self, time_frac):
        """Update model by a fraction of a time step.

        Parameters
        ----------
        time_frac : float
            Fraction fo a time step.
        """
        if f < 0.:
            raise ValueError('fraction is negative')
        else:
            # Implement this: Update for a fraction of a time step.
            raise NotImplementedError('update_frac')

    def update_until(self, then):
        """Update model until a particular time.

        Parameters
        ----------
        then : float
            Time to run model until.
        """
        n_steps = (then - self.get_current_time()) / self.get_time_step()

        for _ in xrange(int(n_steps)):
            self.update()
        self.update_frac(n_steps - int(n_steps))

    def finalize(self):
        """Finalize model."""
        # Implement this: Clean up.
        raise NotImplementedError('finalize')

    def get_var_type(self, var_name):
        """Data type of variable.

        Parameters
        ----------
        var_name : str
            Name of variable as CSDMS Standard Name.

        Returns
        -------
        str
            Data type.
        """
        return str(self.get_value_ref(var_name).dtype)

    def get_var_units(self, var_name):
        """Get units of variable.

        Parameters
        ----------
        var_name : str
            Name of variable as CSDMS Standard Name.

        Returns
        -------
        str
            Variable units.
        """
        return self._vars[var_name].units

    def get_var_nbytes(self, var_name):
        """Get units of variable.

        Parameters
        ----------
        var_name : str
            Name of variable as CSDMS Standard Name.

        Returns
        -------
        int
            Size of data array in bytes.
        """
        return self.get_value_ref(var_name).nbytes

    def get_var_grid(self, var_name):
        """Grid id for a variable.

        Parameters
        ----------
        var_name : str
            Name of variable as CSDMS Standard Name.

        Returns
        -------
        int
            Grid id.
        """
        return self._vars[var_name].grid

    def get_grid_rank(self, grid_id):
        """Rank of grid.

        Parameters
        ----------
        grid_id : int
            Identifier of a grid.

        Returns
        -------
        int
            Rank of grid.
        """
        return self._grids[grid_id].rank

    def get_grid_size(self, grid_id):
        """Size of grid.

        Parameters
        ----------
        grid_id : int
            Identifier of a grid.

        Returns
        -------
        int
            Size of grid.
        """
        return np.prod(self.get_grid_shape(grid_id))

    def get_value_ref(self, var_name):
        """Reference to values.

        Parameters
        ----------
        var_name : str
            Name of variable as CSDMS Standard Name.

        Returns
        -------
        array_like
            Value array.
        """
        return self._values[var_name]

    def get_value(self, var_name):
        """Copy of values.

        Parameters
        ----------
        var_name : str
            Name of variable as CSDMS Standard Name.

        Returns
        -------
        array_like
            Copy of values.
        """
        return self.get_value_ref(var_name).copy()

    def set_value(self, var_name, src):
        """Set model values.

        Parameters
        ----------
        var_name : str
            Name of variable as CSDMS Standard Name.
        src : array_like
            Array of new values.
        """
        val = self.get_value_ref(var_name)
        val[:] = src

    def get_component_name(self):
        """Name of the component."""
        return self._name

    def get_input_var_names(self):
        """Get names of input variables."""
        return self._input_var_names

    def get_output_var_names(self):
        """Get names of output variables."""
        return self._output_var_names

    def get_grid_shape(self, grid_id):
        """Number of rows and columns of uniform rectilinear grid."""
        return self._grids[grid_id].shape

    def get_grid_spacing(self, grid_id):
        """Spacing of rows and columns of uniform rectilinear grid."""
        return self._grids[grid_id].spacing

    def get_grid_origin(self, grid_id):
        """Origin of uniform rectilinear grid."""
        return self._grids[grid_id].origin

    def get_grid_type(self, grid_id):
        """Type of grid."""
        return self._grids[grid_id].type

    def get_start_time(self):
        """Start time of model."""
        return {{ time.start }}

    def get_end_time(self):
        """End time of model."""
        # Implement this: Set end time
        return -1.

    def get_current_time(self):
        """Current time of model."""
        # Implement this: Set current time
        return -1.;

    def get_time_step(self):
        """Time step of model."""
        # Implement this: Set time step.
        return -1.;

    def get_time_units(self):
        """The units of time."""
        return {{ time.units }}
