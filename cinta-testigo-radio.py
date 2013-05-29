#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PEP8:OK, LINT:OK, PY3:OK


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


# metadata
' Cinta Testigo para Radios '
__version__ = ' 0.9 '
__license__ = ' GPL '
__author__ = ' juancarlospaco '
__email__ = ' juancarlospaco@ubuntu.com '
__url__ = ' https://github.com/juancarlospaco '
__date__ = ' 06/06/2013 '
__prj__ = ' cintatestigo '
__docformat__ = 'html'
__source__ = ''
__full_licence__ = 'http://opensource.org/licenses/gpl-3.0.html'


# imports
import sys
from os import (path, linesep, geteuid, environ,
                statvfs, mkdir, getcwd, remove, walk)
from datetime import datetime
from subprocess import call
from random import randint
from webbrowser import open_new_tab
from subprocess import check_output as getoutput
from itertools import (chain, product)
import wave
try:
    from urllib.request import urlopen  # py3
except ImportError:
    from urllib2 import urlopen  # lint:ok

from sip import setapi
try:
    from PyQt4.QtGui import (QIcon, QLabel, QFileDialog, QWidget, QVBoxLayout,
        QHBoxLayout, QComboBox, QCursor, QLineEdit, QCheckBox, QPushButton,
        QGroupBox, QMessageBox, QCompleter, QDirModel, QLCDNumber, QAction,
        QFont, QTabWidget, QDockWidget, QToolBar, QSizePolicy, QColorDialog,
        QPalette, QPen, QPainter, QColor, QPixmap, QMenu, QDialog, QSlider,
        QDesktopWidget, QProgressBar, QMainWindow, QFrame, QApplication,
        QTreeWidget, QTreeWidgetItem, QColumnView, QDial)

    from PyQt4.QtCore import (Qt, QDir, QSize, QUrl, QTimer, QFileInfo)

    from PyQt4.QtNetwork import (QNetworkProxy, )
    from PyQt4.phonon import Phonon
except ImportError:
    print(''' ERROR: No Qt4 avaliable !
          ( sudo apt-get install python-qt4 python-qt4-phonon ) ''')
    exit()

try:
    from PyKDE4.kdeui import (KAboutApplicationDialog, KColorDialog, KHelpMenu,
                              KFontDialog)
    from PyKDE4.kdeui import KTextEdit as QPlainTextEdit
    from PyKDE4.kdeui import KDatePicker as QCalendarWidget
    from PyKDE4.solid import Solid
    from PyKDE4.nepomuk import Nepomuk
    from PyKDE4.kdecore import (KAboutData, ki18n, KUrl)
    aboutData = KAboutData(__doc__, "", ki18n(__doc__), __version__,
        ki18n(__doc__), KAboutData.License_GPL, ki18n(__author__),
        ki18n(" This Smart App uses KDE if present, else Qt only if present "),
        __url__, __email__)
    KDE = True
except ImportError:
    from PyQt4.QtGui import (QPlainTextEdit, QCalendarWidget,  # lint:ok
                             QFontDialog, )  # lint:ok
    print(" WARNING: No PyKDE ! \n ( sudo apt-get install python-kde4 ) ")
    KDE = False


try:
    import alsaaudio
except ImportError:
    exit(' ERROR: AlsaAudio not found,(sudo apt-get install python-alsaaudio)')

try:
    import numpy
except ImportError:
    exit(' ERROR: NumPy not found !, ( sudo apt-get install python-numpy )')


# API 2
(setapi(a, 2) for a in ("QDate", "QDateTime", "QString", "QTime", "QUrl",
                        "QTextStream", "QVariant"))


# constants
HOME = path.abspath(path.expanduser("~"))
print((' INFO: My Home Dir is {}'.format(HOME)))


# root check
if geteuid() == 0:
    exit(" ERROR: Do NOT Run as root!, NO ejecutar como root!\n bye noob...\n")
else:
    pass


print(('#' * 80))
print((''.join((__doc__, ',v.', __version__, __license__, ' by ', __author__))))


###############################################################################


