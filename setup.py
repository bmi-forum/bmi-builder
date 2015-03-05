from setuptools import setup, find_packages

from codecs import open
from os import path

#from wmtexe.commands.configure import Configure
#from wmtexe.commands.install import Install


_HERE = path.abspath(path.dirname(__file__))


def read(*names, **kwds):
    return open(
        path.join(_HERE, *names),
        encoding=kwds.get('encoding', 'utf-8')
    ).read()


def find_version(*file_paths):
    import re

    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='bmibuilder',
    version=find_version("bmibuilder/__init__.py"),
    description='Create BMI templates.',
    long_description=read('README.md'),
    url='https://github.com/csdms/bmi-builder',

    author='Eric Hutton',
    author_email='hutton.eric@gmail.com',

    license='MIT',

    packages=['bmibuilder', 'bmibuilder.writers'],

    entry_points={
        'console_scripts': [
            'bmi-build=bmibuilder.build:main',
        ],
    },

    #cmdclass={
    #    'configure': Configure,
    #    'install': Install,
    #},
)
