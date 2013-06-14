from setuptools import setup, find_packages

version = '0.0.1'

setup(name='repoq',
      version=version,
      description="Collection of utilities to query a repository of python packages",
      long_description="""\
""",
      classifiers=[
          "Development Status :: 3 - Alpha",
          "Environment :: Console",
          "Intended Audience :: Developers",
          "Intended Audience :: System Administrators",
          "Topic :: System :: Software Distribution",
      ], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='python repository pypi',
      author='bhodorog',
      author_email='bogdan.hodorog@3pillarglobal.com',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          "boto",
      ],
      entry_points={
          "console_scripts": [
              "repoq = repoq.handlers:main",
          ],
      },
      )
