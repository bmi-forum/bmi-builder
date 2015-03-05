import os
import textwrap
from string import Template

from cutils import (implement_this, code_block, if_else_blocks,
                    if_strcmp_blocks)


def header(name):
    return Template(code_block(
        """
        #ifndef BMI_${upper_name}_H_INCLUDED
        #define BMI_${upper_name}_H_INCLUDED

        #if defined(__cplusplus)
        extern "C" {
        #endif

        #include <bmi.h>

        BMI_Model * register_bmi_${name}(BMI_Model *model);

        #if defined(__cplusplus)
        }
        #endif

        #endif
        """)).substitute(name=name, upper_name=name.upper())


def get_var_units(items):
    tmpl = Template(code_block("""
        static int
        get_var_units(void *self, const char *name, char *units)
        {
            ${contents}
            return BMI_SUCCESS;
        }"""))

    if len(items) == 0:
        return tmpl.substitute(contents="return BMI_FAILURE;")

    block = 'strncpy(units, "%s", BMI_MAX_UNITS_NAME);'
    blocks = [block % unit for unit in items.units]

    contents = if_strcmp_blocks(zip(items.names, blocks),
                                default="units[0] = '\\0'; return BMI_FAILURE;")

    return tmpl.substitute(contents=contents)


def get_var_type(items):
    tmpl = Template(code_block("""
        static int
        get_var_type(void *self, const char *name, char *type)
        {
            ${contents}
            return BMI_SUCCESS;
        }"""))

    if len(items) == 0:
        return tmpl.substitute(contents="return BMI_FAILURE;")

    block = 'strncpy(type, "%s", BMI_MAX_UNITS_NAME);'
    blocks = [block % type for type in items.types]

    contents = if_strcmp_blocks(zip(items.names, blocks),
                                default="type[0] = '\\0'; return BMI_FAILURE;")

    return tmpl.substitute(contents=contents)


def get_var_nbytes():
    return code_block("""
        static int
        get_var_nbytes(void *self, const char *name, int *nbytes)
        {
            int id, size, itemsize;

            if (get_var_grid(self, name, &id) == BMI_FAILURE)
                return BMI_FAILURE;

            if (get_grid_size(self, id, &size) == BMI_FAILURE)
                return BMI_FAILURE;

            if (get_var_itemsize(self, name, &itemsize) == BMI_FAILURE)
                return BMI_FAILURE;

            *nbytes = itemsize * size;

            return BMI_SUCCESS;
        }""")


def get_var_itemsize(items):
    tmpl = Template(code_block("""
        static int
        get_var_itemsize(void *self, const char *name, int *itemsize)
        {
            ${contents}
            return BMI_SUCCESS;
        }"""))

    if len(items) == 0:
        return tmpl.substitute(contents="return BMI_FAILURE;")

    blocks = ['*itemsize = sizeof(%s);' % type for type in items.types]

    contents = if_strcmp_blocks(zip(items.names, blocks),
                                default="*itemsize = 0; return BMI_FAILURE;")

    return tmpl.substitute(contents=contents)


def get_var_grid(items):
    tmpl = Template(code_block("""
        static int
        get_var_grid(void *self, const char *name, int *id)
        {
            ${contents}
            return BMI_SUCCESS;
        }"""))

    if len(items) == 0:
        return tmpl.substitute(contents="return BMI_FAILURE;")

    blocks = ['*grid = %d;' % grid for grid in items.grids]

    contents = if_strcmp_blocks(zip(items.names, blocks),
                                default="*grid = -1; return BMI_FAILURE;")

    return tmpl.substitute(contents=contents)


def decl_output_var_names(items):
    tmpl = Template(code_block("""
        #define OUTPUT_VAR_NAME_COUNT (${n_names})
        static const char *output_var_names[OUTPUT_VAR_NAME_COUNT] = {
        ${names}
        };"""))

    names = ['    "%s"' % item.name for item in items.output_items]

    return tmpl.substitute(n_names=len(names), names=',\n'.join(names))


def decl_input_var_names(items):
    tmpl = Template(code_block("""
        #define INPUT_VAR_NAME_COUNT (${n_names})
        static const char *input_var_names[INPUT_VAR_NAME_COUNT] = {
        ${names}
        };"""))

    names = ['    "%s"' % item.name for item in items.input_items]

    return tmpl.substitute(n_names=len(names), names=',\n'.join(names))


