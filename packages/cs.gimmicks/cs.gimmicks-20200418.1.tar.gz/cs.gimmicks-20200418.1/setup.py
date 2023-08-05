#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.gimmicks',
  description = 'Gimmicks and hacks to make some of my other modules more robust and less demanding of others.',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20200418.1',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'Topic :: Software Development :: Libraries :: Python Modules', 'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)'],
  include_package_data = True,
  install_requires = [],
  keywords = ['python2', 'python3'],
  license = 'GNU General Public License v3 or later (GPLv3+)',
  long_description = '*Latest release 20200418.1*:\nInitial release with logging call stubs.\n\nGimmicks and hacks to make some of my other modules more robust and\nless demanding of others.\n\n## Function `debug(*a, **kw)`\n\n# Wrapper for `debug()` which does a deferred import.\n\n## Function `error(*a, **kw)`\n\n# Wrapper for `error()` which does a deferred import.\n\n## Function `exception(*a, **kw)`\n\n# Wrapper for `exception()` which does a deferred import.\n\n## Function `info(*a, **kw)`\n\n# Wrapper for `info()` which does a deferred import.\n\n## Function `log(*a, **kw)`\n\n# Wrapper for `log()` which does a deferred import.\n\n## Function `warning(*a, **kw)`\n\n# Wrapper for `warning()` which does a deferred import.\n\n\n\n# Release Log\n\n*Release 20200418.1*:\nInitial release with logging call stubs.',
  long_description_content_type = 'text/markdown',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.gimmicks'],
)
