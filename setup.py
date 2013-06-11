from setuptools import setup, find_packages
import sys, os

version = '0.0.1'

setup(name='repopy',
      version=version,
      description="Collection of utilities to handle a repository of python packages",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='python repository pypi',
      author='bhodorog',
      author_email='bogdan.hodorog@3pillarglobal.com',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