def get_output_var_name_count():
    return code_block("""
        static int
        get_output_var_name_count(void *self, int *count)
        {
            *count = OUTPUT_VAR_NAME_COUNT;
            return BMI_SUCCESS;
        }""")


def get_output_var_names():
    return code_block("""
        static int
        get_output_var_names(void *self, char **names)
        {
            int i;
            for (i=0; i<OUTPUT_VAR_NAME_COUNT; i++) {
                strncpy(names[i], output_var_names[i], BMI_MAX_VAR_NAME);
            }
            return BMI_SUCCESS;
        }""")


def get_input_var_name_count():
    return code_block("""
        static int
        get_input_var_name_count(void *self, int *count)
        {
            *count = INPUT_VAR_NAME_COUNT;
            return BMI_SUCCESS;
        }""")


def get_input_var_names():
    return code_block("""
        static int
        get_input_var_names(void *self, char **names)
        {
            int i;
            for (i=0; i<INPUT_VAR_NAME_COUNT; i++) {
                strncpy(names[i], input_var_names[i], BMI_MAX_VAR_NAME);
            }
            return BMI_SUCCESS;
        }""")


def get_start_time(time):
    return Template(code_block("""
        static int
        get_start_time(void * self, double *time)
        {
            *time = ${time};
            return BMI_SUCCESS;
        }""")).substitute(time=time)


def get_end_time():
    return Template(code_block("""
        static int
        get_end_time(void * self, double *time)
        { ${note}
            *time = -1.;
            return BMI_FAILURE;
        }""")).substitute(note=implement_this('Set end time'))


def get_current_time():
    return Template(code_block("""
        static int
        get_current_time(void * self, double *time)
        { ${note}
            *time = -1.;
            return BMI_FAILURE;
        }""")).substitute(note=implement_this('Set current time'))


def get_time_units(units):
    return Template(code_block("""
        static int
        get_time_units(void * self, char *units)
        {
            strncpy(units, "${units}", BMI_MAX_UNITS_NAME);
            return BMI_SUCCESS;
        }""")).substitute(units=units)


def get_time_step():
    return Template(code_block("""
        static int
        get_time_step(void * self, double *dt)
        { ${note}
            *dt = -1.;
            return BMI_FAILURE;
        }""")).substitute(note=implement_this('Set time step'))


def get_grid_type(grids):
    tmpl = Template(code_block("""
        static int
        get_grid_type(void *self, int id, char *type)
        {
            ${contents}
            return BMI_SUCCESS;
        }"""))

    if len(grids) == 0:
        return tmpl.substitute(contents="return BMI_FAILURE;")

    exprs = []
    for (id, grid_type) in grids:
        exprs.append(('id == %d' % id,
                      'strncpy(type, "%s", 2048);' % grid_type))
    default="type[0] = '\\0'; return BMI_FAILURE;"

    contents = if_else_blocks(exprs, default=default)

    return tmpl.substitute(contents=contents)


def get_grid_rank(grids):
    tmpl = Template(code_block("""
        static int
        get_grid_rank(void *self, int id, int *rank)
        {
            ${contents}
            return BMI_SUCCESS;
        }"""))

    if len(grids) == 0:
        return tmpl.substitute(contents="return BMI_FAILURE;")

    exprs = []
    for (id, rank) in grids:
        exprs.append(('id == %d' % id, '*rank = %d;' % rank))
    default="rank = -1; return BMI_FAILURE;"

    contents = if_else_blocks(exprs, default=default)

    return tmpl.substitute(contents=contents)


def get_grid_size():
    return code_block("""
        static int
        get_grid_size(void *self, int id, int *size)
        {
            int rank;
            if (get_grid_rank(self, id, &rank) == BMI_FAILURE)
                return BMI_FAILURE;

            {
                int * shape = (int*) malloc(sizeof(int) * rank);
                int i;
                *size = 1;
                for (i=0; i<rank; i++)
                    *size *= shape[i];
                free(shape);
            }

            return BMI_SUCCESS;
        }""")


