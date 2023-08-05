#!/usr/bin/env python

# Copyright (c) 2020 Blizzard Entertainment
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import subprocess


def game_version():
    return '2.50.0.79155'


def read_command_output(cmd):
    lines = []
    handle = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    while True:
        line = handle.stdout.readline()
        if line != '':
            lines.append(line.rstrip())
        else:
            break
    return lines


def git_commit_hash():
    git_version_cmd = ['git', 'rev-parse', 'HEAD']
    lines = read_command_output(git_version_cmd)
    if len(lines) == 0 or len(lines > 1):
        raise Exception("invalid output '{}' from '{}'".format(
            '\\n'.join(lines),
            ' '.join(git_version_cmd)))

    git_commit_hash = (''.join(lines))[0:8]

    return git_commit_hash


if __name__ == '__main__':
    print("Game version: {}".format(game_version()))
    print("Git commit hash: {}".format(git_commit_hash()))
