#include <stdio.h>
#include <string.h>

{{ includes }}

#define VERBOSE (false)
#define DEBUG

#if defined (DEBUG)
# define CHECK_OR_THROW(assertion, err) { if (!(assertion)) throw err; }
#else
# define CHECK_OR_THROW(assertion, err) { }
#endif


void bmi::Model::Initialize (const char *file) {
  // Implement this: Initialize Model class
  return;
}

void bmi::Model::Update () {
  // Implement this: Update one time step.
  return;
}

void bmi::Model::UpdateUntil (double t) {
  // Implement this: Update until some time.
  return;
}

void bmi::Model::Finalize () {
  // Implement this: Clean up.
  return;
}

void bmi::Model::GetComponentName (char * const name) {
  strcpy (name, "{{ name }}");
}

int bmi::Model::GetInputVarNameCount (void) {
  return this->input_var_name_count;
}

int bmi::Model::GetOutputVarNameCount (void) {
  return this->output_var_name_count;
}

void bmi::Model::GetInputVarNames (char * const * const names) {
  for (int i=0; i<this->input_var_name_count; i++) {
    strcpy (names[i], input_var_names[i]);
  }
}

void bmi::Model::GetOutputVarNames (char * const * const names) {
  for (int i=0; i<this->output_var_name_count; i++) {
    strcpy (names[i], output_var_names[i]);
  }
}

int bmi::Model::GetVarType (const char * var_name, char * vtype) {
  {% for var in vars %}
    {% if loop.first %}
  if (strcmp(name, "{{ var.name }}") == 0 ) {
    {% else %}
  } else if (strcmp(name, "{{ var.name }}") == 0 ) {
    {% endif %}
    strncpy(vtype, "{{ var.type }}", BMI_MAX_UNITS_NAME);
  {% endfor %}
  } else {
    throw bmi::BAD_VAR_NAME;
  }
}

void bmi::Model::GetVarUnits (const char * var_name,
                              char * const units) {
  {% for var in vars %}
    {% if loop.first %}
  if (strcmp(name, "{{ var.name }}") == 0 ) {
    {% else %}
  } else if (strcmp(name, "{{ var.name }}") == 0 ) {
    {% endif %}
    strncpy(units, "{{ var.units }}", BMI_MAX_UNITS_NAME);
  {% endfor %}
  } else {
    throw bmi::BAD_VAR_NAME;
  }
}

int bmi::Model::GetVarGrid (const char * var_name) {
  int grid_id;

  {% for var in vars %}
    {% if loop.first %}
  if (strcmp(name, "{{ var.name }}") == 0 ) {
    {% else %}
  } else if (strcmp(name, "{{ var.name }}") == 0 ) {
    {% endif %}
    grid_id = {{ var.grid }};
  {% endfor %}
  } else {
    throw bmi::BAD_VAR_NAME;
  }
  return grid_id;
}

int bmi::Model::GetGridRank (const char * var_name) {
  int rank;

  {% for grid in grids %}
    {% if loop.first %}
  if (grid_id == {{ grid.id }}) {
   {% else %}
  } else if (grid_id == {{ grid.id }}) {
    {% endif %}
    rank = {{ grid.rank }};
  {% endfor %}
  } else {
    throw bmi::BAD_VAR_NAME;
  }
  return rank;
}

int bmi::Model::GetGridSize (const char * var_name) {
  int size = 0;
  //Implement this: The number of elements in the grid.
  return size;
}

double bmi::Model::GetStartTime () {
  return {{ time.start }};
}

double bmi::Model::GetCurrentTime () {
  double now = 0.;
  // Implement this: The current model time.
  return now;
}

double bmi::Model::GetEndTime () {
  double stop = 0.;
  // Implement this: The current model stop time.
  return stop;
}

int bmi::Model::GetVarItemsize(const char * name) {
  int itemsize = 0;

  {% for var in vars %}
    {% if loop.first %}
  if (strcmp(name, "{{ var.name }}") == 0 ) {
    {% else %}
  } else if (strcmp(name, "{{ var.name }}") == 0 ) {
    {% endif %}
    itemsize = sizeof({{ var.type }});
  {% endfor %}
  } else {
    throw bmi::BAD_VAR_NAME;
  }
  return itemsize;
}

int bmi::Model::GetVarNbytes(const char * name) {
  const int itemsize = GetVarItemsize(name);
  const int id = GetVarGrid(name);
  const int size = GetGridSize(id);

  return itemsize * size;
}