def get_grid_shape(grids):
    tmpl = Template(code_block("""
        static int
        get_grid_shape(void *self, int id, int *shape)
        {
            ${contents}
            return BMI_SUCCESS;
        }"""))

    if len(grids) == 0:
        return tmpl.substitute(contents="return BMI_FAILURE;")

    exprs = []
    for (id, rank) in grids:
        statements = ['shape[%d] = ;' % i for i in xrange(rank)]
        exprs.append(('id == %d' % id, ' '.join(statements)))
    statements = ['shape[%d] = -1;' % i for i in xrange(rank)]
    default="%s; return BMI_FAILURE;" % ' '.join(statements)

    contents = if_else_blocks(exprs, default=default)

    return tmpl.substitute(contents=contents)


def get_grid_spacing(grids):
    tmpl = Template(code_block("""
        static int
        get_grid_spacing(void *self, int id, double *spacing)
        {
            ${contents}
            return BMI_SUCCESS;
        }"""))

    if len(grids) == 0:
        return tmpl.substitute(contents="return BMI_FAILURE;")

    exprs = []
    for (id, rank) in grids:
        statements = ['spacing[%d] = ;' % i for i in xrange(rank)]
        exprs.append(('id == %d' % id, ' '.join(statements)))
    statements = ['spacing[%d] = -1.;' % i for i in xrange(rank)]
    default="%s; return BMI_FAILURE;" % ' '.join(statements)

    contents = if_else_blocks(exprs, default=default)

    return tmpl.substitute(contents=contents)


def get_grid_origin(grids):
    tmpl = Template(code_block("""
        static int
        get_grid_origin(void *self, int id, double *spacing)
        {
            ${contents}
            return BMI_SUCCESS;
        }"""))

    if len(grids) == 0:
        return tmpl.substitute(contents="return BMI_FAILURE;")

    exprs = []
    for (id, rank) in grids:
        statements = ['origin[%d] = ;' % i for i in xrange(rank)]
        exprs.append(('id == %d' % id, ' '.join(statements)))
    statements = ['origin[%d] = -1.;' % i for i in xrange(rank)]
    default="%s; return BMI_FAILURE;" % ' '.join(statements)

    contents = if_else_blocks(exprs, default=default)

    return tmpl.substitute(contents=contents)


def get_value():
    return code_block("""
        int
        get_value(void * self, const char * name, void *dest)
        {
            void *src = NULL;
            int nbytes = 0;

            if (get_value_ptr (self, name, &src) == BMI_FAILURE)
                return BMI_FAILURE;

            if (get_var_nbytes (self, name, &nbytes) == BMI_FAILURE)
                return BMI_FAILURE;

            memcpy(dest, src, nbytes);

            return BMI_SUCCESS
        }""")


def get_value_ptr(items):
    tmpl = Template(code_block("""
        static int
        get_value_ptr(void *self, const char *name, void **dest)
        {
            ${contents}

            if (*dest)
                return BMI_SUCCESS;
            else
                return BMI_FAILURE;
        }"""))

    if len(items) == 0:
        return tmpl.substitute(contents="return BMI_FAILURE;")

    blocks = []
    for name in items.names:
        blocks.append('*dest = NULL; %s' %
                      implement_this('Pointer to %s' % name))
    default = "*dest = NULL; return BMI_FAILURE;"

    contents = if_strcmp_blocks(zip(items.names, blocks), default=default)

    return tmpl.substitute(contents=contents)


def get_value_at_indices():
    return code_block("""
        static int
        get_value_at_indices (void *self, const char *name, void *dest,
            int * inds, int len)
        {
            void *src = NULL;
            int itemsize = 0;

            if (get_value_ptr(self, name, &src) == BMI_FAILURE)
                return BMI_FAILURE;

            if (get_var_itemsize(self, name, &itemsize) == BMI_FAILURE)
                return BMI_FAILURE;

            { /* Copy the data */
                int i;
                int offset;
                void * ptr;
                for (i=0, ptr=dest; i<len; i++, ptr+=itemsize) {
                    offset = inds[i] * itemsize;
                    memcpy (ptr, src + offset, itemsize);
                }
            }

            return BMI_SUCCESS;
        }""")


