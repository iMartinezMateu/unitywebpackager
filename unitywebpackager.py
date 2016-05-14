#
# Copyright (c) 2016 Iván Martínez Mateu
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
#

import argparse

import constants
import unitywebpackager_ops


class UnityWebPackager:
    @staticmethod
    def main():
        """ Function that initializes the argument parser, so the user can give input data to the script using
            command line arguments"""
        parser = argparse.ArgumentParser(prog=constants.CONST_PROGRAM_NAME,
                                         description='This tool converts a WebGL game built with Unity3D into a binary '
                                                     'executable compatible with Windows, OS X, GNU/Linux and '
                                                     'ARM devices like the Raspberry Pi.')
        parser.add_argument('--version', action='version',
                            version=constants.CONST_PROGRAM_NAME + ' ' + constants.CONST_PROGRAM_VERSION)
        subparsers = parser.add_subparsers()
        parser_convert = subparsers.add_parser('package',
                                               help='Package a WebGL game built with Unity3D into a binary')
        parser_convert.add_argument('--build-dir', dest='build_dir', required=True,
                                    help='the directory where the game was exported to WebGL using Unity3D')
        parser_convert.add_argument('--output-dir', dest='output_dir', required=True,
                                    help='the directory where the binary executable source is going to be stored')
        parser_convert.add_argument('--development', dest='development', required=True, choices=['true', 'false'],
                                    help='configure ' + constants.CONST_PROGRAM_NAME +
                                         ' to convert a development (true) or release (false) Unity 3D WebGL build.')
        parser_convert.set_defaults(func=package_game)
        args = parser.parse_args()
        args.func(args)


def package_game(args):
    """ Function that initializes the WebGL game build packaging process """
    build_dir = args.build_dir
    output_dir = args.output_dir
    development = args.development
    unitywebpackager_ops.print_welcome()
    if unitywebpackager_ops.analyze_directories(build_dir, output_dir, development):
        unitywebpackager_ops.copy_files(build_dir, output_dir, development)
        unitywebpackager_ops.create_html(output_dir, development)
        unitywebpackager_ops.create_player_script(output_dir)
        unitywebpackager_ops.print_final_instructions(output_dir)


if __name__ == '__main__':
    UnityWebPackager().main()
