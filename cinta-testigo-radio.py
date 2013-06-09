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
__version__ = ' 1.0 '
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
from os import (path, linesep, geteuid, environ, statvfs, mkdir, getcwd)
from datetime import datetime
from subprocess import call
from random import randint
from webbrowser import open_new_tab
from shutil import make_archive
from subprocess import check_output as getoutput
from getpass import getuser
from sip import setapi

try:
    from PyQt4.QtGui import (QIcon, QLabel, QFileDialog, QWidget, QVBoxLayout,
        QHBoxLayout, QComboBox, QCursor, QLineEdit, QCheckBox, QPushButton,
        QGroupBox, QMessageBox, QCompleter, QDirModel, QLCDNumber, QAction,
        QFont, QTabWidget, QDockWidget, QToolBar, QSizePolicy, QColorDialog,
        QPalette, QPen, QPainter, QColor, QPixmap, QMenu, QDialog, QSlider,
        QDesktopWidget, QProgressBar, QMainWindow, QApplication, QTreeWidget,
        QTreeWidgetItem, QColumnView, QDial, QTabBar, QGraphicsDropShadowEffect,
        QSystemTrayIcon)

    from PyQt4.QtCore import (Qt, QDir, QSize, QUrl, QEvent,
                              QTimer, QFileInfo, QProcess)

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


class TabBar(QTabBar):
    ' custom tab bar '
    def __init__(self, parent):
        ' init class custom tab bar '
        QTabBar.__init__(self, parent)
        self._editor = QLineEdit(self)
        self._editor.setToolTip(' Type a Tab Name ')
        self._editor.setWindowFlags(Qt.Popup)
        self._editor.setFocusProxy(self)
        self._editor.editingFinished.connect(self.handleEditingFinished)
        self._editor.installEventFilter(self)

    def eventFilter(self, widget, event):
        ' filter mouse, esc key,  events '
        if ((event.type() == QEvent.MouseButtonPress and
             not self._editor.geometry().contains(event.globalPos())) or
            (event.type() == QEvent.KeyPress and
             event.key() == Qt.Key_Escape)):
            self._editor.hide()
            return True
        return QTabBar.eventFilter(self, widget, event)

    def mouseDoubleClickEvent(self, event):
        ' handle double click '
        index = self.tabAt(event.pos())
        if index >= 0:
            self.editTab(index)

    def editTab(self, index):
        ' handle the editor '
        rect = self.tabRect(index)
        self._editor.setFixedSize(rect.size())
        self._editor.move(self.parent().mapToGlobal(rect.topLeft()))
        self._editor.setText(self.tabText(index))
        if not self._editor.isVisible():
            self._editor.show()

    def handleEditingFinished(self):
        ' set text when editing has finished '
        index = self.currentIndex()
        if index >= 0:
            self._editor.hide()
            self.setTabText(index, self._editor.text())


###############################################################################


