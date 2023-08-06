# automatically created by shore 0.0.22

import io
import re
import setuptools
import sys

with io.open('src/nr/powerline/__init__.py', encoding='utf8') as fp:
  version = re.search(r"__version__\s*=\s*'(.*)'", fp.read()).group(1)

with io.open('README.md', encoding='utf8') as fp:
  long_description = fp.read()

requirements = ['nr.parsing.core >=0.0.1,<0.1.0', 'nr.sumtype >=0.0.3,<0.1.0', 'termcolor >=1.1.0,<2.0.0']

setuptools.setup(
  name = 'nr.powerline',
  version = version,
  author = 'Niklas Rosenstein',
  author_email = 'rosensteinniklas@gmail.com',
  description = 'Package description here.',
  long_description = long_description,
  long_description_content_type = 'text/markdown',
  url = None,
  license = 'MIT',
  packages = setuptools.find_packages('src', ['test', 'test.*', 'docs', 'docs.*']),
  package_dir = {'': 'src'},
  include_package_data = True,
  install_requires = requirements,
  extras_require = {},
  tests_require = [],
  python_requires = None, # TODO: '>=3.4,<4.0.0',
  data_files = [],
  entry_points = {
    'console_scripts': [
      'nr-powerline = nr.powerline.main:main',
    ],
    'nr.powerline.plugins': [
      'c = nr.powerline.plugins.characters:CharactersPlugin',
      'git = nr.powerline.plugins.git:GitPlugin',
      'session = nr.powerline.plugins.session:SessionPlugin',
      'time = nr.powerline.plugins.time:TimePlugin',
    ]
  },
  cmdclass = {},
  keywords = [],
  classifiers = [],
)
