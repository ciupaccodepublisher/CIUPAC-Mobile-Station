# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later
#####################################################################################################
# Copyright (C) 2026 Emiliano Farías <efarias@iado-conicet.gob.ar>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://gnu.org>.
#####################################################################################################

# INFO: In NMEA GGA time format, time is represented as hhmmss.ss,
# where hh is hours, mm is minutes, and ss is seconds with optional decimal fractions.
# The time is in Universal Time Coordinated (UTC)

# INFO: NMEA GGA message latitude/longitude format:
# [D]DDMM.MMMMM
# D is degrees, and MM.MMMMM are minutes with decimal point (NOT seconds)
# NMEASentence / NMEA Object format/structure:
# latitude and longitude properties exist as python floats (DD, "decimal degrees") instead of the DDDMM.MMMM
# format used in the NMEA protocol. latitude_minutes, latitude_seconds, longitude_minutes, and longitude_seconds
# are also supported. Ex.:
# >>> msg.latitude
# -19.4840833333
# >>> msg.longitude
# 24.1751
# >>> '%02d°%07.4f′' % (msg.latitude, msg.latitude_minutes)
# '-19°29.0450′'
# >>> '%02d°%02d′%07.4f″' % (msg.latitude, msg.latitude_minutes, msg.latitude_seconds)
# "-19°29′02.7000″"

from PySide6.QtCore import (Qt,
                            Slot,
                            QTimer,
                            Signal,
                            QDir,
                            QFile,
                            QDateTime,
                            QByteArray)
import PySide6.QtCore as QtCore
from PySide6.QtWidgets import (QMessageBox,
                               QDialog,
                               QFileDialog)
# QMainWindow
from time import (time)

from GUI.MainScreen import Ui_MainWindow
from GUI.AC_GUIMain import AC_MainWindow
from GUI.MenuSetStorageDirectoryDialog import Ui_MenuSetStorageDirectoryDialog
from GUI.AboutDialog import AboutDialog
from lib.Utils import (SettingsContainer,
                       IntervalCounter,
                       StationMsgManager,
                       FileReader)
