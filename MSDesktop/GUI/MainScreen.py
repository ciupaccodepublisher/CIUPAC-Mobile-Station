# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainScreen.ui'
##
## Created by: Qt User Interface Compiler version 6.9.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLCDNumber, QLabel,
    QLayout, QMainWindow, QMenu, QMenuBar,
    QPushButton, QSizePolicy, QSpacerItem, QStatusBar,
    QVBoxLayout, QWidget)

from .GUIExtras import MainGraphicsView

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(783, 601)
        MainWindow.setWindowTitle(u"MobileStationDesktop")
        self.actionStorage_directory = QAction(MainWindow)
        self.actionStorage_directory.setObjectName(u"actionStorage_directory")
        self.MainWdt = QWidget(MainWindow)
        self.MainWdt.setObjectName(u"MainWdt")
        self.verticalLayout = QVBoxLayout(self.MainWdt)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.connectionLout = QHBoxLayout()
        self.connectionLout.setObjectName(u"connectionLout")
        self.connectionLout.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)
        self.StatusLbl = QLabel(self.MainWdt)
        self.StatusLbl.setObjectName(u"StatusLbl")

        self.connectionLout.addWidget(self.StatusLbl)

        self.StatusVbeLbl = QLabel(self.MainWdt)
        self.StatusVbeLbl.setObjectName(u"StatusVbeLbl")

        self.connectionLout.addWidget(self.StatusVbeLbl)

        self.TimeLbl = QLabel(self.MainWdt)
        self.TimeLbl.setObjectName(u"TimeLbl")

        self.connectionLout.addWidget(self.TimeLbl)

        self.TimeLcd = QLCDNumber(self.MainWdt)
        self.TimeLcd.setObjectName(u"TimeLcd")

        self.connectionLout.addWidget(self.TimeLcd)

        self.DistanceLbl = QLabel(self.MainWdt)
        self.DistanceLbl.setObjectName(u"DistanceLbl")

        self.connectionLout.addWidget(self.DistanceLbl)

        self.DistanceVbeLbl = QLCDNumber(self.MainWdt)
        self.DistanceVbeLbl.setObjectName(u"DistanceVbeLbl")

        self.connectionLout.addWidget(self.DistanceVbeLbl)

        self.TempLbl = QLabel(self.MainWdt)
        self.TempLbl.setObjectName(u"TempLbl")

        self.connectionLout.addWidget(self.TempLbl)

        self.TempVbeLbl = QLabel(self.MainWdt)
        self.TempVbeLbl.setObjectName(u"TempVbeLbl")
        font = QFont()
        font.setPointSize(15)
        self.TempVbeLbl.setFont(font)
        self.TempVbeLbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.connectionLout.addWidget(self.TempVbeLbl)

        self.HumLbl = QLabel(self.MainWdt)
        self.HumLbl.setObjectName(u"HumLbl")

        self.connectionLout.addWidget(self.HumLbl)

        self.HumVbeLbl = QLabel(self.MainWdt)
        self.HumVbeLbl.setObjectName(u"HumVbeLbl")
        self.HumVbeLbl.setFont(font)
        self.HumVbeLbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.connectionLout.addWidget(self.HumVbeLbl)


        self.verticalLayout.addLayout(self.connectionLout)

        self.BottomLout = QHBoxLayout()
        self.BottomLout.setObjectName(u"BottomLout")
        self.mapGV = MainGraphicsView(self.MainWdt)
        self.mapGV.setObjectName(u"mapGV")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mapGV.sizePolicy().hasHeightForWidth())
        self.mapGV.setSizePolicy(sizePolicy)

        self.BottomLout.addWidget(self.mapGV)

        self.ButtonsLout = QVBoxLayout()
        self.ButtonsLout.setObjectName(u"ButtonsLout")
        self.ButtonsLout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.StartStopBtn = QPushButton(self.MainWdt)
        self.StartStopBtn.setObjectName(u"StartStopBtn")
        self.StartStopBtn.setEnabled(False)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.StartStopBtn.sizePolicy().hasHeightForWidth())
        self.StartStopBtn.setSizePolicy(sizePolicy1)

        self.ButtonsLout.addWidget(self.StartStopBtn)

        self.ButtonsSper = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.ButtonsLout.addItem(self.ButtonsSper)


        self.BottomLout.addLayout(self.ButtonsLout)


        self.verticalLayout.addLayout(self.BottomLout)

        MainWindow.setCentralWidget(self.MainWdt)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 783, 30))
        self.menuSettings = QMenu(self.menuBar)
        self.menuSettings.setObjectName(u"menuSettings")
        self.menuSettings.setTitle(u"Settings")
        MainWindow.setMenuBar(self.menuBar)

        self.menuBar.addAction(self.menuSettings.menuAction())
        self.menuSettings.addAction(self.actionStorage_directory)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        self.actionStorage_directory.setText(QCoreApplication.translate("MainWindow", u"Storage directory...", None))
        self.StatusLbl.setText(QCoreApplication.translate("MainWindow", u"Status:", None))
        self.StatusVbeLbl.setText(QCoreApplication.translate("MainWindow", u"WAIT...", None))
        self.TimeLbl.setText(QCoreApplication.translate("MainWindow", u"Time since\n"
"last location", None))
        self.DistanceLbl.setText(QCoreApplication.translate("MainWindow", u"Distance between\n"
"last locations", None))
        self.TempLbl.setText(QCoreApplication.translate("MainWindow", u"Temperature", None))
        self.TempVbeLbl.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.HumLbl.setText(QCoreApplication.translate("MainWindow", u"Humidity", None))
        self.HumVbeLbl.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.StartStopBtn.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        pass
    # retranslateUi

