#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <float.h>

#include "bmi.h"

{{ includes }}

#define return_on_error(stmt)                 \
  {                                           \
    const int status = (stmt);                \
    if (status != BMI_SUCCESS) return status; \
  }


static int get_component_name(void *self, char *name) {
  strncpy(name, "{{ long_name }}", BMI_MAX_COMPONENT_NAME);
  return BMI_SUCCESS;
}

#define INPUT_VAR_NAME_COUNT ({{ input_vars|length }})
const char *input_var_names[INPUT_VAR_NAME_COUNT] = {
  {% for var in input_vars %}
  "{{ var.name }}" {% if not loop.last %},{% endif %} 
  {% endfor %}
};

#define OUTPUT_VAR_NAME_COUNT ({{ output_vars|length }})
const char *output_var_names[OUTPUT_VAR_NAME_COUNT] = {
  {% for var in output_vars %}
  "{{ var.name }}" {% if not loop.last %},{% endif %} 
  {% endfor %}
};

static int get_input_var_name_count(void *self, int *count) {
  *count = INPUT_VAR_NAME_COUNT;
  return BMI_SUCCESS;
}

static int get_input_var_names(void *self, char **names) {
  int i;
  for (i = 0; i < INPUT_VAR_NAME_COUNT; i++) {
    strncpy(names[i], input_var_names[i], BMI_MAX_VAR_NAME);
  }
  return BMI_SUCCESS;
}

static int get_output_var_name_count(void *self, int *count) {
  *count = OUTPUT_VAR_NAME_COUNT;
  return BMI_SUCCESS;
}

static int get_output_var_names(void *self, char **names) {
  int i;
  for (i = 0; i < OUTPUT_VAR_NAME_COUNT; i++) {
    strncpy(names[i], output_var_names[i], BMI_MAX_VAR_NAME);
  }
  return BMI_SUCCESS;
}

static int get_start_time(void *self, double *time) {
  if (time) {
    *time = {{ time.start }};
    return BMI_SUCCESS;
  } else {
    return BMI_FAILURE;
  }
}

static int get_end_time(void *self, double *time) {
  // Implement this: Set end time
  *time = -1.;
  return BMI_SUCCESS;
}

static int get_current_time(void *self, double *time) {
  // Implement this: Set current time
  *time = -1.;
  return BMI_SUCCESS;
}

static int get_time_step(void *self, double *dt) {
  // Implement this: Set time step.
  *dt = -1.;
  return BMI_SUCCESS;
}

static int get_time_units(void *self, char *units) {
  strncpy(units, "{{ time.units }}", BMI_MAX_UNITS_NAME);
  return BMI_SUCCESS;
}

static int initialize(const char *config_file, void **handle) {
  // Implement this: Create and initialize a model handle.
  return BMI_FAILURE;
}

static int update_frac(void *self, double f) {
  if (f < 0)
    return BMI_FAILURE;
  else {
    // Implement this: Update for a fraction of a time step.
    return BMI_SUCCESS;
  }
}

static int update(void *self) {
  return update_frac(self, 1.);
}

static int update_until(void *self, double t) {
  {
    double dt;
    double now;

    get_time_step(self, &dt);
    get_current_time(self, &now);

    {
      int n;
      const double n_steps = (t - now) / dt;
      const int n_full_steps = (int)n_steps;
      for (n = 0; n < n_full_steps; n++) {
        update(self);
      }

      update_frac(self, n_steps - n_full_steps);
    }
  }

  return BMI_SUCCESS;
}

static int finalize(void *self) {
  // Implement this: Clean up.
  return BMI_FAILURE;
}

static int get_grid_rank(void *self, int grid_id, int *rank) {
  {% for grid in grids %}
    {% if loop.first %}
  if (grid_id == {{ grid.id }}) {
   {% else %}
  } else if (grid_id == {{ grid.id }}) {
    {% endif %}
    *rank = {{ grid.rank }};
  {% endfor %}
  } else {
    *rank = -1;
    return BMI_FAILURE;
  }
  return BMI_SUCCESS;
}

static int get_grid_size(void *self, int grid_id, int *size) {
  int rank = -1;

  if (get_grid_rank(self, grid_id, &rank) == BMI_FAILURE)
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
}