from lib import (BTUtils)
import os
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class StorageDirectoryDialog(QDialog,Ui_MenuSetStorageDirectoryDialog):
    def __init__(self,MainWindow):
        super().__init__(parent= MainWindow)
        self.setupUi(self)
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class MainWindow(AC_MainWindow):
    
    testConnectionSig= Signal()
    # ----------------------------------------------------------------------------------------------
    def __init__(self,configF:SettingsContainer):

        self.config= configF
        self.recording= False
        self.timeSinceLastLocationData= 0
        self.connectionWatchdog= IntervalCounter(self.config.btConnectionWatchdogIvalS,False)

        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.deviceNFMsg= QMessageBox()
        self.deviceNFMsg.buttonClicked.connect(self.deviceNotFoundAcknowledge)
        self.commErrorMsg= QMessageBox()
        self.commErrorMsg.buttonClicked.connect(self.commErrorAckSlot)

        self.ui.setupUi(self)
        self.startStopBtnShowsStart= True
        self.ui.StartStopBtn.clicked.connect(self.startStopBtnClickedSlot)
        self.ui.actionStorage_directory.triggered.connect(self.actionStorage_directoryTriggeredSlot)
        # Licensing: "About..." entry in the menu bar, right next to "Settings"
        self.aboutAction= self.ui.menuBar.addAction("About...")
        self.aboutAction.triggered.connect(self.actionAboutTriggeredSlot)

        if self.config.btPresent:
            self.aBTUnit= BTUtils.BTUnit(self,self.config)
            self.testConnectionSig.connect(self.aBTUnit.testConnectionSlot, Qt.QueuedConnection)
            self.aBTUnit.initConnection()

        # This timer will tick every fixed interval
        # and counters are deployed to count any amount of seconds needed.
        # I mean, there's only one clock and several counters
        self.__gralTimer = QTimer(self)
        self.__gralTimer.timeout.connect(self.gralTimerTimeoutSlot)
        self.__gralTimer.start(1000)
        self.__msgMgr= StationMsgManager(self.config)

        self.__menuActionStorageDirectoryDialog= StorageDirectoryDialog(self)
        self.__menuActionStorageDirectoryDialog.lblCurrentDir.setText(self.config.storageDirectory)
        self.__menuActionStorageDirectoryDialog.btnChooseDir.clicked.connect(self.storageDirectoryChooseBtnPressedSlot)

        # DAD
        if self.config.testing:
            self.counter=0
            self.storedCSV= True
            self.fileHelper= FileReader("./extra/temp/250424-fake-date-change.csv",self.storedCSV)
            self.thereStillSomeLine= True
            self.auxWatchdog= IntervalCounter(self.config.testingWDIntervalS,True)
            self.ui.StartStopBtn.setEnabled(True)
    # ------------------------------------------------------------------------------------------------
    @Slot()
    def startStopBtnClickedSlot(self):
        if self.startStopBtnShowsStart:
            self.recording= True
            self.__msgMgr.beginOfNewSeries()
            self.ui.StartStopBtn.setText("Stop")
            self.startStopBtnShowsStart= False
            self.ui.mapGV.resetGraph()
            dateTimeMgr= QDateTime(QDateTime.currentDateTime())
            if self.config.testing:
                fileName= dateTimeMgr.toString("yyMMdd-hhmmss")+".csv"
            else:
                fileName= dateTimeMgr.toString("yyMMdd-hhmmss")+"-"+self.aBTUnit.stationName+".csv"
            fileFullPath= os.path.join(self.config.storageDirectory, fileName)
            self.recordingFile= QFile(fileFullPath)
        else:
            # TODO: HERE. Disable button if station is not connected.
            self.recording= False
            # DAD
            if not self.config.testing:
                if self.aBTUnit.remoteDevState!= BTUtils.RemoteDeviceState.CONNECTED:
                    self.ui.StartStopBtn.setEnabled(False)
            self.ui.StartStopBtn.setText("Start")
            self.startStopBtnShowsStart= True
    # ------------------------------------------------------------------------------------------------
    @Slot()
    def actionStorage_directoryTriggeredSlot(self):
        dialogResult= self.__menuActionStorageDirectoryDialog.exec()
        if dialogResult == QDialog.DialogCode.Accepted:
            self.config.storageDirectory= self.__newDirPath
            self.config.save()
        if self.config.consoleOutputEnabled:
            print(f"Saved storage directory: {self.config.storageDirectory}")
    # ------------------------------------------------------------------------------------------------
    @Slot()
    def actionAboutTriggeredSlot(self):
        AboutDialog(self).exec()
    # ------------------------------------------------------------------------------------------------
    @Slot()
    def storageDirectoryChooseBtnPressedSlot(self):
        # Within a QWidget method
        selectStorageDirDialog= QFileDialog(self)

        selectStorageDirDialog.setFileMode(QFileDialog.Directory)
        selectStorageDirDialog.setOption(QFileDialog.Option.ShowDirsOnly)
        selectStorageDirDialog.setOption(QFileDialog.Option.DontUseNativeDialog)

        self.__newDirPath= selectStorageDirDialog.getExistingDirectory(
                self, 
                "Select storage directory", 
                self.config.storageDirectory)

        if  self.__newDirPath:
            self.__menuActionStorageDirectoryDialog.lblCurrentDir.setText(self.__newDirPath)
            if self.config.consoleOutputEnabled:
                print(f"Selected storage directory: {self.__newDirPath}")
    # ------------------------------------------------------------------------------------------------
    @Slot(bool)
    def connectionTrySlot(self,success):
        if success:
            self.deviceFoundC()
        else:
            self.deviceNotFoundC()
    # ------------------------------------------------------------------------------------------------
    @Slot()
    def commErrorSlot(self):
        self.commErrorMsg.setText("BT Communication error!.")
        self.commErrorMsg.setInformativeText("Reconnection will start "
                                             +"as soon as you acept this message.")
        self.commErrorMsg.setIcon(QMessageBox.Warning)
        self.commErrorMsg.exec()
    # ------------------------------------------------------------------------------------------------
    def deviceFoundC(self):
        self.ui.StatusVbeLbl.setText("Device Found")
        if not self.aBTUnit.busyF:
            secondsSinceEpoch = str(int(time()))
            self.aBTUnit.sendString("SETTIME")
            self.aBTUnit.sendString(secondsSinceEpoch)
        
        self.ui.StatusVbeLbl.setText("CONNECTED")
        self.ui.StartStopBtn.setEnabled(True)
    # ------------------------------------------------------------------------------------------------
    def deviceNotFoundC(self):
        self.deviceNFMsg.setText("Mobile station not found!.")
        self.deviceNFMsg.setInformativeText("Check that:\n"+
                                            "* BT is on\n"+
                                            "* Mobile station is on\n"+
                                            "* Mobile station is already paired.")
        self.deviceNFMsg.setIcon(QMessageBox.Warning)
        self.deviceNFMsg.exec()
    # ------------------------------------------------------------------------------------------------
    @Slot()
    def deviceNotFoundAcknowledge(self):
        self.close()
    # ------------------------------------------------------------------------------------------------
    @Slot()
    def commErrorAckSlot(self):
    #     Recording should keep going if already started.
    #     Else it should not be allowed to start recording.
        if not self.startStopBtnShowsStart:
            self.ui.StartStopBtn.setEnabled(False)
        self.ui.StatusVbeLbl.setText("WAIT...")
        # TODO: WARNING: I'm not closing any socket, etc.
        self.aBTUnit.initConnection()
    # ------------------------------------------------------------------------------------------------
    @Slot(str)
    def stringReceivedSlot(self,recvdStrM):
        self.connectionWatchdog.reset()
        # DAD
        if self.config.consoleOutputEnabled:
            print("------------------------------------------------------------------")
            print("Received string: %s" % recvdStrM)
        self.__msgMgr.processMsg(recvdStrM)
        if self.__msgMgr.isAValidMsg:
            # TODO: Keep coding msg mgr class
            # TODO: Maybe include temperature in graph
            nmeaObj= self.__msgMgr.nmeaObj
            if self.recording:
                self.recordingFile.open(QtCore.QIODeviceBase.OpenModeFlag.Append)
                self.recordingFile.write(QByteArray(self.__msgMgr.getRecordString()))
                self.recordingFile.close()
            self.ui.TempVbeLbl.setText(self.__msgMgr.temperature)
            self.ui.HumVbeLbl.setText(self.__msgMgr.humidity)
            viewMustBeResized= self.ui.mapGV.plotNMEAObj(nmeaObj)
            if viewMustBeResized:
                aSceneRect= self.ui.mapGV.scene().itemsBoundingRect()
                self.ui.mapGV.fitInView(aSceneRect, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
            self.ui.DistanceVbeLbl.display(self.ui.mapGV.getDistanceBWLastTwoPoints())
            self.timeSinceLastLocationData= 0
    # ------------------------------------------------------------------------------------------------
    @Slot()
    def gralTimerTimeoutSlot(self):

        if self.config.testing:
            if self.auxWatchdog.checkAndClear():
                if self.thereStillSomeLine:
                    try:
                        aLine= self.fileHelper.getNextLine()
                    except:
                        self.thereStillSomeLine= False
                    else:
                        self.stringReceivedSlot(aLine)

        if self.config.btPresent:
            # If not trying to connect and no new data has arrived in time
            if self.connectionWatchdog.checkAndClear():
                # If it is allegedly connected but no new data has arrived in time
                if self.aBTUnit.isConnected():
                    # DAD
                    print("Timeout!")
                    self.testConnectionSig.emit()

        self.ui.TimeLcd.display(self.timeSinceLastLocationData)
        self.timeSinceLastLocationData+= 1
    # ------------------------------------------------------------------------------------------------
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
