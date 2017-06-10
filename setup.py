import os
from setuptools import setup, find_packages

# Utility method to read the README.rst file.
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

import version
VERSION = version.__version__

CLASSIFIERS = [
    'Development Status :: 3 - Alpha', 'Intended Audience :: Science/Research',
    'Operating System :: Microsoft :: Windows', 'Operating System :: POSIX',
    'Operating System :: Unix', 'Operating System :: MacOS',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6', 'Topic :: Scientific/Engineering'
]

setup(
    name='ccg_nlpy',
    version=VERSION,
    description=("Light-weight NLP annotators"),
    long_description=read('README.rst'),
    url='https://github.com/IllinoisCogComp/ccg_nlpy',
    author='Cognitive Computation Group',
    author_email='mssammon@illinois.edu',
    license='Research and Academic Use License',
    keywords="NLP, natural language processing",
    packages=find_packages(exclude=['tests.*', 'tests']),
    install_requires=['configparser', 'Cython', 'pyjnius', 'protobuf', 'requests', 'six'],
    package_data={'ccg_nlpy': ['config/*.cfg']},
    classifiers=CLASSIFIERS,
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'mock'],
    zip_safe=False)
