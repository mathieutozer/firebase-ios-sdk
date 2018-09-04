#! /usr/bin/env python

# Copyright 2018 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Generates and massages protocol buffer outputs.
"""

from __future__ import print_function

import sys

import argparse
import os
import os.path
import re
import shutil
import subprocess
import tarfile
import urllib2


COPYRIGHT_NOTICE = '''
/*
 * Copyright 2018 Google
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
'''.lstrip()


def main():
  parser = argparse.ArgumentParser(
      description='Generates proto messages.')
  parser.add_argument(
      '--nanopb', action='store_true',
      help='Generates nanopb messages.')
  parser.add_argument(
      '--output-dir', '-d', default='.', dest='output_dir',
      help='Directory to write files; subdirectories will be created.')

  parser.add_argument(
      '--protoc', default='protoc',
      help='Location of the protoc executable')
  parser.add_argument(
      '--protoc-gen-nanopb', dest='protoc_gen_nanopb',
      help='Location of the nanopb generator executable')

  if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)
  args = parser.parse_args()

  root_dir = os.path.dirname(__file__)
  os.chdir(root_dir)

  nanopb_proto_files = collect_files('protos', '.proto')

  if args.nanopb:
    NanopbGenerator(args, nanopb_proto_files).run()


class NanopbGenerator(object):
  """Builds and runs the nanopb plugin to protoc."""

  def __init__(self, args, proto_files):
    self.args = args
    self.proto_files = proto_files

  def run(self):
    """Performs the action of the the generator."""

    nanopb_out = os.path.join(self.args.output_dir, 'nanopb')
    mkdir(nanopb_out)

    self.__run_generator(nanopb_out)

    sources = collect_files(nanopb_out, '.nanopb.h', '.nanopb.c')
    post_process_files(sources, add_copyright, nanopb_rename_delete)

  def __run_generator(self, out_dir):
    """Invokes protoc using the nanopb plugin."""
    cmd = [self.args.protoc, '-I', 'protos']

    gen = self.args.protoc_gen_nanopb
    if gen is not None:
      proto_dir = os.path.join(os.path.dirname(gen), 'proto')
      if os.path.isdir(proto_dir):
        cmd.extend(['-I', proto_dir])

      cmd.append('--plugin=protoc-gen-nanopb=%s' % gen)

    nanopb_flags = ' '.join([
        '--extension=.nanopb',
        '--options-file=protos/%s.options',
    ])
    cmd.append('--nanopb_out=%s:%s' % (nanopb_flags, out_dir))

    cmd.extend(self.proto_files)

    subprocess.check_call(cmd)


def post_process_files(filenames, *processors):
  for filename in filenames:
    lines = []
    with open(filename, 'r') as fd:
      lines = fd.readlines()

    for processor in processors:
      lines = processor(lines)

    write_file(filename, lines)


def write_file(filename, lines):
  with open(filename, 'w') as fd:
    fd.write(''.join(lines))


def add_copyright(lines):
  """Adds a copyright notice to the lines."""
  result = [COPYRIGHT_NOTICE, '\n']
  result.extend(lines)
  return result


def nanopb_rename_delete(lines):
  """Renames a delete symbol to delete_.

  If a proto uses a field named 'delete', nanopb happily uses that in the
  message definition. Works fine for C; not so much for C++.

  Args:
    lines: The lines to fix.

  Returns:
    The lines, fixed.
  """
  delete_keyword = re.compile(r'\bdelete\b')
  return [delete_keyword.sub('delete_', line) for line in lines]


def collect_files(root_dir, *extensions):
  """Finds files with the given extensions in the root_dir."""
  result = []
  for root, dirs, files in os.walk(root_dir):
    del dirs
    for basename in files:
      for ext in extensions:
        if basename.endswith(ext):
          filename = os.path.join(root, basename)
          result.append(filename)
  return result


def mkdir(dirname):
  if not os.path.isdir(dirname):
    os.makedirs(dirname)


if __name__ == '__main__':
  main()
