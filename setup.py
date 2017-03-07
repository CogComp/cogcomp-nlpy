from setuptools import setup, find_packages

setup(name='cogcomp_python_utils',
      version='0.1.dev0',
      description='',
      url='https://github.com/IllinoisCogComp/python-utils',
      author='Cognitive Computing Group',
      author_email='',
      license='Research and Academic Use License',
      packages= find_packages(exclude=['tests.*','tests']),
      install_requires = ['requests','configparser'],
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)