class MyMainWindow(QMainWindow):
    ' Main Window '
    def __init__(self, parent=None):
        ' Initialize QWidget inside MyMainWindow '
        super(MyMainWindow, self).__init__(parent)
        QWidget.__init__(self)
        self.statusBar().showMessage('               {}'.format(__doc__))
        self.setStyleSheet('QStatusBar{color:grey;}')
        self.setWindowTitle(__doc__)
        self.setWindowIcon(QIcon.fromTheme("face-monkey"))
        self.setFont(QFont('Ubuntu Light', 10))
        self.setMaximumSize(QDesktopWidget().screenGeometry().width(),
                            QDesktopWidget().screenGeometry().height())

        self.base = path.abspath(path.join(getcwd(), str(datetime.now().year)))

        # directory auto completer
        self.completer = QCompleter(self)
        self.dirs = QDirModel(self)
        self.dirs.setFilter(QDir.AllEntries | QDir.NoDotAndDotDot)
        self.completer.setModel(self.dirs)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setCompletionMode(QCompleter.PopupCompletion)

        # Proxy support, by reading http_proxy os env variable
        proxy_url = QUrl(environ.get('http_proxy', ''))
        QNetworkProxy.setApplicationProxy(QNetworkProxy(QNetworkProxy.HttpProxy
            if str(proxy_url.scheme()).startswith('http')
            else QNetworkProxy.Socks5Proxy, proxy_url.host(), proxy_url.port(),
                 proxy_url.userName(), proxy_url.password())) \
            if 'http_proxy' in environ else None
        print((' INFO: Proxy Auto-Config as ' + str(proxy_url)))

        # basic widgets layouts and set up
        self.mainwidget = QTabWidget()
        self.mainwidget.setToolTip(__doc__)
        self.mainwidget.setMovable(True)
        self.mainwidget.setTabShape(QTabWidget.Triangular)
        self.mainwidget.setTabsClosable(True)
        self.mainwidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.mainwidget.tabCloseRequested.connect(lambda:
            self.mainwidget.setTabPosition(1)
            if self.mainwidget.tabPosition() == 0
            else self.mainwidget.setTabPosition(0))
        self.setCentralWidget(self.mainwidget)
        self.dock1 = QDockWidget()
        self.dock2 = QDockWidget()
        self.dock3 = QDockWidget()
        self.dock4 = QDockWidget()
        for a in (self.dock1, self.dock2, self.dock3, self.dock4):
            a.setWindowModality(Qt.NonModal)
            a.setWindowOpacity(0.9)
            a.setWindowTitle(__doc__
                             if a.windowTitle() == '' else a.windowTitle())
            a.setStyleSheet('QDockWidget::title{text-align:center;}')
            a.setFeatures(QDockWidget.DockWidgetFloatable |
                          QDockWidget.DockWidgetMovable)
            self.mainwidget.addTab(a, QIcon.fromTheme("face-cool"),
                                   str(a.windowTitle()).strip().lower())

        # Paleta de colores para pintar transparente
        self.palette().setBrush(QPalette.Base, Qt.transparent)
        self.setPalette(self.palette())
        self.setAttribute(Qt.WA_OpaquePaintEvent, False)

        # toolbar and basic actions
        self.toolbar = QToolBar(self)
        self.toolbar.setIconSize(QSize(24, 24))
        # spacer widget for left
        self.left_spacer = QWidget(self)
        self.left_spacer.setSizePolicy(QSizePolicy.Expanding,
                                       QSizePolicy.Expanding)
        # spacer widget for right
        self.right_spacer = QWidget(self)
        self.right_spacer.setSizePolicy(QSizePolicy.Expanding,
                                        QSizePolicy.Expanding)
        qaqq = QAction(QIcon.fromTheme("application-exit"), 'Quit', self)
        qaqq.setShortcut('Ctrl+Q')
        qaqq.triggered.connect(exit)
        qamin = QAction(QIcon.fromTheme("go-down"), 'Minimize', self)
        qamin.triggered.connect(lambda: self.showMinimized())
        qamax = QAction(QIcon.fromTheme("go-up"), 'Maximize', self)
        qanor = QAction(QIcon.fromTheme("go-up"), 'AutoCenter AutoResize', self)
        qanor.triggered.connect(self.center)
        qatim = QAction(QIcon.fromTheme("go-up"), 'View Date and Time', self)
        qatim.triggered.connect(self.timedate)
        qabug = QAction(QIcon.fromTheme("help-about"), 'Report a Problem', self)
        qabug.triggered.connect(lambda: qabug.setDisabled(True) if not call(
            'xdg-open mailto:' + 'whnapneybfcnpb@hohagh.pbz'.decode('rot13'),
            shell=True) else ' ERROR ')
        qamax.triggered.connect(lambda: self.showMaximized())
        qaqt = QAction(QIcon.fromTheme("help-about"), 'About Qt', self)
        qaqt.triggered.connect(lambda: QMessageBox.aboutQt(self))
        qakde = QAction(QIcon.fromTheme("help-about"), 'About KDE', self)
        if KDE:
            qakde.triggered.connect(KHelpMenu(self, "", False).aboutKDE)
        qaslf = QAction(QIcon.fromTheme("help-about"), 'About Self', self)
        if KDE:
            qaslf.triggered.connect(
                                KAboutApplicationDialog(aboutData, self).exec_)
        else:
            qaslf.triggered.connect(lambda: QMessageBox.about(self.mainwidget,
            __doc__, ''.join((__doc__, linesep, 'version ', __version__, ', (',
            __license__, '), by ', __author__, ', ( ', __email__, ' )', linesep
            ))))
        qafnt = QAction(QIcon.fromTheme("help-about"), 'Set GUI Font', self)
        if KDE:
            font = QFont()
            qafnt.triggered.connect(lambda:
            self.setStyleSheet(''.join((
                '*{font-family:', str(font.toString()), '}'))
                if KFontDialog.getFont(font)[0] == QDialog.Accepted else ''))
        else:
            qafnt.triggered.connect(lambda:
                self.setStyleSheet(''.join(('*{font-family:',
                            str(QFontDialog.getFont()[0].toString()), '}'))))
        qasrc = QAction(QIcon.fromTheme("applications-development"),
                        'View Source Code', self)
        qasrc.triggered.connect(lambda: call('xdg-open {}'.format(__file__), 1))
        qakb = QAction(QIcon.fromTheme("input-keyboard"),
                       'Keyboard Shortcuts', self)
        qakb.triggered.connect(lambda: QMessageBox.information(self.mainwidget,
                               'Keyboard Shortcuts', ' Ctrl+Q = Quit '))
        qapic = QAction(QIcon.fromTheme("camera-photo"),
                        'Take a Screenshot', self)
        qapic.triggered.connect(lambda: QPixmap.grabWindow(
            QApplication.desktop().winId()).save(QFileDialog.getSaveFileName(
            self.mainwidget, " Save Screenshot As ...", path.expanduser("~"),
            ';;(*.png) PNG', 'png')))
        qatb = QAction(QIcon.fromTheme("help-browser"), 'Toggle ToolBar', self)
        qatb.triggered.connect(lambda: self.toolbar.hide()
                if self.toolbar.isVisible() is True else self.toolbar.show())
        qati = QAction(QIcon.fromTheme("help-browser"),
                       'Switch ToolBar Icon Size', self)
        qati.triggered.connect(lambda:
            self.toolbar.setIconSize(self.toolbar.iconSize() * 4)
            if self.toolbar.iconSize().width() * 4 == 24
            else self.toolbar.setIconSize(self.toolbar.iconSize() / 4))
        qasb = QAction(QIcon.fromTheme("help-browser"), 'Toggle Tabs Bar', self)
        qasb.triggered.connect(lambda: self.mainwidget.tabBar().hide()
                               if self.mainwidget.tabBar().isVisible() is True
                               else self.mainwidget.tabBar().show())
        qadoc = QAction(QIcon.fromTheme("help-browser"), 'On-line Docs', self)
        qadoc.triggered.connect(lambda: open_new_tab(__url__))
        qapy = QAction(QIcon.fromTheme("help-browser"), 'About Python', self)
        qapy.triggered.connect(lambda: open_new_tab('http://python.org/about'))
        qali = QAction(QIcon.fromTheme("help-browser"), 'Read Licence', self)
        qali.triggered.connect(lambda: open_new_tab(__full_licence__))
        qacol = QAction(QIcon.fromTheme("preferences-system"), 'Set GUI Colors',
                        self)
        if KDE:
            color = QColor()
            qacol.triggered.connect(lambda:
                self.setStyleSheet(''.join(('* { background-color: ',
                                            str(color.name()), '}')))
                if KColorDialog.getColor(color, self) else '')
        else:
            qacol.triggered.connect(lambda: self.setStyleSheet(''.join((
                ' * { background-color: ', str(QColorDialog.getColor().name()),
                ' } '))))
        qatit = QAction(QIcon.fromTheme("preferences-system"),
                        'Set the App Window Title', self)
        qatit.triggered.connect(self.seTitle)
        self.toolbar.addWidget(self.left_spacer)
        self.toolbar.addSeparator()
        for b in (qaqq, qamin, qanor, qamax, qasrc, qakb, qacol, qatim, qatb,
            qafnt, qati, qasb, qatit, qapic, qadoc, qali, qaslf, qaqt, qakde,
            qapy, qabug):
            self.toolbar.addAction(b)
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)
        self.toolbar.addSeparator()
        self.toolbar.addWidget(self.right_spacer)

        def contextMenuRequested(point):
            ' quick and dirty custom context menu '
            menu = QMenu()
            menu.addActions((qaqq, qamin, qanor, qamax, qasrc, qakb, qacol,
                qafnt, qati, qasb, qatb, qatim, qatit, qapic, qadoc, qali,
                qaslf, qaqt, qakde, qapy, qabug))
            menu.exec_(self.mapToGlobal(point))
        self.mainwidget.customContextMenuRequested.connect(contextMenuRequested)

        def must_be_checked(widget_list):
            ' widget tuple passed as argument should be checked as ON '
            for each_widget in widget_list:
                try:
                    each_widget.setChecked(True)
                except:
                    pass

        def must_have_tooltip(widget_list):
            ' widget tuple passed as argument should have tooltips '
            for each_widget in widget_list:
                try:
                    each_widget.setToolTip(each_widget.text())
                except:
                    each_widget.setToolTip(each_widget.currentText())
                finally:
                    each_widget.setCursor(QCursor(Qt.PointingHandCursor))

        def must_autofillbackground(widget_list):
            ' widget tuple passed as argument should have filled background '
            for each_widget in widget_list:
                try:
                    each_widget.setAutoFillBackground(True)
                except:
                    pass

        #######################################################################

        # dock 1
        QLabel('<h1 style="color:white;"> Record !</h1>', self.dock1).resize(
               self.dock3.size().width() / 4, 25)
        self.group1 = QGroupBox()
        self.group1.setTitle(__doc__)

        self.lcdNumber = QLCDNumber()
        self.lcdNumber.setFrameShape(QFrame.StyledPanel)
        self.lcdNumber.setNumDigits(4)
        self.lcdNumber.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber.display(666)
        self.lcdNumber.setToolTip(' VUmeter LCD Display ')

        self.lcdNumber2 = QLCDNumber()
        self.lcdNumber2.setFrameShape(QFrame.StyledPanel)
        self.lcdNumber2.setNumDigits(4)
        self.lcdNumber2.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber2.display(666)
        self.lcdNumber2.setToolTip(' VUmeter LCD Display ')

        self.progressBar = QProgressBar()
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(200)
        self.progressBar.setValue(100)
        self.progressBar.setToolTip(' VUmeter ')

        self.progressBar2 = QProgressBar(self)
        self.progressBar2.setMinimum(0)
        self.progressBar2.setMaximum(200)
        self.progressBar2.setValue(100)
        self.progressBar2.setToolTip(' VUmeter ')

        self.clock = QLCDNumber()
        self.clock.setSegmentStyle(QLCDNumber.Flat)
        self.clock.setNumDigits(25)
        self.timer1 = QTimer(self)
        self.timer1.timeout.connect(lambda: self.clock.display(
            datetime.now().strftime("%d-%m-%Y %H:%M:%S %p")))
        self.timer1.start(1000)
        self.clock.setToolTip(datetime.now().strftime("%c %x"))
        self.clock.setCursor(QCursor(Qt.CrossCursor))

        self.diskBar = QProgressBar()
        self.diskBar.setMinimum(0)
        self.diskBar.setMaximum(statvfs(HOME).f_blocks *
            statvfs(HOME).f_frsize / 1024 / 1024 / 1024)
        self.diskBar.setValue(statvfs(HOME).f_bfree *
            statvfs(HOME).f_frsize / 1024 / 1024 / 1024)
        self.diskBar.setToolTip(str(statvfs(HOME).f_bfree *
            statvfs(HOME).f_frsize / 1024 / 1024 / 1024) + ' Gigabytes free')

        self.boton = QPushButton(QIcon.fromTheme("media-record"), 'Record')
        self.boton.clicked.connect(self.run)

        vboxg1 = QVBoxLayout(self.group1)
        for each_widget in (QLabel('<b style="color:white;"> VUMeters '),
            self.progressBar, self.lcdNumber,
            self.progressBar2, self.lcdNumber2,
            QLabel('<b style="color:white;"> Time '), self.clock,
            QLabel('<b style="color:white;"> Disk Space '), self.diskBar,
            QLabel('<b style="color:white;"> Actions '), self.boton):
            vboxg1.addWidget(each_widget)

        self.group2 = QGroupBox()
        self.group2.setTitle(__doc__)

        self.file1 = QLineEdit()
        self.file1.setPlaceholderText('/full/path/to/one_file.py')
        self.file1.setCompleter(self.completer)
        self.borig = QPushButton(QIcon.fromTheme("folder-open"), 'Open')

        self.slider = QSlider(self)
        self.slider.setCursor(QCursor(Qt.ClosedHandCursor))
        self.slider.setMinimum(30)
        self.slider.setMaximum(120)
        self.slider.setValue(30)
        self.slider.setOrientation(Qt.Vertical)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.setTickInterval(30)
        self.slider.setSingleStep(30)
        self.slider.setPageStep(30)

        vboxg2 = QVBoxLayout(self.group2)
        for each_widget in (
            QLabel('<b style="color:white;">MINUTES of recording'), self.slider,
            ):
            vboxg2.addWidget(each_widget)

        group3 = QGroupBox()
        group3.setTitle(__doc__)
        self.label3 = QLabel(str(alsaaudio.cards()).replace("', u'", "<br>"))
        self.label4 = QLabel(str(alsaaudio.mixers()).replace("', u'", "<br>"))
        self.label6 = QLabel(str(getoutput('oggenc --version', shell=1)))
        print((' INFO: Using Cards {}'.format(alsaaudio.cards())))
        print((' INFO: Using Mixers {}'.format(alsaaudio.mixers())))
        vboxg3 = QVBoxLayout(group3)
        for each_widget in (
            QLabel('<b style="color:white;"> Sound Hardware '), self.label3,
            QLabel('<b style="color:white;"> Sound Mixers '), self.label4,
            QLabel('<b style="color:white;"> Off-line Out Codec'), self.label6):
            vboxg3.addWidget(each_widget)
        container = QWidget()
        hbox = QHBoxLayout(container)
        for each_widget in (self.group2, self.group1, group3):
            hbox.addWidget(each_widget)
        self.dock1.setWidget(container)

        # dock 2
        QLabel('<h1 style="color:white;"> Hardware !</h1>', self.dock2).resize(
               self.dock2.size().width() / 4, 25)
        try:
            audioDriverStr = {Solid.AudioInterface.Alsa: "ALSA",
                Solid.AudioInterface.OpenSoundSystem: "Open Sound",
                Solid.AudioInterface.UnknownAudioDriver: "Unknown?"}
            audioInterfaceTypeStr = {
                Solid.AudioInterface.AudioControl: "Control",
                Solid.AudioInterface.UnknownAudioInterfaceType: "Unknown?",
                Solid.AudioInterface.AudioInput: "In",
                Solid.AudioInterface.AudioOutput: "Out"}
            soundcardTypeStr = {
                Solid.AudioInterface.InternalSoundcard: "Internal",
                Solid.AudioInterface.UsbSoundcard: "USB3",
                Solid.AudioInterface.FirewireSoundcard: "FireWire",
                Solid.AudioInterface.Headset: "Headsets",
                Solid.AudioInterface.Modem: "Modem"}
            display = QTreeWidget()
            display.setAlternatingRowColors(True)
            display.setHeaderLabels(["Items", "ID", "Drivers", "I / O", "Type"])
            display.setColumnWidth(0, 350)
            display.setColumnWidth(1, 350)
            display.setColumnWidth(3, 75)
            # retrieve a list of Solid.Device for this machine
            deviceList = Solid.Device.allDevices()
            # filter the list of all devices and display matching results
            # note that we never create a Solid.AudioInterface object, but
            # receive one from the 'asDeviceInterface' call
            for device in deviceList:
                if device.isDeviceInterface(
                                         Solid.DeviceInterface.AudioInterface):
                    audio = device.asDeviceInterface(
                            Solid.DeviceInterface.AudioInterface)
                    devtype = audio.deviceType()
                    devstr = []
                    for key in audioInterfaceTypeStr:
                        flag = key & devtype
                        if flag:
                            devstr.append(audioInterfaceTypeStr[key])
                    QTreeWidgetItem(display, [device.product(), audio.name(),
                        audioDriverStr[audio.driver()], "/".join(devstr),
                        soundcardTypeStr[audio.soundcardType()]])
            self.dock2.setWidget(display)
        except:
            self.dock2.setWidget(QLabel(""" <center style='color:white;'>
            <h1>:(<br>ERROR: Please, install PyKDE !</h1><br>
            <br><i> (Sorry, can not use non-Qt Libs). Thanks </i><center>"""))

        ## dock 3
        QLabel('<h1 style="color:white;"> Previews !</h1>', self.dock3).resize(
               self.dock3.size().width() / 4, 25)
        self.fileView = QColumnView()
        self.fileView.updatePreviewWidget.connect(self.play)
        self.fileView.setToolTip(' Browse and Preview Files ')
        self.media = None
        self.model = QDirModel()
        self.fileView.setModel(self.model)
        self.dock3.setWidget(self.fileView)

        # dock4
        QLabel('<h1 style="color:white;"> Setup !</h1>', self.dock4).resize(
               self.dock4.size().width() / 4, 25)
        self.group4 = QGroupBox()
        self.group4.setTitle(__doc__)

        self.dial = QDial()
        self.dial.setCursor(QCursor(Qt.ClosedHandCursor))
        self.dial.setMinimum(0)
        self.dial.setMaximum(9)
        self.dial.setValue(0)
        self.dial.setWrapping(False)
        self.dial.setNotchesVisible(True)

        self.combo1 = QComboBox()
        self.combo1.addItems(['OGG', 'STDOUT (For Debug)'])

        self.combo2 = QComboBox()
        self.combo2.addItems(['128', '256', '512', '1024', '64', '32', '16'])

        self.combo3 = QComboBox(self)
        self.combo3.addItems(['MONO', 'STEREO', 'Surround'])

        self.combo4 = QComboBox()
        self.combo4.addItems(['44100', '96000', '48000', '32000',
                              '22050', '16000', '11025', '8000'])

        self.combo5 = QComboBox(self)
        self.combo5.addItems(['SMART', 'FORCE'])

        self.nepochoose = QCheckBox('Auto-Tag Files using Nepomuk Semantic')

        vboxg4 = QVBoxLayout(self.group4)
        for each_widget in (
            QLabel('<b style="color:white;">THRESHOLD of Recording'), self.dial,
            QLabel('<b style="color:white;"> Sound Output Format'), self.combo1,
            QLabel('<b style="color:white;"> Sound KBps '), self.combo2,
            QLabel('<b style="color:white;"> Sound Channels '), self.combo3,
            QLabel('<b style="color:white;"> Sound Sample Rate '), self.combo4,
            QLabel('<b style="color:white;">Detection Recording'), self.combo5,
            QLabel('<b style="color:white;">Nepomuk Semantic User Experience'),
            self.nepochoose):
            vboxg4.addWidget(each_widget)
        self.dock4.setWidget(self.group4)

        # configure some widget settings
        must_be_checked((self.nepochoose, ))
        must_have_tooltip((self.label3, self.label4, self.label6,
            self.nepochoose, self.combo1, self.combo2, self.combo3,
            self.combo4, self.combo5, self.boton))
        must_autofillbackground((self.lcdNumber2, self.lcdNumber, self.clock,
            self.label3, self.label4, self.label6, self.nepochoose))

    def play(self, index):
        ' play with delay '
        if not self.media:
            self.media = Phonon.MediaObject(self)
            audioOutput = Phonon.AudioOutput(Phonon.MusicCategory, self)
            Phonon.createPath(self.media, audioOutput)
        self.media.setCurrentSource(Phonon.MediaSource(
            self.model.filePath(index)))
        self.media.play()

    def run(self):
        ' run forest run '
        print((' INFO: Working at {}'.format(str(datetime.now()))))
        channels = 1 if self.combo3.currentText() == 'MONO' else 2
        print((' INFO: Using {} Channels . . . '.format(channels)))
        bitrate = int(self.combo4.currentText())
        print((' INFO: Using {} Hz per Second . . . '.format(bitrate)))
        threshold = int(self.dial.value())
        print((' INFO: Using Thresold of {} . . . '.format(threshold)))
        record_seconds = int(self.slider.value()) * 60
        print((' INFO: Using Recording time of {} ...'.format(record_seconds)))
        # make base directory
        try:
            mkdir(self.base)
            print((' INFO: Base Directory path created {}'.format(self.base)))
        except OSError:
            print((' INFO: Base Directory already exist {}'.format(self.base)))
        except:
            print((' ERROR: Can not create Directory ?, {}'.format(self.base)))
        # make directory tree
        try:
            for dr in range(1, 13):
                mkdir(path.abspath(path.join(self.base, str(dr))))
                print((' INFO:Directory created {}/{}'.format((self.base, dr))))
        except OSError:
            print((' INFO: Directory already exist {}/1,12'.format(self.base)))
        except:
            print((' ERROR: Cant create Directory?, {}/1,12'.format(self.base)))
        # convert to ogg the old wav files
        self.convertOGG()
        # VUMeter
        inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE)
        inp.setrate(bitrate)
        inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
        inp.setperiodsize(1024)
        # recording loop
        while True:
            filename = path.abspath(path.join(self.base,
                       str(datetime.now().month),
                       datetime.now().strftime("%Y-%m-%d_%H:%M:%S.wav")))
            print((' INFO: Recording on the file {}'.format(filename)))
            print((' INFO: Loop of {}'.format(bitrate / 1024 * record_seconds)))
            print(('-' * 80))
            w = wave.open(filename, 'w')
            w.setnchannels(channels)
            w.setsampwidth(2)
            w.setframerate(bitrate)
            for i in range(0, bitrate / 1024 * record_seconds):
                l, data = inp.read()
                a = int(numpy.abs(numpy.fromstring(data, dtype='int16').mean()))
                a = a * 4
                # Feedback to the GUI and CLI
                # print((i, a))
                self.progressBar.setValue(a)
                self.progressBar2.setValue(a)
                self.lcdNumber.display(a)
                self.lcdNumber2.display(a)
                # compares THRESHOLD versus a so only record if sound
                if self.combo5.currentText() == 'SMART' and a <= threshold:
                    continue
                # force recording, even if its silent
                else:
                    w.writeframes(data) if self.combo1.currentText() == 'OGG' \
                        else repr(data)
            w.close()

    def convertOGG(self):
        ' convert to ogg files '
        # convert WAV to compressed .OGG files
        try:
            print(' INFO: Compressing sound into .OGG files . . . ')
            [call(''.join(('nice --adjustment=20 oggenc ', path.abspath(a))), shell=True) for a in iter(["{}/{}".format(root, f) for root, f in list(chain(*[list(product([root], files)) for root, dirs, files in walk(self.base)])) if f.endswith(('.wav', '.WAV')) and not f.startswith('.')])]
            print(' INFO: Deleting uncompressed sound files . . . ')
            [remove(a) for a in iter(["{}/{}".format(root, f) for root, f in list(chain(*[list(product([root], files)) for root, dirs, files in walk(self.base)])) if f.endswith(('.wav', '.WAV')) and not f.startswith('.')])]
        except:
            print((' ERROR: Cant Convert PCM to OGG files? ', linesep,
                   ' ERROR: oggenc not found installed ??? ', linesep,
                   ' ( sudo apt-get install vorbis-tools ) ', linesep))
        if self.nepochoose.isChecked() is True:
            try:
                print(' INFO: Semantic User Experience is Auto-Tagging files ')
                [self.nepomuk_set(a, 'testigo', 'testigo', 'Auto-Tagged file by Cinta-Testigo') for a in iter(["{}/{}".format(root, f) for root, f in list(chain(*[list(product([root], files)) for root, dirs, files in walk(self.base)])) if f.endswith(('.ogg', '.OGG')) and not f.startswith('.')])]
                print(' INFO: Semantic User Experience Query files. . . ')
                self.nepomuk_get('testigo')
            except:
                print((' ERROR: Cant use Semantic User Experience on file', linesep,
                       ' ERROR: Nepomuk not found installed ??? ', linesep,
                       ' ( sudo apt-get install python-kde4 ) ', linesep))

    ###########################################################################

    def paintEvent(self, event):
        'Paint semi-transparent background, animated pattern, background text'
        # because we are on 2012 !, its time to showcase how Qt we are !
        QWidget.paintEvent(self, event)
        # make a painter
        p = QPainter(self)
        p.setRenderHint(QPainter.TextAntialiasing)
        p.setRenderHint(QPainter.HighQualityAntialiasing)
        # fill a rectangle with transparent painting
        p.fillRect(event.rect(), Qt.transparent)
        # animated random dots background pattern
        for i in range(4096):
            x = randint(9, self.size().width() - 9)
            y = randint(9, self.size().height() - 9)
            p.setPen(QPen(QColor(randint(9, 255), randint(9, 255), 255), 1))
            p.drawPoint(x, y)
        # set pen to use white color
        p.setPen(QPen(QColor(randint(9, 255), randint(9, 255), 255), 1))
        # Rotate painter 45 Degree
        p.rotate(35)
        # Set painter Font for text
        p.setFont(QFont('Ubuntu', 200))
        # draw the background text, with antialiasing
        p.drawText(99, 99, "Radio")
        # Rotate -45 the QPen back !
        p.rotate(-35)
        # set the pen to no pen
        p.setPen(Qt.NoPen)
        # Background Color
        p.setBrush(QColor(0, 0, 0))
        # Background Opacity
        p.setOpacity(0.75)
        # Background Rounded Borders
        p.drawRoundedRect(self.rect(), 50, 50)
        # finalize the painter
        p.end()

    def seTitle(self):
        ' set the title of the main window '
        dialog = QDialog(self)
        textEditInput = QLineEdit(' Type Title Here ')
        ok = QPushButton(' O K ')
        ok.clicked.connect(lambda: self.setWindowTitle(textEditInput.text()))
        ly = QVBoxLayout()
        [ly.addWidget(wdgt) for wdgt in (QLabel('Title:'), textEditInput, ok)]
        dialog.setLayout(ly)
        dialog.exec_()

    def timedate(self):
        ' get the time and date '
        dialog = QDialog(self)
        clock = QLCDNumber()
        clock.setNumDigits(24)
        timer = QTimer()
        timer.timeout.connect(lambda: clock.display(
            datetime.now().strftime("%d-%m-%Y %H:%M:%S %p")))
        timer.start(1000)
        clock.setToolTip(datetime.now().strftime("%c %x"))
        ok = QPushButton(' O K ')
        ok.clicked.connect(dialog.close)
        ly = QVBoxLayout()
        [ly.addWidget(wdgt) for wdgt in (QCalendarWidget(), clock, ok)]
        dialog.setLayout(ly)
        dialog.exec_()

    def closeEvent(self, event):
        ' Ask to Quit '
        if QMessageBox.question(self, ' Close ', ' Quit ? ',
           QMessageBox.Yes | QMessageBox.No, QMessageBox.No) == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def center(self):
        ' Center and resize the window '
        self.resize(QDesktopWidget().screenGeometry().width() // 1.25,
                    QDesktopWidget().screenGeometry().height() // 1.25)
        qr = self.frameGeometry()
        qr.moveCenter(QDesktopWidget().availableGeometry().center())
        self.move(qr.topLeft())

    def nepomuk_set(self, file_tag=None, __tag='', _label='', _description=''):
        ' Quick and Easy Nepomuk Taggify for Files '
        if Nepomuk.ResourceManager.instance().init() is 0:
            fle = Nepomuk.Resource(KUrl(QFileInfo(file_tag).absoluteFilePath()))
            _tag = Nepomuk.Tag(__tag)
            _tag.setLabel(_label)
            fle.addTag(_tag)
            fle.setDescription(_description)
            print(([str(a.label()) for a in fle.tags()], fle.description()))
            return ([str(a.label()) for a in fle.tags()], fle.description())
        else:
            print(" ERROR: FAIL: Nepomuk is not running ! ")
            return

    def nepomuk_get(self, query_to_search):
        ' Quick and Easy Nepomuk Query for Files '
        results = []
        nepo = Nepomuk.Query.QueryServiceClient()
        nepo.desktopQuery("hasTag:{}".format(query_to_search))

        def _query(data):
            ''' ('filename.ext', 'file description', ['list', 'of', 'tags']) '''
            results.append(([str(a.resource().genericLabel()) for a in data][0],
                            [str(a.resource().description()) for a in data][0],
            [str(a.label()) for a in iter([a.resource().tags() for a in data][0]
            )]))
        nepo.newEntries.connect(_query)

        def _end():
            '''
            [  ('filename.ext', 'file description', ['list', 'of', 'tags']),
               ('filename.ext', 'file description', ['list', 'of', 'tags']),
               ('filename.ext', 'file description', ['list', 'of', 'tags'])  ]
            '''
            nepo.newEntries.disconnect
            print(results)
            return results
        nepo.finishedListing.connect(_end)


###############################################################################


def main():
    ' Main Loop '
    from getopt import getopt
    OPAQUE = True
    BORDER = True
    try:
        opts, args = getopt(sys.argv[1:], 'hvob',
                                   ['version', 'help', 'opaque', 'border'])
        pass
    except:
        pass
    for o, v in opts:
        if o in ('-h', '--help'):
            print('''
            Usage:
                  -h, --help        Show help informations and exit.
                  -v, --version     Show version information and exit.
                  -o, --opaque      Use Opaque GUI.
                  -b, --border      Use WM Borders.
                  Run without parameters and arguments to use the GUI.
            ''')
            return sys.exit(1)
        elif o in ('-v', '--version'):
            print(__version__)
            return sys.exit(1)
        elif o in ('-o', '--opaque'):
                OPAQUE = False
        elif o in ('-b', '--border'):
                BORDER = False
    # define our App
    app = QApplication(sys.argv)
    app.setApplicationName(__doc__)
    app.setOrganizationName(__author__)
    app.setOrganizationDomain(__author__)
    # w is gonna be the mymainwindow class
    w = MyMainWindow()
    # set the class with the attribute of translucent background as true
    if OPAQUE is True:
        w.setAttribute(Qt.WA_TranslucentBackground, True)
    # WM Borders
    if BORDER is True:
        w.setWindowFlags(w.windowFlags() | Qt.FramelessWindowHint)
    # run the class
    w.show()
    # if exiting the loop take down the app
    sys.exit(app.exec_())


if __name__ == '__main__':
    ' Do NOT add anything here!, use main() function instead. '
    main()