class MyMainWindow(QMainWindow):
    ' Main Window '
    def __init__(self, AUTO):
        ' Initialize QWidget inside MyMainWindow '
        super(MyMainWindow, self).__init__()
        QWidget.__init__(self)
        self.auto = AUTO
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

        # process
        self.process1 = None
        self.process2 = None
        self.cmd1 = 'nice -n {n} arecord{v} -f {f} -c {c} -r {b} -t raw'
        self.cmd2 = 'oggenc - -r -C {c} -R {b} -q {q} {d}{t}{a} -o {o}'
        self.process3 = QProcess(self)
        #self.process3.finished.connect(self.on_process3_finished)
        #self.process3.error.connect(self.on_process3_error)

        self.cmd3 = ('nice -n 20 ' +
          'sox "{o}" -n spectrogram -x {x} -y {y} -z 99 -t "{o}" -o "{o}.png"')
        self.actual_file = ''

        # re starting timers, one stops, one starts
        self.timerFirst = QTimer(self)
        self.timerFirst.timeout.connect(self.end)
        self.timerSecond = QTimer(self)
        self.timerSecond.timeout.connect(self.run)

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
        self.mainwidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.mainwidget.setStyleSheet('QTabBar{color:white;font-weight:bold;}')
        self.mainwidget.setTabBar(TabBar(self))
        self.mainwidget.setTabsClosable(False)
        self.setCentralWidget(self.mainwidget)
        self.dock1 = QDockWidget()
        self.dock2 = QDockWidget()
        self.dock3 = QDockWidget()
        self.dock4 = QDockWidget()
        self.dock5 = QDockWidget()
        for a in (self.dock1, self.dock2, self.dock3, self.dock4, self.dock5):
            a.setWindowModality(Qt.NonModal)
            # a.setWindowOpacity(0.9)
            a.setWindowTitle(__doc__
                             if a.windowTitle() == '' else a.windowTitle())
            a.setStyleSheet('QDockWidget::title{text-align:center;}')
            self.mainwidget.addTab(a, QIcon.fromTheme("face-smile"),
                                   'Double Click Me')

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
        qanor = QAction(QIcon.fromTheme("view-fullscreen"),
                        'AutoCenter AutoResize', self)
        qanor.triggered.connect(self.center)
        qatim = QAction(QIcon.fromTheme("mail-signed-verified"),
                        'View Date and Time', self)
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
        qafnt = QAction(QIcon.fromTheme("tools-check-spelling"),
                        'Set GUI Font', self)
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
        qasrc.triggered.connect(lambda:
                            call('xdg-open {}'.format(__file__), shell=True))
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
        qatb = QAction(QIcon.fromTheme("go-top"), 'Toggle ToolBar', self)
        qatb.triggered.connect(lambda: self.toolbar.hide()
                if self.toolbar.isVisible() is True else self.toolbar.show())
        qati = QAction(QIcon.fromTheme("zoom-in"),
                       'Switch ToolBar Icon Size', self)
        qati.triggered.connect(lambda:
            self.toolbar.setIconSize(self.toolbar.iconSize() * 4)
            if self.toolbar.iconSize().width() * 4 == 24
            else self.toolbar.setIconSize(self.toolbar.iconSize() / 4))
        qasb = QAction(QIcon.fromTheme("preferences-other"),
                       'Toggle Tabs Bar', self)
        qasb.triggered.connect(lambda: self.mainwidget.tabBar().hide()
                               if self.mainwidget.tabBar().isVisible() is True
                               else self.mainwidget.tabBar().show())
        qadoc = QAction(QIcon.fromTheme("help-browser"), 'On-line Docs', self)
        qadoc.triggered.connect(lambda: open_new_tab(str(__url__).strip()))
        qapy = QAction(QIcon.fromTheme("help-about"), 'About Python', self)
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
        self.toolbar.addActions((qaqq, qamin, qanor, qamax, qasrc, qakb, qacol,
            qatim, qatb, qafnt, qati, qasb, qatit, qapic, qadoc, qali, qaslf,
            qaqt, qakde, qapy, qabug))
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)
        self.toolbar.addSeparator()
        self.toolbar.addWidget(self.right_spacer)
        # define the menu
        menu = self.menuBar()
        # File menu items
        menu.addMenu('&File').addActions((qaqq, ))
        menu.addMenu('&Window').addActions((qamax, qanor, qamin))
        # Settings menu
        menu.addMenu('&Settings').addActions((qasrc, qacol, qafnt, qatim,
                                              qatb, qati, qasb, qapic))
        # Help menu items
        menu.addMenu('&Help').addActions((qadoc, qakb, qabug, qali,
                                          qaqt, qakde, qapy, qaslf))
        # Tray Icon
        tray = QSystemTrayIcon(QIcon.fromTheme("face-devilish"), self)
        tray.setToolTip(__doc__)
        traymenu = QMenu()
        traymenu.addActions((qamax, qanor, qamin, qaqq))
        tray.setContextMenu(traymenu)
        tray.show()

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

        def must_glow(widget_list):
            ' apply an glow effect to the widget '
            for glow, each_widget in enumerate(widget_list):
                try:
                    if each_widget.graphicsEffect() is None:
                        glow = QGraphicsDropShadowEffect(self)
                        glow.setOffset(0)
                        glow.setBlurRadius(99)
                        glow.setColor(QColor(99, 255, 255))
                        each_widget.setGraphicsEffect(glow)
                        # glow.setEnabled(False)
                        try:
                            each_widget.clicked.connect(lambda:
                            each_widget.graphicsEffect().setEnabled(True)
                            if each_widget.graphicsEffect().isEnabled() is False
                            else each_widget.graphicsEffect().setEnabled(False))
                        except:
                            each_widget.sliderPressed.connect(lambda:
                            each_widget.graphicsEffect().setEnabled(True)
                            if each_widget.graphicsEffect().isEnabled() is False
                            else each_widget.graphicsEffect().setEnabled(False))
                except:
                    pass

        #######################################################################

        # dock 1
        QLabel('<h1 style="color:white;"> Record !</h1>', self.dock1).resize(
               self.dock3.size().width() / 4, 25)
        self.group1 = QGroupBox()
        self.group1.setTitle(__doc__)

        self.spec = QPushButton(self)
        self.spec.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.spec.setMinimumSize(self.spec.size().width(), 250)
        self.spec.setFlat(True)
        self.spec.clicked.connect(self.spectro)

        self.clock = QLCDNumber()
        self.clock.setSegmentStyle(QLCDNumber.Flat)
        self.clock.setMinimumSize(self.clock.size().width(), 50)
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

        self.feedback = QPlainTextEdit(''.join(('<center><h3>', __doc__,
            ', version', __version__, __license__, ' <br> by ', __author__,
            ' <i>(Dev)</i>, Radio Comunitaria FM Reconquista <i>(Q.A.)</i><br>',
            'FMReconquista.org.ar & GitHub.com/JuanCarlosPaco/Cinta-Testigo')))

        self.rec = QPushButton(QIcon.fromTheme("media-record"), 'Record')
        self.rec.setMinimumSize(self.rec.size().width(), 50)
        self.rec.clicked.connect(self.go)  # self.run

        self.stop = QPushButton(QIcon.fromTheme("media-playback-stop"), 'Stop')
        self.stop.clicked.connect(self.end)

        self.kill = QPushButton(QIcon.fromTheme("process-stop"), 'Kill')
        self.kill.clicked.connect(self.killer)

        vboxg1 = QVBoxLayout(self.group1)
        for each_widget in (
            QLabel('<b style="color:white;"> Spectro'), self.spec,
            QLabel('<b style="color:white;"> Time '), self.clock,
            QLabel('<b style="color:white;"> Disk '), self.diskBar,
            QLabel('<b style="color:white;"> STDOUT + STDIN '), self.feedback,
            QLabel('<b style="color:white;"> Record '), self.rec, self.stop,
            self.kill):
            vboxg1.addWidget(each_widget)

        self.group2 = QGroupBox()
        self.group2.setTitle(__doc__)

        self.slider = QSlider(self)
        self.slid_l = QLabel(self.slider)
        self.slider.setCursor(QCursor(Qt.OpenHandCursor))
        self.slider.sliderPressed.connect(lambda:
                            self.slider.setCursor(QCursor(Qt.ClosedHandCursor)))
        self.slider.sliderReleased.connect(lambda:
                            self.slider.setCursor(QCursor(Qt.OpenHandCursor)))
        self.slider.valueChanged.connect(lambda:
                            self.slider.setToolTip(str(self.slider.value())))
        self.slider.valueChanged.connect(lambda: self.slid_l.setText(
                    '<h2 style="color:white;">{}'.format(self.slider.value())))
        self.slider.setMinimum(10)
        self.slider.setMaximum(99)
        self.slider.setValue(30)
        self.slider.setOrientation(Qt.Vertical)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.setTickInterval(2)
        self.slider.setSingleStep(10)
        self.slider.setPageStep(10)

        vboxg2 = QVBoxLayout(self.group2)
        for each_widget in (
            QLabel('<b style="color:white;">MINUTES of recording'), self.slider,
            QLabel('<b style="color:white;"> Default: 30 Min')):
            vboxg2.addWidget(each_widget)

        group3 = QGroupBox()
        group3.setTitle(__doc__)
        self.label2 = QLabel(getoutput('sox --version', shell=True))
        self.label4 = QLabel(getoutput('arecord --version', shell=True)[:25])
        self.label6 = QLabel(str(getoutput('oggenc --version', shell=True)))

        self.button5 = QPushButton(QIcon.fromTheme("audio-x-generic"),
                                   'OGG --> ZIP')
        self.button5.clicked.connect(lambda: make_archive(
            str(QFileDialog.getSaveFileName(self, "Save OGG to ZIP file As...",
            getcwd(), ';;(*.zip)', 'zip')).replace('.zip', ''), "zip",
            path.abspath(path.join(getcwd(), str(datetime.now().year)))))

        self.button1 = QPushButton(QIcon.fromTheme("folder-open"), 'Files')
        self.button1.clicked.connect(lambda:
                                     call('xdg-open ' + getcwd(), shell=True))

        self.button0 = QPushButton(
            QIcon.fromTheme("preferences-desktop-screensaver"), 'LCD OFF')
        self.button0.clicked.connect(lambda:
            call('sleep 3 ; xset dpms force off', shell=True))

        vboxg3 = QVBoxLayout(group3)
        for each_widget in (
            QLabel('<b style="color:white;"> OGG Output Codec '), self.label6,
            QLabel('<b style="color:white;"> Raw Record Backend '), self.label4,
            QLabel('<b style="color:white;"> Helper Libs '), self.label2,
            QLabel('<b style="color:white;"> OGG ZIP '), self.button5,
            QLabel('<b style="color:white;"> Files '), self.button1,
            QLabel('<b style="color:white;"> LCD '), self.button0):
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

        self.combo0 = QComboBox()
        self.combo0.addItems(['S16_LE', 'S32_LE', 'S16_BE', 'U16_LE', 'U16_BE',
          'S24_LE', 'S24_BE', 'U24_LE', 'U24_BE', 'S32_BE', 'U32_LE', 'U32_BE'])

        self.combo1 = QComboBox()
        self.combo1.addItems(['1', '-1', '0', '2', '3', '4',
                              '5', '6', '7', '8', '9', '10'])

        self.combo2 = QComboBox()
        self.combo2.addItems(['128', '256', '512', '1024', '64', '32', '16'])

        self.combo3 = QComboBox(self)
        self.combo3.addItems(['MONO', 'STEREO', 'Surround'])

        self.combo4 = QComboBox()
        self.combo4.addItems(['44100', '96000', '48000', '32000',
                              '22050', '16000', '11025', '8000'])

        self.combo5 = QComboBox(self)
        self.combo5.addItems(['20', '19', '18', '17', '16', '15', '14', '13',
            '12', '10', '9', '8', '7', '6', '5', '4', '3', '2', '1', '0'])

        self.nepochoose = QCheckBox('Auto-Tag Files using Nepomuk Semantic')

        self.chckbx0 = QCheckBox('Disable Software based Volume Control')

        self.chckbx1 = QCheckBox('Output Sound Stereo-to-Mono Downmix')

        self.chckbx2 = QCheckBox('Add Date and Time MetaData to Sound files')

        self.chckbx3 = QCheckBox('Add Yourself as the Author Artist of Sound')

        vboxg4 = QVBoxLayout(self.group4)
        for each_widget in (
            QLabel('<b style="color:white;"> Sound OGG Quality'), self.combo1,
            QLabel('<b style="color:white;"> Sound Record Format'), self.combo0,
            QLabel('<b style="color:white;"> Sound KBps '), self.combo2,
            QLabel('<b style="color:white;"> Sound Channels '), self.combo3,
            QLabel('<b style="color:white;"> Sound Sample Rate '), self.combo4,
            QLabel('<b style="color:white;"> Sound Volume'), self.chckbx0,
            QLabel('<b style="color:white;"> Sound Mix'), self.chckbx1,
            QLabel('<b style="color:white;"> Sound Meta'), self.chckbx2,
            QLabel('<b style="color:white;"> Sound Authorship'), self.chckbx3,
            QLabel('<b style="color:white;"> CPUs Priority'), self.combo5,
            QLabel('<b style="color:white;">Nepomuk Semantic User Experience'),
            self.nepochoose):
            vboxg4.addWidget(each_widget)
        self.dock4.setWidget(self.group4)

        # dock 5
        QLabel('<h1 style="color:white;"> Voice Changer ! </h1>', self.dock5
               ).resize(self.dock5.size().width() / 3, 25)
        self.group5 = QGroupBox()
        self.group5.setTitle(__doc__)

        self.dial = QDial()
        self.dial.setCursor(QCursor(Qt.OpenHandCursor))
        self.di_l = QLabel(self.dial)
        self.di_l.resize(self.dial.size() / 8)
        self.dial.sliderPressed.connect(lambda:
                            self.dial.setCursor(QCursor(Qt.ClosedHandCursor)))
        self.dial.sliderReleased.connect(lambda:
                            self.dial.setCursor(QCursor(Qt.OpenHandCursor)))
        self.dial.valueChanged.connect(lambda:
                            self.dial.setToolTip(str(self.dial.value())))
        self.dial.valueChanged.connect(lambda: self.di_l.setText(
                    '<h1 style="color:white;">{}'.format(self.dial.value())))
        self.dial.setValue(0)
        self.dial.setMinimum(-999)
        self.dial.setMaximum(999)
        self.dial.setSingleStep(100)
        self.dial.setPageStep(100)
        self.dial.setWrapping(False)
        self.dial.setNotchesVisible(True)

        self.defo = QPushButton(QIcon.fromTheme("media-playback-start"), 'Run')
        self.defo.setMinimumSize(self.defo.size().width(), 50)
        self.defo.clicked.connect(lambda: self.process3.start(
            'play -q -V0 "|rec -q -V0 -n -d -R riaa pitch {} reverb"'
            .format(self.dial.value()) if int(self.dial.value()) != 0 else
            'play -q -V0 "|rec -q -V0 --multi-threaded -n -d -R bend {} "'
            .format(' 3,2500,3 3,-2500,3 ' * 999)))

        self.qq = QPushButton(QIcon.fromTheme("media-playback-stop"), 'Stop')
        self.qq.clicked.connect(self.process3.kill)

        self.die = QPushButton(QIcon.fromTheme("process-stop"), 'Kill')
        self.die.clicked.connect(lambda: call('killall rec', shell=True))

        vboxg5 = QVBoxLayout(self.group5)
        for each_widget in (self.dial, self.defo, self.qq, self.die):
            vboxg5.addWidget(each_widget)
        self.dock5.setWidget(self.group5)

        # configure some widget settings
        must_be_checked((self.nepochoose, self.chckbx1,
                         self.chckbx2, self.chckbx3))
        must_have_tooltip((self.label2, self.label4, self.label6, self.combo0,
            self.nepochoose, self.combo1, self.combo2, self.combo3, self.combo4,
            self.combo5, self.chckbx0, self.chckbx1, self.chckbx2, self.chckbx3,
            self.rec, self.stop, self.defo, self.qq, self.die, self.kill,
            self.button0, self.button1, self.button5))
        must_autofillbackground((self.clock, self.label2, self.label4,
            self.label6, self.nepochoose, self.chckbx0, self.chckbx1,
            self.chckbx2, self.chckbx3))
        must_glow((self.rec, self.dial, self.combo1))
        self.nepomuk_get('testigo')
        if self.auto is True:
            self.go()

    def play(self, index):
        ' play with delay '
        if not self.media:
            self.media = Phonon.MediaObject(self)
            audioOutput = Phonon.AudioOutput(Phonon.MusicCategory, self)
            Phonon.createPath(self.media, audioOutput)
        self.media.setCurrentSource(Phonon.MediaSource(
            self.model.filePath(index)))
        self.media.play()

    def end(self):
        ' kill it with fire '
        print((' INFO: Stoping Processes at {}'.format(str(datetime.now()))))
        self.feedback.setText(u'''
            <h5>Errors for RECORDER QProcess 1:</h5>{}<hr>
            <h5>Errors for ENCODER QProcess 2:</h5>{}<hr>
            <h5>Output for RECORDER QProcess 1:</h5>{}<hr>
            <h5>Output for ENCODER QProcess 2:</h5>{}<hr>
            '''.format(self.process1.readAllStandardError(),
                       self.process2.readAllStandardError(),
                       self.process1.readAllStandardOutput(),
                       self.process2.readAllStandardOutput(),
        ))
        self.process1.terminate()
        self.process2.terminate()
        self.process1.kill()
        self.process2.kill()

    def killer(self):
        ' kill -9 '
        QMessageBox.information(self.mainwidget, __doc__,
            ' KILL -9 was sent to the multi-process backend ! ')
        self.process1.kill()
        self.process2.kill()

    def go(self):
        ' run timeout re-starting timers '
        self.timerFirst.start(int(self.slider.value()) * 60 * 1000)
        self.timerSecond.start(int(self.slider.value()) * 60 * 1000 + 1000)
        self.run()

    def run(self):
        ' run forest run '
        print((' INFO: Working at {}'.format(str(datetime.now()))))

        chnl = 1 if self.combo3.currentText() == 'MONO' else 2
        print((' INFO: Using {} Channels . . . '.format(chnl)))

        btrt = int(self.combo4.currentText())
        print((' INFO: Using {} Hz per Second . . . '.format(btrt)))

        threshold = int(self.dial.value())
        print((' INFO: Using Thresold of {} . . . '.format(threshold)))

        print((' INFO: Using Recording time of {}'.format(self.slider.value())))

        frmt = str(self.combo0.currentText()).strip()
        print((' INFO: Using Recording quality of {} ...'.format(frmt)))

        qlt = str(self.combo1.currentText()).strip()
        print((' INFO: Using Recording quality of {} ...'.format(qlt)))

        prio = str(self.combo5.currentText()).strip()
        print((' INFO: Using CPU Priority of {} ...'.format(prio)))

        downmix = '--downmix ' if self.chckbx1.isChecked() is True else ''
        print((' INFO: Using Downmix is {} ...'.format(downmix)))

        aut = '-a ' + getuser() if self.chckbx3.isChecked() is True else ''
        print((' INFO: The Author Artist of this sound is: {}'.format(aut)))

        T = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        tim = '--date {} '.format(T) if self.chckbx2.isChecked() is True else ''
        print((' INFO: The Date and Time of this sound is: {}'.format(tim)))

        vol = ' --disable-softvol' if self.chckbx0.isChecked() is True else ''
        print((' INFO: Software based Volume Control is: {}'.format(vol)))

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
                print((' INFO:Directory created {}/{}'.format(self.base, dr)))
        except OSError:
            print((' INFO: Directory already exist {}/1,12'.format(self.base)))
        except:
            print((' ERROR: Cant create Directory?, {}/1,12'.format(self.base)))

        # make new filename
        flnm = path.abspath(path.join(self.base, str(datetime.now().month),
                   datetime.now().strftime("%Y-%m-%d_%H:%M:%S.ogg")))
        self.actual_file = flnm
        print((' INFO: Recording on the file {}'.format(flnm)))

        # make custom commands
        cmd1 = self.cmd1.format(n=prio, f=frmt, c=chnl, b=btrt, v=vol)
        cmd2 = self.cmd2.format(c=chnl, b=btrt, q=qlt,
                                d=downmix, o=flnm, a=aut, t=tim)
        print((cmd1, cmd2))
        #  multiprocess recording loop pipe
        self.process1 = QProcess(self)
        self.process2 = QProcess(self)
        self.process1.setStandardOutputProcess(self.process2)
        self.process1.start(cmd1)
        if not self.process1.waitForStarted():
            print((" ERROR: RECORDER QProcess 1 Failed: \n {}   ".format(cmd1)))
        self.process2.start(cmd2)
        if not self.process2.waitForStarted():
            print((" ERROR: ENCODER QProcess 2 Failed: \n   {} ".format(cmd2)))
        self.nepomuk_set(flnm, 'testigo', 'testigo', 'AutoTag by Cinta-Testigo')

    def spectro(self):
        ' spectrometer '
        wid = self.spec.size().width()
        hei = self.spec.size().height()
        command = self.cmd3.format(o=self.actual_file, x=wid, y=hei)
        print(' INFO: Spectrometer is deleting OLD .ogg.png Files on target ')
        call('rm --verbose --force {}/*/*.ogg.png'.format(self.base), shell=1)
        print(' INFO: Spectrometer finished Deleting Files, Starting Render ')
        call(command, shell=True)
        print((''' INFO: Spectrometer finished Rendering Sound using:
               {}{}   OutPut: {}'''.format(command, linesep, self.actual_file)))
        self.spec.setIcon(QIcon('{o}.png'.format(o=self.actual_file)))
        self.spec.setIconSize(QSize(wid, hei))
        self.spec.resize(wid, hei)

    ###########################################################################

    def paintEvent(self, event):
        'Paint semi-transparent background, animated pattern, background text'
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
            p.setPen(QPen(QColor(randint(200, 255), randint(200, 255), 255), 1))
            p.drawPoint(x, y)
        # set pen to use white color
        p.setPen(QPen(QColor(randint(9, 255), randint(9, 255), 255), 1))
        # Rotate painter 45 Degree
        p.rotate(35)
        # Set painter Font for text
        p.setFont(QFont('Ubuntu', 300))
        # draw the background text, with antialiasing
        p.drawText(99, 199, "Radio")
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
        self.showNormal()
        self.resize(QDesktopWidget().screenGeometry().width() // 1.25,
                    QDesktopWidget().screenGeometry().height() // 1.25)
        qr = self.frameGeometry()
        qr.moveCenter(QDesktopWidget().availableGeometry().center())
        self.move(qr.topLeft())

    def nepomuk_set(self, file_tag=None, __tag='', _label='', _description=''):
        ' Quick and Easy Nepomuk Taggify for Files '
        print((''' INFO: Semantic Desktop Experience is Tagging Files :
              {}, {}, {}, {})'''.format(file_tag, __tag, _label, _description)))
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

    def nepomuk_get(self, query_to_search):
        ' Quick and Easy Nepomuk Query for Files '
        print((''' INFO: Semantic Desktop Experience is Quering Files :
              {} '''.format(query_to_search)))
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
    AUTO = False
    try:
        opts, args = getopt(sys.argv[1:], 'hvoba',
                            ['version', 'help', 'opaque', 'borderless', 'auto'])
        pass
    except:
        pass
    for o, v in opts:
        if o in ('-h', '--help'):
            print('''
            Usage:
                  -h, --help        Show help informations and exit.
                  -a, --auto        Auto-Start Recording at start up.
                  -v, --version     Show version information and exit.
                  -o, --opaque      Use Opaque GUI.
                  -b, --borderless  No WM Borders.
                  Run without parameters and arguments to use the GUI.
            ''')
            return sys.exit(1)
        elif o in ('-v', '--version'):
            print(__version__)
            return sys.exit(1)
        elif o in ('-o', '--opaque'):
                OPAQUE = False
        elif o in ('-b', '--borderless'):
                BORDER = False
        elif o in ('-a', '--auto'):
            AUTO = True
    # define our App
    app = QApplication(sys.argv)
    app.setApplicationName(__doc__)
    app.setOrganizationName(__author__)
    app.setOrganizationDomain(__author__)
    app.setStyle('Plastique')
    app.setStyle('Oxygen')
    # w is gonna be the mymainwindow class
    w = MyMainWindow(AUTO)
    # set the class with the attribute of translucent background as true
    if OPAQUE is True:
        w.setAttribute(Qt.WA_TranslucentBackground, True)
    # WM Borders
    if BORDER is False:
        w.setWindowFlags(w.windowFlags() | Qt.FramelessWindowHint)
    # run the class
    w.show()
    # if exiting the loop take down the app
    sys.exit(app.exec_())


if __name__ == '__main__':
    ' Do NOT add anything here!, use main() function instead. '
    main()
