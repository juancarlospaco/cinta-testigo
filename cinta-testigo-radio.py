#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#############################################################################
## This file may be used under the terms of the GNU General Public
## License version 2.0 or 3.0 as published by the Free Software Foundation
## and appearing in the file LICENSE.GPL included in the packaging of
## this file.  Please review the following information to ensure GNU
## General Public Licensing requirements will be met:
## http:#www.fsf.org/licensing/licenses/info/GPLv2.html and
## http:#www.gnu.org/copyleft/gpl.html.
##
## This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
## WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
#############################################################################

# If you hackin bro, read: http://pyalsaaudio.sourceforge.net/libalsaaudio.html

# metadata
' Cinta Testigo para Radios en Ubuntu '
__version__ = ' 0.8 '
__license__ = ' GPL '
__author__ = ' juancarlospaco '
__email__ = ' juancarlospaco@ubuntu.com '


# imports
import sys
from os import geteuid
from os import linesep
from os import statvfs
from os import getcwd
from os import mkdir
from os import path
from os import remove
from os import walk
from itertools import chain
from itertools import product
from shutil import make_archive
from random import randint
from subprocess import call
from subprocess import check_output as getoutput
from webbrowser import open_new_tab
from datetime import datetime
from string import punctuation

try:
    from PyQt4.QtCore import Qt
    from PyQt4.QtCore import QRect
    from PyQt4.QtCore import QTimer

    from PyQt4.QtGui import QMainWindow
    from PyQt4.QtGui import QLabel
    from PyQt4.QtGui import QProgressBar
    from PyQt4.QtGui import QIcon
    from PyQt4.QtGui import QAction
    from PyQt4.QtGui import QPushButton
    from PyQt4.QtGui import QComboBox
    from PyQt4.QtGui import QApplication
    from PyQt4.QtGui import QWidget
    from PyQt4.QtGui import QFont
    from PyQt4.QtGui import QVBoxLayout
    from PyQt4.QtGui import QLCDNumber
    from PyQt4.QtGui import QSlider
    from PyQt4.QtGui import QDial
    from PyQt4.QtGui import QFrame
    from PyQt4.QtGui import QCursor
    from PyQt4.QtGui import QDialogButtonBox
    from PyQt4.QtGui import QPalette
    from PyQt4.QtGui import QMessageBox
    from PyQt4.QtGui import QPainter
    from PyQt4.QtGui import QColor
    from PyQt4.QtGui import QDialog
    from PyQt4.QtGui import QColorDialog
    from PyQt4.QtGui import QLineEdit
    from PyQt4.QtGui import QPen
    from PyQt4.QtGui import QFileDialog
    from PyQt4.QtGui import QPixmap
except ImportError:
    exit(" ERROR: No Qt4 avaliable!\n (sudo apt-get install python-qt4)")

try:
    import alsaaudio
except ImportError:
    exit(' ERROR: AlsaAudio not found,(sudo apt-get install python-alsaaudio)')

try:
    import numpy
except ImportError:
    exit(' ERROR: NumPy not found !, ( sudo apt-get install python-numpy )')


print(('#' * 80))


# print program info
print((''.join((__doc__, ',v.', __version__, __license__, ',by ', __author__))))


# root check
if geteuid() == 0:
    exit(" ERROR: Do NOT Run as root!, NO ejecutar como root!\n bye noob...\n")
else:
    pass


print((' INFO: Starting ' + str(datetime.now())))


###############################################################################


