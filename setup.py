import os
from setuptools import setup, find_packages

from pip.req import parse_requirements

current_dir = os.path.dirname(os.path.realpath(__file__))
requirements_file = 'requirements.txt'
requirements_file_path = os.path.join(current_dir, requirements_file)

install_reqs = parse_requirements(requirements_file_path)
reqs = [str(ir.req) for ir in install_reqs]

setup(name='pyconcordion2',
      version='0.15.0',
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
      install_requires=reqs,
      tests_require=['mock'],
      # test_suite='runtests.get_suite',
      entry_points="""
      # -*- Entry points: -*-
      """,
)