void *bmi::Model::GetValuePtr(const char * var_name) {
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
    throw bmi::BAD_VAR_NAME;
  }
  return data;
}

void bmi::Model::GetValue(const char * var_name, void * const dest) {
  void *src = NULL;

  src = GetValuePtr(var_name);
  if (src) {
    int nbytes = GetVarNbytes(name);
    memcpy(dest, src, nbytes);
  } else {
    throw bmi::FAILURE;
  }
}


void bmi::Model::SetValue (const char * var_name, double *vals) {
  void *dest = NULL;

  dest = GetValuePtr(name);
  if (dest) {
    int nbytes = GetVarNbytes(name);
    memcpy(dest, array, nbytes);
  } else {
    throw bmi::FAILURE;
  }
}

void bmi::Model::GetGridX (const int grid_id, double * const x) {
  {% for grid in grids %}
    {% if loop.first %}
  if (grid_id == {{ grid.id }}) {
    {% else %}
  } else if (grid_id == {{ grid.id }}) {
    {% endif %}
    // Implement this: x for this grid.
  {% endfor %}
  } else {
    throw bmi:FAILURE;
  }
}

void bmi::Model::GetGridY (const int grid_id, double * const y) {
  {% for grid in grids %}
    {% if loop.first %}
  if (grid_id == {{ grid.id }}) {
    {% else %}
  } else if (grid_id == {{ grid.id }}) {
    {% endif %}
    // Implement this: y for this grid.
  {% endfor %}
  } else {
    throw bmi:FAILURE;
  }
}

void bmi::Model::GetGridConnectivity (const int grid_id, int * connectivity) {
  {% for grid in grids %}
    {% if loop.first %}
  if (grid_id == {{ grid.id }}) {
    {% else %}
  } else if (grid_id == {{ grid.id }}) {
    {% endif %}
    // Implement this: connectivity for this grid.
  {% endfor %}
  } else {
    throw bmi:FAILURE;
  }
}

void bmi::Model::GetGridOffset (const int grid_id, int * const offset) {
  {% for grid in grids %}
    {% if loop.first %}
  if (grid_id == {{ grid.id }}) {
    {% else %}
  } else if (grid_id == {{ grid.id }}) {
    {% endif %}
    // Implement this: connectivity for this grid.
  {% endfor %}
  } else {
    throw bmi:FAILURE;
  }
}

void bmi::Model::GetGridType (const char * var_name, const char *gtype) {
  {% for grid in grids %}
    {% if loop.first %}
  if (grid_id == {{ grid.id }}) {
    {% else %}
  } else if (grid_id == {{ grid.id }}) {
    {% endif %}
    strncpy(gtype, "{{ grid.type }}", 2048);
  {% endfor %}
  } else {
    throw bmi::FAILURE;
  }
}

bool bmi::Model::HasInputVar (const char * var_name) {
  for (int i=0; i<this->input_var_name_count; i++) {
    if (strcmp (input_var_names[i], var_name) == 0)
      return true;
  }
  return false;
}

bool bmi::Model::HasOutputVar (const char * var_name) {
  for (int i=0; i<this->output_var_name_count; i++) {
    if (strcmp (output_var_names[i], var_name) == 0)
      return true;
  }
  return false;
}

void bmi::Model::SetInputVarNames (const char **names) {
  if (input_var_names) {
    for (int i=0; i<input_var_name_count; ++i)
      free (input_var_names[i]);
    delete input_var_names;
  }
  input_var_name_count = 0;

  if (names) {
    for (const char **name=names; *name; ++name)
      ++input_var_name_count;

    input_var_names = new char*[input_var_name_count];
    for (int i=0; i<input_var_name_count; ++i)
      input_var_names[i] = strdup (names[i]);
  }
  else
    input_var_names = NULL;
}

void bmi::Model::SetOutputVarNames (const char **names) {
  if (output_var_names) {
    for (int i=0; i<output_var_name_count; ++i)
      free (output_var_names[i]);
    delete output_var_names;
  }
  output_var_name_count = 0;

  if (names) {
    for (const char **name=names; *name; ++name)
      ++output_var_name_count;

    output_var_names = new char*[output_var_name_count];
    for (int i=0; i<output_var_name_count; ++i)
      output_var_names[i] = strdup (names[i]);
  }
  else
    output_var_names = NULL;
}
