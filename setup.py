import os
from setuptools import setup, find_packages

version = __import__('pyconcordion2').__version__

setup(name='pyconcordion2',
      version=version,
      description="Concordion Python Port",
      long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst'), 'rU').read(),
      # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=["Topic :: Software Development :: Testing",
                   "License :: OSI Approved :: Apache Software License"],
      keywords='concordion acceptance-test',
      author='John Jiang',
      author_email='johnjiang101@gmail.com',
      url='https://github.com/johnjiang/pyconcordion2',
      license='Apache Software License',
      packages=find_packages(),
      package_data={
          'pyconcordion2': [
              'resources/*.css',
              'resources/*.js',
          ],
      },
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'lxml', 'pyparsing', 'enum34'  # -*- Extra requirements: -*-
      ],
      tests_require=['mock'],
      # test_suite='runtests.get_suite',
      entry_points="""
      # -*- Entry points: -*-
      """,
)