def set_value():
    return code_block("""
        static int
        set_value (void *self, const char *name, void *array)
        {
            void * dest = NULL;
            int nbytes = 0;

            if (get_value_ptr(self, name, &dest) == BMI_FAILURE)
                return BMI_FAILURE;

            if (get_var_nbytes(self, name, &nbytes) == BMI_FAILURE)
                return BMI_FAILURE;
    
            memcpy (dest, array, nbytes);

            return BMI_SUCCESS;
        }""")


def set_value_at_indices():
    return code_block("""
        static int
        set_value_at_indices (void *self, const char *name, int * inds, int len,
            void *src)
        {
            void * to = NULL;
            int itemsize = 0;

            if (get_value_ptr (self, name, &to) == BMI_FAILURE)
                return status;

            if (get_var_itemsize(self, name, &itemsize) == BMI_FAILURE)
                return BMI_FAILURE;

            { /* Copy the data */
                int i;
                int offset;
                void * ptr;
                for (i=0, ptr=src; i<len; i++, ptr+=itemsize) {
                    offset = inds[i] * itemsize;
                    memcpy (to + offset, ptr, itemsize);
                }
            }
            return BMI_SUCCESS;
        }""")


def get_component_name(name):
    return Template(code_block("""
        static int
        get_component_name (void *self, char * name)
        {
            strncpy (name, "${name}", BMI_MAX_COMPONENT_NAME);
            return BMI_SUCCESS;
        }""")).substitute(name=name)


def initialize():
    return code_block("""
        static int
        initialize(const char * file, void **handle)
        { %s
            return BMI_FAILURE;
        }""") % implement_this('Create and initialize a model handle')


def update_frac():
    return code_block("""
        static int
        update_frac(void * self, double *f)
        { %s
            return BMI_FAILURE;
        }""") % implement_this('Update for a fraction of a time step')


def update():
    return code_block("""
        static int
        update(void * self, double *f)
        {
            return update_frac(self, 1.);
        }""")


def update_until():
    return code_block("""
        static int
        update_until(void * self, double *f)
        {
            double dt;
            double now;

            if (get_time_step(self, &dt) == BMI_FAILURE)
                return BMI_FAILURE;

            if (get_current_time(self, &now) == BMI_FAILURE)
                return BMI_FAILURE;

            {
                int n;
                const double n_steps = (t - now) / dt;
                for (n=0; n<(int)n_steps; n++) {
                    if (update(self) == BMI_FAILURE)
                        return BMI_FAILURE;
                }

                if (update_frac(self, n_steps - (int)n_steps) == BMI_FAILURE)
                    return BMI_FAILURE;
            }

            return BMI_SUCCESS;
        }""")


def finalize():
    return code_block("""
        static int
        finalize(void * self)
        { %s
            return BMI_FAILURE;
        }""") % implement_this('Clean up')


def register_bmi(name):
    return Template(code_block("""
        BMI_Model*
        register_bmi_${name}(BMI_Model *model)
        {
            model->self = NULL;

            model->initialize = initialize;
            model->update = update;
            model->update_until = update_until;
            model->update_frac = update_frac;
            model->finalize = finalize;
            model->run_model = NULL;

            model->get_component_name = get_component_name;
            model->get_input_var_name_count = get_input_var_name_count;
            model->get_output_var_name_count = get_output_var_name_count;
            model->get_input_var_names = get_input_var_names;
            model->get_output_var_names = get_output_var_names;

            model->get_var_type = get_var_type;
            model->get_var_units = get_var_units;
            model->get_var_rank = get_var_rank;
            model->get_var_size = get_var_size;
            model->get_var_nbytes = get_var_nbytes;
            model->get_current_time = get_current_time;
            model->get_start_time = get_start_time;
            model->get_end_time = get_end_time;
            model->get_time_units = get_time_units;
            model->get_time_step = get_time_step;

            model->get_value = get_value;
            model->get_value_ptr = get_value_ptr;
            model->get_value_at_indices = get_value_at_indices;

            model->set_value = set_value;
            model->set_value_ptr = NULL;
            model->set_value_at_indices = set_value_at_indices;

            model->get_grid_type = get_grid_type;
            model->get_grid_shape = get_grid_shape;
            model->get_grid_spacing = get_grid_spacing;
            model->get_grid_origin = get_grid_origin;

            model->get_grid_x = NULL;
            model->get_grid_y = NULL;
            model->get_grid_z = NULL;

            return model;
        }""")).substitute(name=name)
