#!/usr/bin/env python
import sys
import os
from setuptools import setup
from xchatbot import __version__ as version

with open('README.md', 'r') as f:
    README = f.read()

# 'setup.py publish' shortcut.
if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist bdist_wheel')
    os.system('twine upload dist/*')
    sys.exit()

setup(name='xchatbot',
      version=version,
      description='the Xtensible XMPP Chat Bot',
      long_description=README,
      long_description_content_type='text/markdown',
      author='Fabio Comuni',
      author_email='fabrixxm@gmail.com',
      url='https://git.sr.ht/~fabrixxm/xchatbot',
      py_modules=['xchatbot'],
      package_data={
          'dist': ['./echobot.rc.dist', './README.md', './LICENSE'],
      },
      install_requires=[
          'nbxmpp>=0.6.10,<0.7.0',
          'PyGObject>=3.30.0,<3.40.0',
      ],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Programming Language :: Python :: 3',
          'Topic :: Communications :: Chat',
      ]
)