static int get_grid_shape(void *self, int grid_id, int *shape) {
  {% for grid in grids %}

    {% if loop.first %}
  if (grid_id =={{ grid.id }}) {
    {% else %}
  } else if (grid_id == {{ grid.id }}) {
    {% endif %}
    {% for dim in range(grid.rank) %}
    shape[{{ dim }}] = -1;
    {% endfor %}
  {% endfor %}
  } else {
    return BMI_FAILURE;
  }
  return BMI_SUCCESS;
}

static int get_grid_spacing(void *self, int grid_id, double *spacing) {
  {% for grid in grids %}

    {% if loop.first %}
  if (grid_id == {{ grid.id }}) {
    {% else %}
  } else if (grid_id == {{ grid.id }}) {
    {% endif %}
    {% for dim in range(grid.rank) %}
    spacing[{{ dim }}] = -1.;
    {% endfor %}
  {% endfor %}
  } else {
    return BMI_FAILURE;
  }
  return BMI_SUCCESS;
}

static int get_grid_origin(void *self, int grid_id, double *origin) {
  {% for grid in grids %}
    {% if loop.first %}
  if (grid_id == {{ grid.id }}) {
    {% else %}
  } else if (grid_id == {{ grid.id }}) {
    {% endif %}
    {% for dim in range(grid.rank) %}
    origin[{{ dim }}] = -1.;
    {% endfor %}
  {% endfor %}
  } else {
    return BMI_FAILURE;
  }
  return BMI_SUCCESS;
}

static int get_grid_x(void *self, int grid_id, double *x) {
  {% for grid in grids %}
    {% if loop.first %}
  if (grid_id == {{ grid.id }}) {
    {% else %}
  } else if (grid_id == {{ grid.id }}) {
    {% endif %}
    // Implement this: set x values for grid.
  {% endfor %}
  } else {
    return BMI_FAILURE;
  }
  return BMI_SUCCESS;
}

static int get_grid_y(void *self, int grid_id, double *y) {
  {% for grid in grids %}
    {% if loop.first %}
  if (grid_id == {{ grid.id }}) {
    {% else %}
  } else if (grid_id == {{ grid.id }}) {
    {% endif %}
    // Implement this: set y values for grid.
  {% endfor %}
  } else {
    return BMI_FAILURE;
  }
  return BMI_SUCCESS;
}

static int get_grid_connectivity(void *self, int grid_id, double *c) {
  {% for grid in grids %}
    {% if loop.first %}
  if (grid_id == {{ grid.id }}) {
    {% else %}
  } else if (grid_id == {{ grid.id }}) {
    {% endif %}
    // Implement this: set connectivity of nodes.
  {% endfor %}
  } else {
    return BMI_FAILURE;
  }
  return BMI_SUCCESS;
}

static int get_grid_offset(void *self, int grid_id, double *o) {
  {% for grid in grids %}
    {% if loop.first %}
  if (grid_id == {{ grid.id }}) {
    {% else %}
  } else if (grid_id == {{ grid.id }}) {
    {% endif %}
    // Implement this: set offsets into connectivity array.
  {% endfor %}
  } else {
    return BMI_FAILURE;
  }
  return BMI_SUCCESS;
}

static int get_grid_type(void *self, int grid_id, char *gtype) {
  {% for grid in grids %}
    {% if loop.first %}
  if (grid_id == {{ grid.id }}) {
   {% else %}
  } else if (grid_id == {{ grid.id }}) {
    {% endif %}
    strncpy(gtype, "{{ grid.type }}", 2048);
  {% endfor %}
  } else {
    *gtype = '\0';
    return BMI_FAILURE;
  }
  return BMI_SUCCESS;
}

static int get_var_grid(void *self, const char *name, int *grid_id) {
  {% for var in vars %}
    {% if loop.first %}
  if (strcmp(name, "{{ var.name }}") == 0 ) {
    {% else %}
  } else if (strcmp(name, "{{ var.name }}") == 0 ) {
    {% endif %}
    *grid_id = {{ var.grid }};
  {% endfor %}
  } else {
    *grid_id = -1;
    return BMI_FAILURE;
  }
  return BMI_SUCCESS;
}

