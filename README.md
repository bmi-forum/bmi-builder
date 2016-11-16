# bmi-builder
Autogenerate BMI code in C, C++, and Python.

## Installation
Clone and install with setuptools.

```bash
$ git clone https://github.com/bmi-forum/bmi-builder.git
$ cd bmi-builder
$ python setup.py install
```

Test the install.

```bash
$ bmi-build --help
usage: bmi-build [-h] [--language {c,cxx,python}] [--clobber] file

positional arguments:
  file                  YAML file
  
optional arguments:
  -h, --help            show this help message and exit
  --language {c,cxx,python}
                        BMI language
  --clobber             Overwrite any existing files.
```

## Use

Create a YAML file with
`name`, `language`, `grids`, `time`, and `exchange_items` attributes,
following this template:

```yaml
name: <str>
long_name: <str>
language: {c, c++, python}
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
```

and provide this file as the argument to `bmi-build`.

An example of building a Python BMI is given in the **examples** directory.
Run the example with

```bash
$ cd examples
$ bmi-build --language=python --clobber bmi_python.yaml
```

The result, **bmi_model.py**,
implements all the BMI methods for the model.
Some methods,
such as `initialize`, `update_frac`, and `finalize`,
are stubbed,
and require the developer 
to fill out the implementation details.
