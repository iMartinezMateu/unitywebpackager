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

import logging
import os
import shutil

import progressbar

import constants


def print_welcome():
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info('==============================================================================')
    logging.info('Welcome to ' + constants.CONST_PROGRAM_NAME + '!')
    logging.info('Version: ' + constants.CONST_PROGRAM_VERSION)
    logging.info('Repository URL: ' + constants.CONST_PROGRAM_REPO_URL)
    logging.info('Author: ' + constants.CONST_PROGRAM_AUTHOR)
    logging.info('<Ctrl-C> to stop.')
    logging.info('==============================================================================')


def analyze_directories(build_dir, output_dir, development):
    bar = progressbar.ProgressBar()
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info('Analysing build directory ' + build_dir)
    if not os.path.isdir(build_dir):
        logging.error('Build directory does not exist at ' + build_dir)
        return
    bar.update(16)
    for files in os.walk(build_dir):
        if not files:
            logging.error('Build directory is empty.')
            return
    bar.update(32)
    if development == 'false':
        if not os.path.isdir(os.path.join(build_dir, 'Release')):
            logging.error('Release subdirectory does not exist at ' + build_dir)
            return
        bar.update(48)
        for files in os.walk(os.path.join(build_dir, 'Release')):
            if not files:
                logging.error('Release subdirectory is empty.')
                return
        bar.update(64)
    if development == 'true':
        if not os.path.isdir(os.path.join(build_dir, 'Development')):
            logging.error('Development subdirectory does not exist at ' + build_dir)
            return
        bar.update(48)
        for files in os.walk(os.path.join(build_dir, 'Development')):
            if not files:
                logging.error('Development subdirectory is empty.')
                return
        bar.update(64)
    if not os.path.isfile(os.path.join(build_dir, 'index.html')):
        logging.error('Index file does not exist at ' + build_dir)
        return
    bar.update(90)
    if os.stat(os.path.join(build_dir, 'index.html')).st_size == 0:
        logging.error('Index file is empty.')
        return
    bar.update(100)
    bar = progressbar.ProgressBar()
    logging.info('Analysing output directory ' + output_dir)
    bar.update(33)
    if not os.path.isdir(output_dir):
        logging.error('Output directory does not exist at ' + output_dir)
        return
    bar.update(66)
    for file in os.listdir(output_dir):
        file_path = os.path.join(output_dir, file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(e)
    bar.update(100)
    return True


def copy_files(build_dir, output_dir, development):
    bar = progressbar.ProgressBar()
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info('Copying game build assets to ' + output_dir)
    if development == 'true':
        shutil.copytree(os.path.join(build_dir, 'Development'), os.path.join(output_dir, 'Development'))
        bar.update(50)
    if development == 'false':
        shutil.copytree(os.path.join(build_dir, 'Release'), os.path.join(output_dir, 'Release'))
        bar.update(50)
    bar.update(100)


def create_html(output_dir, development):
    bar = progressbar.ProgressBar()
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info('Creating index HTML file.')
    with open(os.path.join(output_dir, 'index.html'), 'w') as out:
        bar.update(4)
        out.write('<!doctype html>\n');
        bar.update(8)
        out.write('<html lang="en-us">\n');
        bar.update(12)
        out.write('<head>\n');
        bar.update(16)
        out.write('<meta charset="utf-8">\n');
        bar.update(20)
        out.write('<meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n');
        bar.update(24)
        out.write('<title>Unity Web Packager</title>\n');
        bar.update(28)
        out.write('</head>\n');
        bar.update(32)
        out.write('<body>\n');
        bar.update(36)
        out.write('<canvas style=\'height: 100vh; width: 100vw; display:block;\' class="emscripten" id="canvas" '
                  'oncontextmenu="event.preventDefault()" </canvas>\n');
        bar.update(40)
        out.write('<script type=\'text/javascript\'>\n');
        bar.update(44)
        out.write('var Module = {\n');
        bar.update(48)
        out.write('TOTAL_MEMORY: 268435456,\n');
        bar.update(52)
        out.write('errorhandler: null,\n');
        bar.update(56)
        out.write('compatibilitycheck: null,\n');
        bar.update(60)
        if development == 'true':
            for file in os.listdir(os.path.join(output_dir, 'Development')):
                if file.endswith('.datagz'):
                    out.write('dataUrl: "Development/' + file.replace('.datagz', '.data') + '",\n');
                    bar.update(64)
                if file.endswith('.jsgz') and file is not 'UnityLoader.js':
                    out.write('codeUrl: "Development/' + file.replace('.jsgz', '.js') + '",\n');
                    bar.update(68)
                if file.endswith('.memgz'):
                    out.write('memUrl: "Development/' + file.replace('.memgz', '.mem') + '",\n');
                    bar.update(72)
        if development == 'false':
            for file in os.listdir(os.path.join(output_dir, 'Release')):
                if file.endswith('.datagz'):
                    out.write('dataUrl: "Release/' + file.replace('.datagz', '.data') + '",\n');
                    bar.update(64)
                if file.endswith('.jsgz'):
                    out.write('codeUrl: "Release/' + file.replace('.jsgz', '.js') + '",\n');
                    bar.update(68)
                if file.endswith('.memgz'):
                    out.write('memUrl: "Release/' + file.replace('.memgz', '.mem') + '",\n');
                    bar.update(72)
        out.write('};</script>\n');
        bar.update(76)
        if development == 'true':
            out.write('<script src="Development/UnityLoader.js"></script>\n');
            bar.update(80)
        if development == 'false':
            out.write('<script src="Release/UnityLoader.js"></script>\n');
            bar.update(80)
        out.write('</body>\n');
        bar.update(84)
        out.write('</html>\n');
        bar.update(88)
    bar.update(100)


def create_player_script(output_dir):
    bar = progressbar.ProgressBar()
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info('Creating executable player script file.')
    with open(os.path.join(output_dir, 'player.py'), 'w') as out:
        bar.update(2)
        out.write('#\n')
        bar.update(4)
        out.write('# Copyright (c) 2016 Ivan Martinez Mateu\n')
        bar.update(6)
        out.write('#\n')
        bar.update(8)
        out.write('# Permission is hereby granted, free of charge, to any person obtaining a copy\n')
        bar.update(10)
        out.write('# of this software and associated documentation files (the "Software"), to deal\n')
        bar.update(12)
        out.write('# in the Software without restriction, including without limitation the rights\n')
        bar.update(14)
        out.write('# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n')
        bar.update(16)
        out.write('# copies of the Software, and to permit persons to whom the Software is\n')
        bar.update(18)
        out.write('# furnished to do so, subject to the following conditions:\n')
        bar.update(20)
        out.write('#\n')
        bar.update(22)
        out.write('# The above copyright notice and this permission notice shall be included in\n')
        bar.update(24)
        out.write('# all copies or substantial portions of the Software.\n')
        bar.update(26)
        out.write('#\n')
        bar.update(28)
        out.write('# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n')
        bar.update(30)
        out.write('# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n')
        bar.update(32)
        out.write('# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n')
        bar.update(34)
        out.write('# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n')
        bar.update(36)
        out.write('# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n')
        bar.update(38)
        out.write('# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN\n')
        bar.update(40)
        out.write('# THE SOFTWARE.\n')
        bar.update(42)
        out.write('#\n')
        bar.update(44)
        out.write('import os\n')
        bar.update(46)
        out.write('import sys\n\n')
        bar.update(48)
        out.write('import PyQt5\n')
        bar.update(50)
        out.write('from PyQt5.QtCore import *\n')
        bar.update(52)
        out.write('from PyQt5.QtWidgets import *\n')
        bar.update(54)
        out.write('from PyQt5.QtGui import *\n')
        bar.update(56)
        out.write('from PyQt5.QtWebKitWidgets import *\n')
        bar.update(58)
        out.write('class Player(QWebView):\n\n')
        bar.update(60)
        out.write('\tdef __init__(self, parent=None):\n')
        bar.update(62)
        out.write('\t\tQWebView.__init__(self, parent)\n\n')
        bar.update(64)
        out.write('\tdef contextMenuEvent(self, event):\n')
        bar.update(66)
        out.write('\t\tpass\n\n')
        bar.update(68)
        out.write('app = QApplication(sys.argv)\n')
        bar.update(70)
        out.write('view = QWebView()\n')
        bar.update(72)
        out.write(
            'view.load(QUrl.fromLocalFile(os.path.abspath(os.path.join(os.path.dirname(__file__), "index.html"))))\n')
        bar.update(74)
        out.write('view.show()\n')
        bar.update(76)
        out.write('app.exec_()\n')
        bar.update(78)
    bar.update(100)


def print_final_instructions(output_dir):
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info(
        constants.CONST_PROGRAM_NAME + ' has exported successfully the packaged game source at ' + output_dir + '.')
    logging.info('From here, use a program that freezes (packages) Python programs into stand-alone executables.')
    logging.info(
        'You can use PyInstaller (http://www.pyinstaller.org) but you will need to freeze the packaged game source in '
        'the deployment machine (for example, if you want to deploy your game to Raspberry Pi, then execute '
        'PyInstaller in a Raspberry Pi and freeze/package the output generated by this program in the '
        'following directory: ' + output_dir + '. You will need to have installed Qt 5 and PyQt5 in your system in '
                                               'order to compile and distribute the game package.')
