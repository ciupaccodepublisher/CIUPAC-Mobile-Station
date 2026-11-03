# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MenuSetStorageDirectoryDialog.ui'
##
## Created by: Qt User Interface Compiler version 6.9.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QLabel, QPushButton, QSizePolicy, QWidget)

class Ui_MenuSetStorageDirectoryDialog(object):
    def setupUi(self, MenuSetStorageDirectoryDialog):
        if not MenuSetStorageDirectoryDialog.objectName():
            MenuSetStorageDirectoryDialog.setObjectName(u"MenuSetStorageDirectoryDialog")
        MenuSetStorageDirectoryDialog.resize(400, 181)
        self.buttonBox = QDialogButtonBox(MenuSetStorageDirectoryDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(40, 140, 341, 32))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.lblShowCurrentDir = QLabel(MenuSetStorageDirectoryDialog)
        self.lblShowCurrentDir.setObjectName(u"lblShowCurrentDir")
        self.lblShowCurrentDir.setGeometry(QRect(20, 10, 181, 18))
        # self.lblShowCurrentDir.setGeometry(QRect(20, 10, 256, 18))
        self.lblShowCurrentDir.setText(u"Current storage directory is:")
        self.lblCurrentDir = QLabel(MenuSetStorageDirectoryDialog)
        self.lblCurrentDir.setObjectName(u"lblCurrentDir")
        # self.lblCurrentDir.setGeometry(QRect(40, 30, 181, 18))
        self.lblCurrentDir.setGeometry(QRect(40, 30, 320, 18))
        self.lblCurrentDir.setText(u"Some directory")
        self.btnChooseDir = QPushButton(MenuSetStorageDirectoryDialog)
        self.btnChooseDir.setObjectName(u"btnChooseDir")
        self.btnChooseDir.setGeometry(QRect(20, 90, 88, 34))

        self.retranslateUi(MenuSetStorageDirectoryDialog)
        self.buttonBox.accepted.connect(MenuSetStorageDirectoryDialog.accept)
        self.buttonBox.rejected.connect(MenuSetStorageDirectoryDialog.reject)

        QMetaObject.connectSlotsByName(MenuSetStorageDirectoryDialog)
    # setupUi

    def retranslateUi(self, MenuSetStorageDirectoryDialog):
        MenuSetStorageDirectoryDialog.setWindowTitle(QCoreApplication.translate("MenuSetStorageDirectoryDialog", u"Dialog", None))
        self.btnChooseDir.setText(QCoreApplication.translate("MenuSetStorageDirectoryDialog", u"Choose...", None))
    # retranslateUi

