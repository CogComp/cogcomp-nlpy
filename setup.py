from setuptools import setup, find_packages

classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Science/Research',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: POSIX',
    'Operating System :: Unix',
    'Operating System :: MacOS',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Topic :: Scientific/Engineering'
]

setup(name='sioux',
      version='0.3.dev0',
      description='',
      url='https://github.com/IllinoisCogComp/sioux',
      author='Cognitive Computing Group',
      author_email='',
      license='Research and Academic Use License',
      packages= find_packages(exclude=['tests.*','tests']),
      install_requires = ['requests','configparser'],
      classifiers=classifiers,
      data_files=[('config', ['config/pipeline.cfg'])],
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)
