# The MIT License (MIT)
#
# Copyright (c) 2020 Niklas Rosenstein
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from nr.databind.core import Field, FieldName, ObjectMapper, Remainder, Struct
from nr.databind.json import JsonModule
from yaml import safe_load as load_yaml
from typing import TextIO, Union
import click
import os
import nr.config
import requests
import sys

__author__ = 'Niklas Rosenstein <rosensteinniklas@gmail.com>'
__version__ = '0.0.4'

MAPPER = ObjectMapper(JsonModule())


class ProfileConfig(Struct):
  environment = Field(dict(value_type=([str], str)), default=dict)
  aliases = Field(dict(value_type=str), default=dict)
  blocks = Field(dict(value_type=str), default=dict)

  def render(self, fp: TextIO):
    for key, value in self.environment.items():
      if isinstance(value, list):
        value = os.pathsep.join(value)
      fp.write('export {}="{}"\n'.format(key, value))
    fp.write('\n')
    for key, value in self.aliases.items():
      fp.write('alias {}="{}"\n'.format(key, value))
    fp.write('\n')
    for value in self.blocks.values():
      fp.write(value)
      fp.write('\n')


class GitConfig(Struct):
  fields = Field(dict(value_type=dict(value_type=str)), Remainder())

  def render(self, fp: TextIO):
    for section, values in self.fields.items():
      fp.write('[{}]\n'.format(section))
      for key, value in values.items():
        fp.write('  {} = "{}"\n'.format(key, value))


class DotfileConfig(Struct):
  base = Field(str, default=None)
  profile = Field(ProfileConfig, default=None)
  gitconfig = Field(GitConfig, default=None)


class DotfileConfigPreprocessing(Struct):
  filename = Field(str, default=None, hidden=True)
  base = Field(str, default=None)
  data = Field(dict, Remainder())

  def get(self) -> DotfileConfig:
    return MAPPER.deserialize(self.data, DotfileConfig, filename=self.filename)


def load_config(config: Union[str, TextIO]) -> DotfileConfigPreprocessing:
  """
  Loads a dotfile config, recursively if need be.
  """

  if isinstance(config, str):
    if config.startswith('https://') or config.startswith('http://'):
      response = requests.get(config, stream=True)
      response.raise_for_status()
      config_data = load_yaml(response.raw)
    else:
      if config.startswith('file://'):
        config = config[7:]
      with open(config) as fp:
        config_data = load_yaml(fp)
  else:
    config_data = load_yaml(config)

  filename = config if isinstance(config, str) else getattr(config, 'name', None)
  config = MAPPER.deserialize(config_data, DotfileConfigPreprocessing, filename=filename)
  config.filename = filename

  if config.base:
    base = load_config(config.base)
    plugins = [nr.config.Vars({'base': base.data}, safe=True)]
    config.data = nr.config.process_config(config.data, plugins)
    config.data = nr.config.merge_config(base.data, config.data)

  return config


@click.command()
@click.argument('config', type=click.File('r'))
@click.option('-f', '--file', type=click.Choice(['profile', 'gitconfig']))
@click.option('-u', '--update', is_flag=True)
def cli(config, file, update):
  config = load_config(config).get()

  if file == 'profile':
    config.profile.render(sys.stdout)
    return
  elif file == 'gitconfig':
    config.gitconfig.render(sys.stdout)
    return
  elif file:
    sys.exit('error: unexpected -f,--file: {!r}'.format(file))

  if update:
    if config.profile:
      filename = os.path.expanduser('~/.bash_profile')
      print('Writing', filename)
      with open(filename, 'w') as fp:
        config.profile.render(fp)
    if config.gitconfig:
      filename = os.path.expanduser('~/.gitconfig')
      print('Writing', filename)
      with open(filename, 'w') as fp:
        config.gitconfig.render(fp)
    return

  sys.exit('error: no operation specified')


if __name__ == '__main__':
  cli()