class MyMainWindow(QMainWindow):
    ' Main Window '
    def __init__(self, parent=None):
        ' Initialize QWidget inside MyMainWindow '
        super(MyMainWindow, self).__init__(parent)
        QWidget.__init__(self)

        # Main Window initial StatusBar Message
        self.statusBar().showMessage(__doc__)

        # Main Window initial Geometry
        self.resize(640, 700)

        # Main Window initial Title
        self.setWindowTitle(__doc__)

        # Main Window Minimum Size
        self.setMinimumSize(640, 700)

        # Main Window Maximum Size
        self.setMaximumSize(800, 840)

        # Main Window initial ToolTip
        self.setToolTip(__doc__)

        # Main Window initial Font type
        self.setFont(QFont('Ubuntu Light', 10))

        # Set Window Icon, if find on filesystem or default to a STD one
        self.setWindowIcon(QIcon.fromTheme("face-devilish"))
        self.setStyleSheet('''
            QToolTip {
                border: 1px solid black;
                background-color: #ffa02f;
                padding: 1px;
                border-radius: 3px;
                opacity: 100;
            }

            QWidget {
                color: #b1b1b1;
                background-color: rgba(75, 75, 75, 200);
            }

            QWidget:item:hover {
                background-color: QLinearGradient(
                    x1: 0, y1: 0,
                    x2: 0, y2: 1,
                    stop: 0 #ffa02f,
                    stop: 1 #ca0619
                );
                color: #000000;
            }

            QWidget:item:selected {
                background-color: QLinearGradient(
                    x1: 0, y1: 0,
                    x2: 0, y2: 1,
                    stop: 0 #ffa02f,
                    stop: 1 #d7801a
                );
            }

            QMenuBar::item { background: transparent; }

            QMenuBar::item:selected {
                background: transparent;
                border: 1px solid #ffaa00;
            }

            QMenuBar::item:pressed {
                background: #444;
                border: 1px solid #000;
                background-color: QLinearGradient(
                    x1:0, y1:0,
                    x2:0, y2:1,
                    stop:1 #212121,
                    stop:0.4 #343434,
                    stop:0.2 #343434,
                    stop:0.1 #ffaa00
                );
                margin-bottom:-1px;
                padding-bottom:1px;
            }

            QMenu { border: 1px solid #000; }

            QMenu::item { padding: 2px 20px 2px 20px; }

            QMenu::item:selected { color: #000000; }

            QWidget:disabled {
                color: #404040;
            }

            QAbstractItemView {
                background-color: QLinearGradient(
                    x1: 0, y1: 0,
                    x2: 0, y2: 1,
                    stop: 0 #4d4d4d,
                    stop: 0.1 #646464,
                    stop: 1 #5d5d5d
                );
            }

            QWidget:focus {
                border: 2px solid QLinearGradient(
                    x1: 0, y1: 0,
                    x2: 0, y2: 1,
                    stop: 0 #ffa02f,
                    stop: 1 #d7801a
                );
            }

            QLineEdit {
                background-color: QLinearGradient(
                    x1: 0, y1: 0,
                    x2: 0, y2: 1,
                    stop: 0 #4d4d4d,
                    stop: 0 #646464,
                    stop: 1 #5d5d5d
                );
                padding: 1px;
                border-style: solid;
                border: 1px solid #1e1e1e;
                border-radius: 5;
            }

            QPushButton {
                color: #b1b1b1;
                background-color: QLinearGradient(
                    x1: 0, y1: 0,
                    x2: 0, y2: 1,
                    stop: 0 #565656,
                    stop: 0.1 #525252,
                    stop: 0.5 #4e4e4e,
                    stop: 0.9 #4a4a4a,
                    stop: 1 #464646
                );
                border-width: 1px;
                border-color: #1e1e1e;
                border-style: solid;
                border-radius: 6;
                padding: 3px;
                font-size: 12px;
                padding-left: 5px;
                padding-right: 5px;
            }

            QPushButton:pressed {
                background-color: QLinearGradient(
                    x1: 0, y1: 0,
                    x2: 0, y2: 1,
                    stop: 0 #2d2d2d,
                    stop: 0.1 #2b2b2b,
                    stop: 0.5 #292929,
                    stop: 0.9 #282828,
                    stop: 1 #252525
                );
            }

            QComboBox {
                selection-background-color: #ffaa00;
                background-color: QLinearGradient(
                    x1: 0, y1: 0,
                    x2: 0, y2: 1,
                    stop: 0 #565656,
                    stop: 0.1 #525252,
                    stop: 0.5 #4e4e4e,
                    stop: 0.9 #4a4a4a,
                    stop: 1 #464646
                );
                border-style: solid;
                border: 1px solid #1e1e1e;
                border-radius: 5;
            }

            QComboBox:hover,QPushButton:hover {
                border: 2px solid QLinearGradient(
                    x1: 0, y1: 0,
                    x2: 0, y2: 1,
                    stop: 0 #ffa02f,
                    stop: 1 #d7801a
                );
            }

            QComboBox:on {
                padding-top: 3px;
                padding-left: 4px;
                background-color: QLinearGradient(
                    x1: 0, y1: 0,
                    x2: 0, y2: 1,
                    stop: 0 #2d2d2d,
                    stop: 0.1 #2b2b2b,
                    stop: 0.5 #292929,
                    stop: 0.9 #282828,
                    stop: 1 #252525
                );
                selection-background-color: #ffaa00;
            }

            QComboBox QAbstractItemView {
                border: 2px solid darkgray;
                selection-background-color: QLinearGradient(
                    x1: 0, y1: 0,
                    x2: 0, y2: 1,
                    stop: 0 #ffa02f,
                    stop: 1 #d7801a
                );
            }

            QComboBox::drop-down {
                 subcontrol-origin: padding;
                 subcontrol-position: top right;
                 width: 15px;
                 border-left-width: 0px;
                 border-left-color: darkgray;
                 border-left-style: solid;
                 border-top-right-radius: 3px;
                 border-bottom-right-radius: 3px;
             }

            QComboBox::down-arrow { }

            QGroupBox:focus {
                border: 2px solid QLinearGradient(
                    x1: 0, y1: 0,
                    x2: 0, y2: 1,
                    stop: 0 #ffa02f,
                    stop: 1 #d7801a
                );
            }

            QTextEdit:focus {
                border: 2px solid QLinearGradient(
                    x1: 0, y1: 0,
                    x2: 0, y2: 1,
                    stop: 0 #ffa02f,
                    stop: 1 #d7801a
                );
            }

            QScrollBar:horizontal {
                border: 1px solid #222222;
                background: QLinearGradient(
                    x1: 0, y1: 0,
                    x2: 0, y2: 1,
                    stop: 0.0 #121212,
                    stop: 0.2 #282828,
                    stop: 1 #484848
                );
                height: 7px;
                margin: 0px 16px 0 16px;
            }

            QScrollBar::handle:horizontal {
                background: QLinearGradient(
                    x1: 0, y1: 0,
                    x2: 1, y2: 0,
                    stop: 0 #ffa02f,
                    stop: 0.5 #d7801a,
                    stop: 1 #ffa02f
                );
                min-height: 20px;
                border-radius: 2px;
            }

            QScrollBar::add-line:horizontal {
                border: 1px solid #1b1b19;
                border-radius: 2px;
                background: QLinearGradient(
                    x1: 0, y1: 0,
                    x2: 1, y2: 0,
                    stop: 0 #ffa02f,
                    stop: 1 #d7801a
                );
                width: 14px;
                subcontrol-position: right;
                subcontrol-origin: margin;
            }

            QScrollBar::sub-line:horizontal {
                border: 1px solid #1b1b19;
                border-radius: 2px;
                background: QLinearGradient(
                    x1: 0, y1: 0,
                    x2: 1, y2: 0,
                    stop: 0 #ffa02f,
                    stop: 1 #d7801a
                );
                width: 14px;
                subcontrol-position: left;
                subcontrol-origin: margin;
            }

            QScrollBar::right-arrow:horizontal,
            QScrollBar::left-arrow:horizontal {
                border: 1px solid black;
                width: 1px;
                height: 1px;
                background: white;
            }

            QScrollBar::add-page:horizontal,
            QScrollBar::sub-page:horizontal { background: none; }

            QScrollBar:vertical {
                background: QLinearGradient(
                    x1: 0, y1: 0,
                    x2: 1, y2: 0,
                    stop: 0.0 #121212,
                    stop: 0.2 #282828,
                    stop: 1 #484848
                );
                width: 7px;
                margin: 16px 0 16px 0;
                border: 1px solid #222222;
            }

            QScrollBar::handle:vertical {
                background: QLinearGradient(
                    x1: 0, y1: 0,
                    x2: 0, y2: 1,
                    stop: 0 #ffa02f,
                    stop: 0.5 #d7801a,
                    stop: 1 #ffa02f
                );
                min-height: 20px;
                border-radius: 2px;
            }

            QScrollBar::add-line:vertical {
                border: 1px solid #1b1b19;
                border-radius: 2px;
                background: QLinearGradient(
                    x1: 0, y1: 0,
                    x2: 0, y2: 1,
                    stop: 0 #ffa02f,
                    stop: 1 #d7801a
                );
                height: 14px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }

            QScrollBar::sub-line:vertical {
                border: 1px solid #1b1b19;
                border-radius: 2px;
                background: QLinearGradient(
                    x1: 0, y1: 0,
                    x2: 0, y2: 1,
                    stop: 0 #d7801a,
                    stop: 1 #ffa02f
                );
                height: 14px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }

            QScrollBar::up-arrow:vertical,
            QScrollBar::down-arrow:vertical {
                border: 1px solid black;
                width: 1px;
                height: 1px;
                background: white;
            }

            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical { background: none; }

            QTextEdit { background-color: #242424; }

            QPlainTextEdit { background-color: #242424; }

            QHeaderView::section {
                background-color: QLinearGradient(
                    x1:0, y1:0,
                    x2:0, y2:1,
                    stop:0 #616161,
                    stop: 0.5 #505050,
                    stop: 0.6 #434343,
                    stop:1 #656565
                );
                color: white;
                padding-left: 4px;
                border: 1px solid #6c6c6c;
            }

            QCheckBox:disabled { color: #414141; }

            QDockWidget::title {
                text-align: center;
                spacing: 3px;
                background-color: QLinearGradient(
                    x1:0, y1:0,
                    x2:0, y2:1,
                    stop:0 #323232,
                    stop: 0.5 #242424,
                    stop:1 #323232
                    );
            }

            QDockWidget::close-button,
            QDockWidget::float-button {
                text-align: center;
                spacing: 1px;
                background-color: QLinearGradient(
                    x1:0, y1:0,
                    x2:0, y2:1,
                    stop:0 #323232,
                    stop: 0.5 #242424,
                    stop:1 #323232
                );
            }

            QDockWidget::close-button:hover,
            QDockWidget::float-button:hover { background: #242424; }

            QDockWidget::close-button:pressed,
            QDockWidget::float-button:pressed { padding: 1px -1px -1px 1px;}

            QMainWindow::separator {
                background-color: QLinearGradient(
                    x1:0, y1:0,
                    x2:0, y2:1,
                    stop:0 #161616,
                    stop: 0.5 #151515,
                    stop: 0.6 #212121,
                    stop:1 #343434
                );
                color: white;
                padding-left: 4px;
                border: 1px solid #4c4c4c;
                spacing: 3px;
            }

            QMainWindow::separator:hover {
                background-color: QLinearGradient(
                    x1:0, y1:0,
                    x2:0, y2:1,
                    stop:0 #d7801a,
                    stop:0.5 #b56c17,
                    stop:1 #ffa02f
                );
                color: white;
                padding-left: 4px;
                border: 1px solid #6c6c6c;
                spacing: 3px;
            }

            QToolBar::handle { spacing: 3px; }

            QMenu::separator {
                height: 2px;
                background-color: QLinearGradient(
                    x1:0, y1:0,
                    x2:0, y2:1,
                    stop:0 #161616,
                    stop: 0.5 #151515,
                    stop: 0.6 #212121,
                    stop:1 #343434
                );
                color: white;
                padding-left: 4px;
                margin-left: 10px;
                margin-right: 5px;
            }

            QProgressBar {
                border: 2px solid grey;
                border-radius: 5px;
                text-align: center;
            }

            QProgressBar::chunk {
                background-color: #d7801a;
                width: 2.15px;
                margin: 0.5px;
            }

            QTabBar::tab {
                color: #b1b1b1;
                border: 1px solid #444;
                border-bottom-style: none;
                background-color: #323232;
                padding-left: 10px;
                padding-right: 10px;
                padding-top: 3px;
                padding-bottom: 2px;
                margin-right: -1px;
            }

            QTabWidget::pane {
                border: 1px solid #444;
                top: 1px;
            }

            QTabBar::tab:last {
                margin-right: 0;
                border-top-right-radius: 3px;
            }

            QTabBar::tab:first:!selected {
                margin-left: 0px;
                border-top-left-radius: 3px;
            }

            QTabBar::tab:!selected {
                color: #b1b1b1;
                border-bottom-style: solid;
                margin-top: 3px;
                background-color: QLinearGradient(
                    x1:0, y1:0,
                    x2:0, y2:1,
                    stop:1 #212121,
                    stop:.4 #343434
                );
            }

            QTabBar::tab:selected {
                border-top-left-radius: 3px;
                border-top-right-radius: 3px;
                margin-bottom: 0px;
            }

            QTabBar::tab:!selected:hover {
                border-top: 2px solid #ffaa00;
                padding-bottom: 3px;
                border-top-left-radius: 3px;
                border-top-right-radius: 3px;
                background-color: QLinearGradient(
                    x1:0, y1:0,
                    x2:0, y2:1,
                    stop:1 #212121,
                    stop:0.4 #343434,
                    stop:0.2 #343434,
                    stop:0.1 #ffaa00
                );
            }

            QRadioButton::indicator:checked, QRadioButton::indicator:unchecked{
                color: #b1b1b1;
                background-color: #323232;
                border: 1px solid #b1b1b1;
                border-radius: 6px;
            }

            QRadioButton::indicator:checked {
                background-color: qradialgradient(
                    cx: 0.5, cy: 0.5,
                    fx: 0.5, fy: 0.5,
                    radius: 1.0,
                    stop: 0.25 #ffaa00,
                    stop: 0.3 #323232
                );
            }

            QCheckBox::indicator {
                color: #b1b1b1;
                background-color: #323232;
                border: 1px solid #b1b1b1;
                width: 9px;
                height: 9px;
            }

            QRadioButton::indicator { border-radius: 6px; }

            QRadioButton::indicator:hover, QCheckBox::indicator:hover {
                border: 1px solid #ffaa00;
            }

            QCheckBox::indicator:checked { }

            QCheckBox::indicator:disabled,
            QRadioButton::indicator:disabled {
                border: 1px solid #444;
            }
         ''')

        # this always gives the current user Home Folder, cross-platform
        homedir = path.expanduser("~")
        # print homedir and extensions variables for debug
        print((' INFO: My Home is ' + homedir))

        # Menu Bar inicialization and detail definitions
        menu_salir = QAction(QIcon.fromTheme("application-exit"),
            'Quit | Salir', self)
        # set the quit shortcut to CTRL + Q
        menu_salir.setShortcut('Ctrl+Q')
        # set the triggered signal to the quit slot
        menu_salir.setStatusTip('Quit | Salir')
        menu_salir.triggered.connect(self.close)

        # qt color setting via qcolordialog menu item
        menu_color = QAction(QIcon.fromTheme("preferences-system"),
            'Set GUI Colors | Configurar Colores de GUI', self)
        # set the status tip for this menu item
        menu_color.setStatusTip('Manually set GUI Colors...')
        # set the triggered signal to the showQColorDialog
        menu_color.triggered.connect(self.showQColorDialog)

        # qt window title setting via qdialog menu item
        menu_tit = QAction(QIcon.fromTheme("preferences-system"),
            'Set Window Title | Configurar Titulo de ventana', self)
        # set the status tip for this menu item
        menu_tit.setStatusTip('Manually set Window Title...')
        # set the triggered signal to the showQColorDialog
        menu_tit.triggered.connect(self.seTitle)

        # keys help
        menu_keys = QAction(QIcon.fromTheme("help-faq"), 'Shorcuts | Atajos',
                                                                        self)
        # set the status tip for this menu item
        menu_keys.setStatusTip('Key Shorcuts')
        # set the triggered signal to lambda gui that shows key shortcuts
        menu_keys.triggered.connect(lambda:
                        QMessageBox.about(self, __doc__, ' CTRL + Q = Quit '))

        # about faq
        menu_faq = QAction(QIcon.fromTheme("help-faq"), 'Donate | Donar', self)
        # set the status tip for this menu item
        menu_faq.setStatusTip(' Donate $5 !, No credit card required !')
        # set the triggered signal to lambda gui that shows the FAQ
        menu_faq.triggered.connect(lambda: open_new_tab('http://goo.gl/cB7PR'))

        # report a bug
        menu_bug = QAction(QIcon.fromTheme("help-faq"),
            'Report a Problem | Reportar un Problema ', self)
        # set the status tip for this menu item
        menu_bug.setStatusTip('Report a Problem...')
        # set the triggered signal to lambda for reporting problems
        menu_bug.triggered.connect(lambda:
            call('xdg-open mailto:juancarlospaco@ubuntu.com', shell=True))

        # about self
        menu_self = QAction(QIcon.fromTheme("help-contents"), 'About', self)
        # set the status tip for this menu item
        menu_self.setStatusTip('About self...')
        # set the triggered signal to lambda qmessagebox for the about __doc__
        menu_self.triggered.connect(lambda: QMessageBox.about(self, __doc__,
            ''.join((__doc__, ', version ', __version__, ' ( ', __license__,
            ' ), by ', __author__, ', ( ', __email__, ' ). '))))

        # about Qt
        menu_qt = QAction(QIcon.fromTheme("help-contents"), 'About Qt', self)
        # set the status tip for this menu item
        menu_qt.setStatusTip('About Qt...')
        # set the triggered signal to lambda for the about qt built-in gui
        menu_qt.triggered.connect(lambda: QMessageBox.aboutQt(self))

        # about python
        menu_py = QAction(QIcon.fromTheme("help-contents"),
            'About Python | Acerca de Python', self)
        # set the status tip for this menu item
        menu_py.setStatusTip('About Python...')
        # set the triggered signal to lambda for online about python
        menu_py.triggered.connect(lambda:
                                  open_new_tab('http://python.org/about'))

        # about pyalsa
        menu_pa = QAction(QIcon.fromTheme("help-contents"),
            'About PyAlsa | Acerca de PyAlsa', self)
        # set the status tip for this menu item
        menu_pa.setStatusTip('About PyAlsa...')
        # set the triggered signal to lambda for online about python
        menu_pa.triggered.connect(lambda:
          open_new_tab('http://pyalsaaudio.sourceforge.net/libalsaaudio.html'))

        # define the menu
        menu = self.menuBar()

        # File menu items
        archivo = menu.addMenu('&Archivo')
        archivo.addAction(menu_salir)

        # Settings menu
        settings = menu.addMenu('&Settings')
        settings.addAction(menu_color)
        settings.addAction(menu_tit)

        # Help menu items
        jelp = menu.addMenu('&Help')
        jelp.addAction(menu_faq)
        jelp.addAction(menu_keys)
        jelp.addAction(menu_bug)
        jelp.addSeparator()
        jelp.addAction(menu_self)
        jelp.addAction(menu_qt)
        jelp.addAction(menu_py)
        jelp.addAction(menu_pa)

        # Set Widgets Layout settings
        layout = QVBoxLayout(self)
        # set the lyout to self class
        self.setLayout(layout)
        # set the default spacing
        self.layout().setSpacing(1)

        self.lcdNumber = QLCDNumber(self)
        self.lcdNumber.setGeometry(QRect(525, 20, 80, 25))
        self.lcdNumber.setFrameShape(QFrame.StyledPanel)
        self.lcdNumber.setLineWidth(2)
        self.lcdNumber.setSmallDecimalPoint(True)
        self.lcdNumber.setNumDigits(4)
        self.lcdNumber.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber.setProperty("value", 666.0)
        self.lcdNumber.setToolTip('VUmeter LCD Display')
        self.lcdNumber.setObjectName("lcdNumber")
        layout.addWidget(self.lcdNumber)

        self.lcdNumber_2 = QLCDNumber(self)
        self.lcdNumber_2.setGeometry(QRect(525, 50, 80, 25))
        self.lcdNumber_2.setFrameShape(QFrame.StyledPanel)
        self.lcdNumber_2.setFrameShadow(QFrame.Raised)
        self.lcdNumber_2.setLineWidth(2)
        self.lcdNumber_2.setSmallDecimalPoint(True)
        self.lcdNumber_2.setNumDigits(4)
        self.lcdNumber_2.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber_2.setProperty("value", 666.0)
        self.lcdNumber_2.setToolTip('VUmeter LCD Display')
        self.lcdNumber_2.setObjectName("lcdNumber_2")
        layout.addWidget(self.lcdNumber_2)

        self.progressBar = QProgressBar(self)
        self.progressBar.setGeometry(QRect(20, 20, 500, 20))
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(5000)
        self.progressBar.setProperty("value", 2500)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setTextDirection(QProgressBar.TopToBottom)
        self.progressBar.setToolTip('VUmeter')
        self.progressBar.setObjectName("progressBar")
        layout.addWidget(self.progressBar)

        self.progressBar_2 = QProgressBar(self)
        self.progressBar_2.setGeometry(QRect(20, 50, 500, 20))
        self.progressBar_2.setMinimum(0)
        self.progressBar_2.setMaximum(5000)
        self.progressBar_2.setProperty("value", 2500)
        self.progressBar_2.setInvertedAppearance(False)
        self.progressBar_2.setTextDirection(QProgressBar.TopToBottom)
        self.progressBar_2.setToolTip('VUmeter')
        self.progressBar_2.setObjectName("progressBar_2")
        layout.addWidget(self.progressBar_2)

        self.dial = QDial(self)
        self.dial.setGeometry(QRect(530, 75, 75, 75))
        self.dial.setCursor(QCursor(Qt.ClosedHandCursor))
        self.dial.setMinimum(0)
        self.dial.setMaximum(9)
        self.dial.setProperty("value", 0)
        self.dial.setToolTip('THRESHOLD of Smart Recording')
        self.dial.setWrapping(False)
        self.dial.setNotchesVisible(True)
        self.dial.setObjectName("dial")
        layout.addWidget(self.dial)

        clock = QLCDNumber(self)
        clock.setNumDigits(25)
        timer = QTimer(self)
        timer.timeout.connect(lambda: clock.display(
            datetime.now().strftime("%d-%m-%Y %H:%M:%S %p")))
        timer.start(1000)
        clock.setObjectName("clock")
        clock.setGeometry(QRect(20, 80, 500, 50))
        clock.setToolTip(datetime.now().strftime("%c %x"))
        clock.setCursor(QCursor(Qt.CrossCursor))
        layout.addWidget(clock)

        self.label1 = QLabel(self)
        self.label1.setText('     Buffer Kb                 KBps                          Mode                          Sample                          Recording     ')
        self.label1.setGeometry(QRect(20, 150, 600, 25))
        self.label1.setObjectName("label")
        layout.addWidget(self.label1)

        self.combo1 = QComboBox(self)
        self.combo1.setGeometry(20, 175, 100, 25)
        self.combo1.setCursor(QCursor(Qt.PointingHandCursor))
        self.combo1.setToolTip('Real Time Buffer Data Chunk')
        self.combo1.addItems(['1024', '512', '256', '128'])
        layout.addWidget(self.combo1)

        self.combo2 = QComboBox(self)
        self.combo2.setGeometry(145, 175, 100, 25)
        self.combo2.setCursor(QCursor(Qt.PointingHandCursor))
        self.combo2.setToolTip('Sound KBps')
        self.combo2.addItems(['128', '256', '512', '1024', '64', '32', '16'])
        layout.addWidget(self.combo2)

        self.combo3 = QComboBox(self)
        self.combo3.setGeometry(265, 175, 100, 25)
        self.combo3.setCursor(QCursor(Qt.PointingHandCursor))
        self.combo3.setToolTip('Sound Channels')
        self.combo3.addItems(['MONO', 'STEREO', 'Surround'])
        layout.addWidget(self.combo3)

        self.combo4 = QComboBox(self)
        self.combo4.setGeometry(395, 175, 100, 25)
        self.combo4.setCursor(QCursor(Qt.PointingHandCursor))
        self.combo4.setToolTip('Sound Sample Rate')
        self.combo4.addItems(['44100', '96000', '48000', '32000',
                              '22050', '16000', '11025', '8000'])
        layout.addWidget(self.combo4)

        self.combo5 = QComboBox(self)
        self.combo5.setGeometry(520, 175, 100, 25)
        self.combo5.setCursor(QCursor(Qt.PointingHandCursor))
        self.combo5.setToolTip('Sound Detection for Recording')
        self.combo5.addItems(['SMART', 'FORCE'])
        layout.addWidget(self.combo5)

        self.label2 = QLabel(self)
        self.label2.setText(' 30 Min                                         60 Min                                             90 Min                                  120 Min ')
        self.label2.setGeometry(QRect(20, 225, 600, 25))
        self.label2.setCursor(QCursor(Qt.OpenHandCursor))
        self.label2.setToolTip('MINUTES of recording')
        self.label2.setObjectName("label2")
        layout.addWidget(self.label2)

        self.horizontalSlider = QSlider(self)
        self.horizontalSlider.setGeometry(QRect(20, 250, 600, 25))
        self.horizontalSlider.setCursor(QCursor(Qt.ClosedHandCursor))
        self.horizontalSlider.setMinimum(30)
        self.horizontalSlider.setMaximum(120)
        self.horizontalSlider.setProperty("value", 30)
        self.horizontalSlider.setOrientation(Qt.Horizontal)
        self.horizontalSlider.setInvertedAppearance(False)
        self.horizontalSlider.setInvertedControls(False)
        self.horizontalSlider.setTickPosition(QSlider.TicksBothSides)
        self.horizontalSlider.setTickInterval(30)
        self.horizontalSlider.setSingleStep(30)
        self.horizontalSlider.setPageStep(30)
        self.horizontalSlider.setToolTip('MINUTES of recording')
        self.horizontalSlider.setObjectName("horizontalSlider")
        layout.addWidget(self.horizontalSlider)

        self.label3 = QLabel(self)
        self.label3.setText(' <b> Cards: </b> ' + ''.join(a
          for a in str(alsaaudio.cards()).lower() if a not in set(punctuation)))
        self.label3.setGeometry(QRect(20, 300, 600, 25))
        self.label3.setToolTip('Sound Hardware')
        self.label3.setObjectName("label3")
        layout.addWidget(self.label3)

        self.label4 = QLabel(self)
        self.label4.setText(' <b> Mixers: </b> ' + ''.join(a
                for a in str(alsaaudio.mixers()) if a not in set(punctuation)))
        self.label4.setGeometry(QRect(20, 325, 600, 25))
        self.label4.setToolTip('Sound Hardware')
        self.label4.setObjectName("label4")
        layout.addWidget(self.label4)

        print((' INFO: Using Cards ' + str(alsaaudio.cards()).lower()))
        print((' INFO: Using Mixers ' + str(alsaaudio.mixers()).lower()))

        self.label0 = QLabel(self)
        self.label0.setText(' Advanced Input Capturing Codec selection ')
        self.label0.setGeometry(QRect(20, 375, 600, 25))
        self.label0.setObjectName("label0")
        layout.addWidget(self.label0)

        self.combo0 = QComboBox(self)
        self.combo0.setGeometry(20, 400, 600, 25)
        self.combo0.setCursor(QCursor(Qt.PointingHandCursor))
        self.combo0.setToolTip('Recording Codec')
        self.combo0.addItems([
          'PCM_FORMAT_S32_LE Signed 32bit sample per channel Little Endian',
          'PCM_FORMAT_S8 Signed 8bit samples for each channel',
          'PCM_FORMAT_U8 Signed 8bit samples for each channel',
          'PCM_FORMAT_S16_LE Signed 16bit sample per channel Little Endian',
          'PCM_FORMAT_S16_BE Signed 16bit sample per each channel Big Endian',
          'PCM_FORMAT_U16_LE Unsigned 16bit sample per channel Little Endian',
          'PCM_FORMAT_U16_BE Unsigned 16bit sample per channel Big Endian',
          'PCM_FORMAT_S24_LE Signed 24bit sample per channel Little Endian',
          'PCM_FORMAT_S24_BE Signed 24bit sample per channel Big Endian',
          'PCM_FORMAT_U24_LE Unsigned 24bit sample per channel Little Endian',
          'PCM_FORMAT_U24_BE Unsigned 24bit samples per channel Big Endian',
          'PCM_FORMAT_S32_BE Signed 32bit sample per channel Big Endian',
          'PCM_FORMAT_U32_LE Unsigned 32bit sample per channel Little Endian',
          'PCM_FORMAT_U32_BE Unsigned 32bit sample per channel Big Endian',
          'PCM_FORMAT_FLOAT_LE 32bit samples encoded as float Little Endian',
          'PCM_FORMAT_FLOAT_BE 32bit samples encoded as float Big Endian',
          'PCM_FORMAT_FLOAT64_LE 64bit sample encoded as float Little Endian',
          'PCM_FORMAT_FLOAT64_BE 64bit samples encoded as float Big Endian',
          'PCM_FORMAT_MU_LAW A logarithmic encoding used by .au files',
          'PCM_FORMAT_A_LAW Another logarithmic encoding',
          'PCM_FORMAT_IMA_ADPCM A 4:1 compressed format by I.M.A.',
          'PCM_FORMAT_MPEG MPEG encoded audio',
          'PCM_FORMAT_GSM 9600 bits/s constant rate encoding for speech'
          ])
        layout.addWidget(self.combo0)

        self.label5 = QLabel(self)
        self.label5.setText(' Disk Space')
        self.label5.setGeometry(QRect(20, 450, 600, 25))
        self.label5.setObjectName("label5")
        layout.addWidget(self.label5)

        self.diskBar = QProgressBar(self)
        self.diskBar.setGeometry(QRect(20, 475, 600, 25))
        self.diskBar.setMinimum(0)
        self.diskBar.setMaximum(statvfs(homedir).f_blocks *
            statvfs(homedir).f_frsize / 1024 / 1024 / 1024)
        self.diskBar.setProperty("value", statvfs(homedir).f_bfree *
            statvfs(homedir).f_frsize / 1024 / 1024 / 1024)
        self.diskBar.setInvertedAppearance(False)
        self.diskBar.setTextDirection(QProgressBar.TopToBottom)
        self.diskBar.setToolTip(str(statvfs(homedir).f_bfree *
            statvfs(homedir).f_frsize / 1024 / 1024 / 1024) + ' Gigabytes free')
        self.diskBar.setObjectName("diskBar")
        layout.addWidget(self.diskBar)

        self.label6 = QLabel(self)
        self.label6.setText(' <b> Off-line Output Recording Codec: </b> ' +
                        str(getoutput('oggenc --version', shell=True)).strip())
        self.label6.setGeometry(QRect(20, 525, 600, 25))
        self.label6.setObjectName("label6")
        layout.addWidget(self.label6)

        self.button1 = QPushButton(self)
        self.button1.setGeometry(QRect(25, 575, 100, 25))
        self.button1.setText(' Files ')
        self.button1.setObjectName("button1")
        self.button1.clicked.connect(lambda:
                                     call('xdg-open ' + getcwd(), shell=True))
        layout.addWidget(self.button1)

        self.button2 = QPushButton(self)
        self.button2.setGeometry(QRect(150, 575, 100, 25))
        self.button2.setText(' Donate ')
        self.button2.setToolTip(' Donate $5 !, No credit card required ! ')
        self.button2.setObjectName("button2")
        self.button2.clicked.connect(lambda:
                                     open_new_tab('http://goo.gl/cB7PR'))
        layout.addWidget(self.button2)

        self.button3 = QPushButton(self)
        self.button3.setGeometry(QRect(525, 575, 100, 25))
        self.button3.setText(' Compress OGG ')
        self.button3.setObjectName("button3")
        self.button3.clicked.connect(self.convertOGG)
        layout.addWidget(self.button3)

        self.button4 = QPushButton(self)
        self.button4.setGeometry(QRect(400, 575, 100, 25))
        self.button4.setText(' Screenshot ')
        self.button4.setObjectName("button4")
        self.button4.clicked.connect(lambda: QPixmap.grabWindow(
            QApplication.desktop().winId()).save(QFileDialog.getSaveFileName(
            self, " Save Screenshot As ... ", getcwd(), ';;(*.png)', 'png')))

        self.button5 = QPushButton(self)
        self.button5.setGeometry(QRect(275, 575, 100, 25))
        self.button5.setText(' OGG --> ZIP ')
        self.button5.setObjectName("button4")
        self.button5.clicked.connect(lambda: make_archive(
            str(QFileDialog.getSaveFileName(self, "Save OGG to ZIP file As...",
            getcwd(), ';;(*.zip)', 'zip')).replace('.zip', ''), "zip",
            path.abspath(path.join(getcwd(), str(datetime.now().year)))))

        # Bottom Buttons Bar
        self.buttonBox = QDialogButtonBox(self)
        # set the geometry of buttonbox
        self.buttonBox.setGeometry(QRect(25, 625, 600, 32))
        # set the orientation, can be horizontal or vertical
        self.buttonBox.setOrientation(Qt.Horizontal)
        # define the buttons to use on it, std buttons uncomment to use
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok |
            QDialogButtonBox.Cancel | QDialogButtonBox.Close |
            QDialogButtonBox.Reset | QDialogButtonBox.Help |
            QDialogButtonBox.Abort | QDialogButtonBox.Retry)
        # set if buttons are centered or not
        self.buttonBox.setCenterButtons(False)
        # give the object a name
        self.buttonBox.setObjectName("buttonBox")
        # add it to the layout
        layout.addWidget(self.buttonBox)
        # Help Button Action connection helpRequested() to a QMessageBox
        self.buttonBox.helpRequested.connect(lambda: QMessageBox.about(self,
            __doc__, ''.join((__doc__, linesep, 'version ', __version__, ' (',
            __license__, '), by ', __author__, ', ( ', __email__, ' ). \n'))))
        # Help Button Action connection to a quit() slot
        self.buttonBox.rejected.connect(self.close)
        # Help Button Action connection to a accepted() slot
        self.buttonBox.accepted.connect(self.run)
        # Paleta de colores para pintar transparente
        palette = self.palette()
        # add a transparent to the brush of palette
        palette.setBrush(QPalette.Base, Qt.transparent)
        # set the palette to the page in the widget
        self.setPalette(palette)
        # set the opaque paint to false
        self.setAttribute(Qt.WA_OpaquePaintEvent, False)
        # self.convertOGG()

    def run(self):  # FIXME threading ???
        ' run the recording functionality '

        print((' INFO: Started Recording at ' + str(datetime.now())))
        inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE)
        # Parse the options

        # stereo, mono
        if self.combo3.currentText() == 'MONO':
            inp.setchannels(1)
            print(' INFO: Using Mono, 1 Channel . . . ')
        elif self.combo3.currentText() == 'STEREO':
            inp.setchannels(2)
            print(' INFO: Using Stereo, 2 Channels . . . ')
        elif self.combo3.currentText() == 'Surround':
            inp.setchannels(6)
            print(' INFO: Using 3D Surround, 6 Channels . . . ')
            print((' WARNING: 6 Channels 3D Surround is EXPERIMENTAL!!\n' * 9))

        # '44100', '96000', '48000', '32000', '22050', '16000', '11025', '8000'
        if self.combo4.currentText() == '44100':
            bitrate = 44100
            inp.setrate(bitrate)
            print(' INFO: Using 44100 Hz per Second . . . ')
        elif self.combo4.currentText() == '96000':
            bitrate = 96000
            inp.setrate(bitrate)
            print(' INFO: Using 96000 Hz per Second . . . ')
        elif self.combo4.currentText() == '48000':
            bitrate = 48000
            inp.setrate(bitrate)
            print(' INFO: Using 48000 Hz per Second . . . ')
        elif self.combo4.currentText() == '32000':
            bitrate = 32000
            inp.setrate(bitrate)
            print(' INFO: Using 32000 Hz per Second . . . ')
        elif self.combo4.currentText() == '22050':
            bitrate = 22050
            inp.setrate(bitrate)
            print(' INFO: Using 22050 Hz per Second . . . ')
        elif self.combo4.currentText() == '16000':
            bitrate = 16000
            inp.setrate(bitrate)
            print(' INFO: Using 16000 Hz per Second . . . ')
        elif self.combo4.currentText() == '11025':
            bitrate = 11025
            inp.setrate(bitrate)
            print(' INFO: Using 11025 Hz per Second . . . ')
        elif self.combo4.currentText() == '8000':
            bitrate = 8000
            inp.setrate(bitrate)
            print(' INFO: Using 8000 Hz per Second . . . ')

        # Sound Codec
        if self.combo0.currentText() == \
            'PCM_FORMAT_S8 Signed 8bit samples for each channel':
            inp.setformat(alsaaudio.PCM_FORMAT_S8)
            print(' INFO: Using Sound Codec PCM_FORMAT_S8')

        elif self.combo0.currentText() == \
            'PCM_FORMAT_U8 Signed 8bit samples for each channel':
            inp.setformat(alsaaudio.PCM_FORMAT_U8)
            print(' INFO: Using Sound Codec PCM_FORMAT_U8')

        elif self.combo0.currentText() == \
            'PCM_FORMAT_S16_LE Signed 16bit sample per channel Little Endian':
            inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
            print(' INFO: Using Sound Codec PCM_FORMAT_S16_LE')

        elif self.combo0.currentText() == \
           'PCM_FORMAT_S16_BE Signed 16bit sample per each channel Big Endian':
            inp.setformat(alsaaudio.PCM_FORMAT_S16_BE)
            print(' INFO: Using Sound Codec PCM_FORMAT_S16_BE')

        elif self.combo0.currentText() == \
           'PCM_FORMAT_U16_LE Unsigned 16bit sample per channel Little Endian':
            inp.setformat(alsaaudio.PCM_FORMAT_U16_LE)
            print(' INFO: Using Sound Codec PCM_FORMAT_U16_LE')

        elif self.combo0.currentText() == \
            'PCM_FORMAT_U16_BE Unsigned 16bit sample per channel Big Endian':
            inp.setformat(alsaaudio.PCM_FORMAT_U16_BE)
            print(' INFO: Using Sound Codec PCM_FORMAT_U16_BE')

        elif self.combo0.currentText() == \
            'PCM_FORMAT_S24_LE Signed 24bit sample per channel Little Endian':
            inp.setformat(alsaaudio.PCM_FORMAT_S24_LE)
            print(' INFO: Using Sound Codec PCM_FORMAT_S24_LE')

        elif self.combo0.currentText() == \
            'PCM_FORMAT_S24_BE Signed 24bit sample per channel Big Endian':
            inp.setformat(alsaaudio.PCM_FORMAT_S24_BE)
            print(' INFO: Using Sound Codec PCM_FORMAT_S24_BE')

        elif self.combo0.currentText() == \
            'PCM_FORMAT_S32_LE Signed 32bit sample per channel Little Endian':
            inp.setformat(alsaaudio.PCM_FORMAT_S32_LE)
            print(' INFO: Using Sound Codec PCM_FORMAT_S32_LE')

        elif self.combo0.currentText() == \
                'PCM_FORMAT_S32_BE Signed 32bit sample per channel Big Endian':
            inp.setformat(alsaaudio.PCM_FORMAT_S32_BE)
            print(' INFO: Using Sound Codec PCM_FORMAT_S32_BE')

        elif self.combo0.currentText() == \
           'PCM_FORMAT_U32_LE Unsigned 32bit sample per channel Little Endian':
            inp.setformat(alsaaudio.PCM_FORMAT_U32_LE)
            print(' INFO: Using Sound Codec PCM_FORMAT_U32_LE')

        elif self.combo0.currentText() == \
           'PCM_FORMAT_U32_LE Unsigned 32bit sample per channel Little Endian':
            inp.setformat(alsaaudio.PCM_FORMAT_U32_LE)
            print(' INFO: Using Sound Codec PCM_FORMAT_U32_LE')

        elif self.combo0.currentText() == \
            'PCM_FORMAT_U32_BE Unsigned 32bit sample per channel Big Endian':
            inp.setformat(alsaaudio.PCM_FORMAT_U32_BE)
            print(' INFO: Using Sound Codec PCM_FORMAT_U32_BE')

        elif self.combo0.currentText() == \
            'PCM_FORMAT_FLOAT_LE 32bit samples encoded as float Little Endian':
            inp.setformat(alsaaudio.PCM_FORMAT_FLOAT_LE)
            print(' INFO: Using Sound Codec PCM_FORMAT_FLOAT_LE')

        elif self.combo0.currentText() == \
            'PCM_FORMAT_FLOAT_BE 32bit samples encoded as float Big Endian':
            inp.setformat(alsaaudio.PCM_FORMAT_FLOAT_BE)
            print(' INFO: Using Sound Codec PCM_FORMAT_FLOAT_BE')

        elif self.combo0.currentText() == \
           'PCM_FORMAT_FLOAT64_LE 64bit sample encoded as float Little Endian':
            inp.setformat(alsaaudio.PCM_FORMAT_FLOAT64_LE)
            print(' INFO: Using Sound Codec PCM_FORMAT_FLOAT64_LE')

        elif self.combo0.currentText() == \
            'PCM_FORMAT_FLOAT64_BE 64bit samples encoded as float Big Endian':
            inp.setformat(alsaaudio.PCM_FORMAT_FLOAT64_BE)
            print(' INFO: Using Sound Codec PCM_FORMAT_FLOAT64_BE')

        elif self.combo0.currentText() == \
            'PCM_FORMAT_MU_LAW A logarithmic encoding used by .au files':
            inp.setformat(alsaaudio.PCM_FORMAT_MU_LAW)
            print(' INFO: Using Sound Codec PCM_FORMAT_MU_LAW')

        elif self.combo0.currentText() == \
            'PCM_FORMAT_A_LAW Another logarithmic encoding':
            inp.setformat(alsaaudio.PCM_FORMAT_A_LAW)
            print(' INFO: Using Sound Codec PCM_FORMAT_A_LAW')

        elif self.combo0.currentText() == \
            'PCM_FORMAT_IMA_ADPCM A 4:1 compressed format by I.M.A.':
            inp.setformat(alsaaudio.PCM_FORMAT_IMA_ADPCM)
            print(' INFO: Using Sound Codec PCM_FORMAT_IMA_ADPCM')

        elif self.combo0.currentText() == \
            'PCM_FORMAT_MPEG MPEG encoded audio':
            inp.setformat(alsaaudio.PCM_FORMAT_MPEG)
            print(' INFO: Using Sound Codec PCM_FORMAT_MPEG')

        elif self.combo0.currentText() == \
            'PCM_FORMAT_GSM 9600 bits/s constant rate encoding for speech':
            inp.setformat(alsaaudio.PCM_FORMAT_GSM)
            print(' INFO: Using Sound Codec PCM_FORMAT_GSM')

        # raw binary data chunk size
        if self.combo1.currentText() == '1024':
            inp.setperiodsize(1024)
            print(' INFO: Using Buffer Data Chuck of 1024 . . . ')
        elif self.combo1.currentText() == '512':
            inp.setperiodsize(512)
            print(' INFO: Using Buffer Data Chuck of 512 . . . ')
        elif self.combo1.currentText() == '256':
            inp.setperiodsize(256)
            print(' INFO: Using Buffer Data Chuck of 256 . . . ')
        elif self.combo1.currentText() == '128':
            inp.setperiodsize(128)
            print(' INFO: Using Buffer Data Chuck of 128 . . . ')

        # threshold value
        try:
            THRESHOLD = self.dial.value() * 100
            print((' INFO: Using Thresold of ' + str(THRESHOLD) + ' . . . '))
        except:
            THRESHOLD = 0
            print((' INFO: Using FALLBACK Thresold ' + str(THRESHOLD) + '...'))

        # recording time
        try:
            RECORD_SECONDS = self.horizontalSlider.value() * 60  # * 60
            print((' INFO: Using Recording time of ' + str(RECORD_SECONDS)))
        except:
            RECORD_SECONDS = 1800
            print((' INFO: FALLBACK Recording time' + str(RECORD_SECONDS)))

        base = path.join(getcwd(), str(datetime.now().year))
        self.convertOGG()

        # recording loop
        while True:
            filename = path.abspath(path.join(base, str(datetime.now().month),
                       datetime.now().strftime("%Y-%m-%d_%H:%M:%S.pcm")))
            print((' INFO: Recording on the file ' + filename))
            f = open(filename, 'wb')
            print(('-' * 80))
            print((' INFO: Loop Range ' + str(bitrate / 1024 * RECORD_SECONDS)))
            print(' Logic Tick, Data Chunk, VUmeter ')
            for i in range(0, bitrate / 512 * RECORD_SECONDS):
                l, data = inp.read()
                b = numpy.fromstring(data, dtype='int32')
                a = int(numpy.abs(b).mean().astype(numpy.int32) * 0.00001)

                # Feedback to the GUI and CLI
                print((i, l, a))
                self.progressBar.setValue(a)
                self.progressBar_2.setValue(a)
                self.lcdNumber.display(a)
                self.lcdNumber_2.display(a)

                # compares THRESHOLD versus a so only record if sound detected
                if self.combo5.currentText() == 'SMART' and a <= THRESHOLD:
                    continue
                # force recording, even if its silent
                else:
                    f.write(data)
            f.close()

    def convertOGG(self):
        ' convert to ogg files '
        # make base directory
        base = path.join(getcwd(), str(datetime.now().year))
        try:
            mkdir(base)
            print((' INFO: Base Directory path created ' + base))
        except OSError:
            print((' INFO: Base Directory path already exist ' + base))
        except:
            print((' ERROR: Can not create Base Directory ?, ' + base))
        # make directory tree
        try:
            for dr in range(1, 13):
                mkdir(path.abspath(path.join(base, str(dr))))
                print((' INFO: Directory Tree created ', base, str(dr)))
        except OSError:
            print((' INFO: Directory Tree path already exist ' + base + '1,12'))
        except:
            print((' ERROR: Can not create Directory Tree?, ' + base + '1, 12'))
        # convert RAW .PCM to compressed .OGG files
        print(' INFO: Compressing sound into .OGG files . . . ')
        try:
            for dr in range(1, 13):
                print((''.join((' INFO: Executing:  oggenc -r --downmix ',
                            path.abspath(path.join(base, str(dr), '*.pcm'))))))
                call(''.join(('nice --adjustment=20 oggenc -r --downmix ',
                path.abspath(path.join(base, str(dr), '*.pcm')))), shell=True)
                print((' INFO: Compressed .OGG files created at ',
                       path.abspath(path.join(base, str(dr), '*.pcm'))))
            # remove uncompressed files
            print(' INFO: Deleting uncompressed sound files . . . ')
            [remove(a) for a in iter(["{}/{}".format(root, f) for root, f in list(chain(*[list(product([root], files)) for root, dirs, files in walk(base)])) if f.endswith(('.pcm', '.PCM')) and not f.startswith('.')])]
        except:
            print((' ERROR: Cant Convert PCM to OGG files?, ' + base))
            print(' ERROR: oggenc not found installed ??? ')
            print(' ( sudo apt-get install vorbis-tools ) ')

    def closeEvent(self, event):
        ' Ask to Quit '
        # if the reply is yes then accept, else ignore the close call
        event.accept() if QMessageBox.question(self, 'Close | Cerrar',
            "Salir? | Quit?", QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No) == QMessageBox.Yes else event.ignore()

    def paintEvent(self, event):
        ' Paint semi-transparent background '
        QWidget.paintEvent(self, event)
        # make a painter
        # make a painter
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setRenderHint(QPainter.TextAntialiasing)
        p.setRenderHint(QPainter.HighQualityAntialiasing)
        # fill a rectangle with transparent painting
        p.fillRect(event.rect(), Qt.transparent)
        # animated random dots background pattern
        for i in range(4096):
            x = randint(25, self.size().width() - 25)
            y = randint(25, self.size().height() - 25)
            p.setPen(QPen(QColor(randint(9, 255), 255, randint(9, 255)), 1))
            p.drawPoint(x, y)
        # set pen to use white color
        p.setPen(QPen(QColor(randint(9, 255), 255, randint(9, 255)), 1))
        # Rotate painter 45 Degree
        p.rotate(45)
        # Set painter Font for text
        p.setFont(QFont('Ubuntu', 200))
        # draw the background text, with antialiasing
        p.drawText(99, 99, "Radio")
        # Rotate -45 the QPen back !
        p.rotate(-45)
        # set the pen to no pen
        p.setPen(Qt.NoPen)
        # Background Color
        p.setBrush(QColor(0, 0, 0))
        # Background Opacity
        p.setOpacity(0.75)
        # Background Rounded Borders
        p.drawRoundedRect(self.rect(), 100, 50)
        # finalize the painter
        p.end()

    def showQColorDialog(self):
        ' Choose a Color for Qt '
        color = QColorDialog.getColor()
        # print info
        print((' INFO: Using User requested color ' + str(color.name())))
        # if the color is a valid color use it into an CSS and apply it
        if color.isValid():
            self.setStyleSheet(" * { background-color: %s } " % color.name())

    def seTitle(self):
        ' set the title of the main window '
        # make a dialog gui
        dialog = QDialog(self)
        #
        textEditInput = QLineEdit(dialog)
        textEditInput.setPlaceholderText(' title ')
        # make a button
        ok = QPushButton(dialog)
        # set the text on the button to ok
        ok.setText('&O K')
        ok.setDefault(True)
        # connect the clicked signal to an accept slot
        ok.clicked.connect(lambda: self.setWindowTitle(textEditInput.text()))
        # make a local layout
        layout = QVBoxLayout()
        [layout.addWidget(a) for a in (QLabel('Title:'), textEditInput, ok)]
        dialog.setLayout(layout)
        # run the dialog
        dialog.exec_()


###############################################################################


def main():
    ' Main Loop '
    app = QApplication(sys.argv)
    # w is gonna be the mymainwindow class
    w = MyMainWindow()
    # set the class with the attribute of translucent background as true
    w.setAttribute(Qt.WA_TranslucentBackground, True)
    # run the class
    w.show()
    # if exiting the loop take down the app
    sys.exit(app.exec_())


if __name__ == '__main__':
    ' Do NOT add anything here!, use main() function instead. '
    main()
