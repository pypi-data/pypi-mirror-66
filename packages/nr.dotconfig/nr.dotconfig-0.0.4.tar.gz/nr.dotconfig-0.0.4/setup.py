# automatically created by shore 0.0.9

import io
import re
import setuptools
import sys

with io.open('src/dotconfig.py', encoding='utf8') as fp:
  version = re.search(r"__version__\s*=\s*'(.*)'", fp.read()).group(1)

with io.open('README.md', encoding='utf8') as fp:
  long_description = fp.read()

requirements = ['click >=7.1.1,<8.0.0', 'nr.config >=0.0.2,<0.1.0', 'nr.databind.core >=0.0.8,<0.1.0', 'nr.databind.json >=0.0.7,<0.1.0', 'PyYAML >=5.3.0,<5.4.0', 'requests >=2.23.0,<3.0.0']

setuptools.setup(
  name = 'nr.dotconfig',
  version = version,
  author = 'Niklas Rosenstein',
  author_email = 'rosensteinniklas@gmail.com',
  description = 'A single configuration file for .bash_profile and .gitconfig.',
  long_description = long_description,
  long_description_content_type = 'text/markdown',
  url = 'https://git.niklasrosenstein.com/NiklasRosenstein/dotconfig',
  license = 'MIT',
  py_modules = ['dotconfig'],
  package_dir = {'': 'src'},
  include_package_data = True,
  install_requires = requirements,
  extras_require = {},
  tests_require = [],
  python_requires = None, # TODO: '>=3.4,<4.0.0',
  data_files = [],
  entry_points = {
    'console_scripts': [
      'dotconfig = dotconfig:cli',
    ]
  },
  cmdclass = {},
  keywords = [],
  classifiers = [],
)
