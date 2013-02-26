from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='pyconcordion2',
      version=version,
      description="Concordion Python Port",
      long_description="""\
""",
      # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=["Topic :: Software Development :: Testing",
                   "License :: OSI Approved :: MIT License"],
      keywords='concordion acceptance-test',
      author='John Jiang',
      author_email='',
      url='https://github.com/johnjiang/pyconcordion2',
      license='MIT License',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      package_data={
          'pyconcordion2': [
              'resources/*/*.css',
              'resources/*/*.js',
          ],
      },
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'lxml', 'pyparsing', # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
)
