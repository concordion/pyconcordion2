from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='pyconcordion2',
      version=version,
      description="Concordion Python Port",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='concordion acceptance-test',
      author='John Jiang',
      author_email='',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'lxml', 'pyparsing',# -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