static int get_var_type(void *self, const char *name, char *vtype) {
  {% for var in vars %}
    {% if loop.first %}
  if (strcmp(name, "{{ var.name }}") == 0 ) {
    {% else %}
  } else if (strcmp(name, "{{ var.name }}") == 0 ) {
    {% endif %}
    strncpy(vtype, "{{ var.type }}", BMI_MAX_UNITS_NAME);
  {% endfor %}
  } else {
    *vtype = '\0';
    return BMI_FAILURE;
  }
  return BMI_SUCCESS;
}

static int get_var_units(void *self, const char *name, char *units) {
  {% for var in vars %}
    {% if loop.first %}
  if (strcmp(name, "{{ var.name }}") == 0 ) {
    {% else %}
  } else if (strcmp(name, "{{ var.name }}") == 0 ) {
    {% endif %}
    strncpy(units, "{{ var.units }}", BMI_MAX_UNITS_NAME);
  {% endfor %}
  } else {
    *units = '\0';
    return BMI_FAILURE;
  }
  return BMI_SUCCESS;
}

static int get_var_itemsize(void *self, const char *name, int *itemsize) {
  {% for var in vars %}
    {% if loop.first %}
  if (strcmp(name, "{{ var.name }}") == 0 ) {
    {% else %}
  } else if (strcmp(name, "{{ var.name }}") == 0 ) {
    {% endif %}
    *itemsize = sizeof({{ var.type }});
  {% endfor %}
  } else {
    *itemsize = 0;
    return BMI_FAILURE;
  }
  return BMI_SUCCESS;
}

static int get_var_nbytes(void *self, const char *name, int *nbytes) {
  int id, size, itemsize;

  return_on_error(get_var_grid(self, name, &id));
  return_on_error(get_grid_size(self, id, &size));
  return_on_error(get_var_itemsize(self, name, &itemsize));

  *nbytes = itemsize * size;

  return BMI_SUCCESS;
}

static int get_value_ptr(void *self, const char *name, void **dest) {
  void *data = NULL;

  {% for var in vars %}
    {% if loop.first %}
  if (strcmp(name, "{{ var.name }}") == 0 ) {
    {% else %}
  } else if (strcmp(name, "{{ var.name }}") == 0 ) {
    {% endif %}
    data = (void*)NULL; // Implement this: Pointer to data.
  {% endfor %}
  } else {
    *dest = NULL;
    return BMI_FAILURE;
  }
  *dest = data;
  return BMI_SUCCESS;
}

static int get_value(void *self, const char *name, void *dest) {
  void *src = NULL;

  if (get_value_ptr(self, name, &src) == BMI_FAILURE) {
    return BMI_FAILURE;
  } else {
    int nbytes;
    return_on_error(get_var_nbytes(self, name, &nbytes));
    memcpy(dest, src, nbytes);
  }

  return BMI_SUCCESS;
}

static int set_value(void *self, const char *name, void *array) {
  void *dest = NULL;

  if (get_value_ptr(self, name, &dest) == BMI_FAILURE) {
    return BMI_FAILURE;
  } else {
    int nbytes = 0;
    return_on_error(get_var_nbytes(self, name, &nbytes));
    memcpy(dest, array, nbytes);
    return BMI_SUCCESS;
  }
}

BMI_Model *register_bmi_{{ name }}(BMI_Model *model) {
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

  model->get_var_grid = get_var_grid;
  model->get_var_type = get_var_type;
  model->get_var_units = get_var_units;
  model->get_var_nbytes = get_var_nbytes;
  model->get_current_time = get_current_time;
  model->get_start_time = get_start_time;
  model->get_end_time = get_end_time;
  model->get_time_units = get_time_units;
  model->get_time_step = get_time_step;

  model->get_value = get_value;
  model->get_value_ptr = get_value_ptr;

  model->set_value = set_value;
  model->set_value_ptr = NULL;

  model->get_grid_rank = get_grid_rank;
  model->get_grid_size = get_grid_size;
  model->get_grid_type = get_grid_type;
  model->get_grid_shape = get_grid_shape;
  model->get_grid_spacing = get_grid_spacing;
  model->get_grid_origin = get_grid_origin;

  model->get_grid_x = get_grid_x;
  model->get_grid_y = get_grid_y;
  model->get_grid_z = NULL;

  model->get_grid_connectivity = get_grid_connectivity;
  model->get_grid_offset = get_grid_offset;

  return model;
}
