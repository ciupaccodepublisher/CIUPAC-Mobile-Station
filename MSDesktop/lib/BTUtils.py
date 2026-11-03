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

from PySide6.QtCore import (Qt,
                            Slot,
                            Signal,
                            QObject,
                            QByteArray,
                            QIODeviceBase,
                            QTimer)

# QMetaObject
# QPoint, Qt, 
from PySide6.QtBluetooth import (QBluetoothDeviceDiscoveryAgent,
                                 QBluetoothLocalDevice,
                                 QBluetoothDeviceInfo,
                                 QBluetoothAddress,
                                 QBluetoothServiceDiscoveryAgent,
                                 QBluetoothServiceInfo,
                                 QBluetoothSocket,
                                 QBluetoothUuid)
 
# from PySide6.QtWidgets import QDialog
# from PySide6.QtWidgets import QCheckBox
# , QListWidgetItem, QMenu
from time import sleep
from enum import Enum

# INFO: Abstract class to avoid circular import
from GUI.AC_GUIMain import AC_MainWindow
from lib.Utils import (SettingsContainer)
# ------------------------------------------------------------------------------------------------
CHARS_TO_READ_QTY= 128
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class RemoteDeviceState(Enum):
    ABSENT = 0
    PRESENTINLIST = 1
    PAIRED = 2
    SPPPRESENT= 3
    WAITING_ACK= 4
    CONNECTED= 5
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class BTUnit(QObject):
    connectionTrySig= Signal(bool)
    stringReceivedSig= Signal(str)
    commErrorSig= Signal()

    def __init__(self, parent:AC_MainWindow,configF:SettingsContainer):
        super().__init__()
        self.config= configF

        self.busyF= False
        self.tryingToConnectF= False
        self.stationName= ""

        self.parent= parent
        self.connectionTrySig.connect(self.parent.connectionTrySlot, Qt.QueuedConnection)
        self.stringReceivedSig.connect(self.parent.stringReceivedSlot, Qt.QueuedConnection)
        self.commErrorSig.connect(self.parent.commErrorSlot, Qt.QueuedConnection)

        self.localBTDevice = QBluetoothLocalDevice()
        self.aDeviceDA = QBluetoothDeviceDiscoveryAgent()
        hostAddress = QBluetoothAddress(self.localBTDevice.address())
        self.aServiceDA = QBluetoothServiceDiscoveryAgent(hostAddress)

        self.remoteAddress = None
        self.aDeviceDA.deviceDiscovered.connect(self.checkRemoteDevice)
        self.aDeviceDA.finished.connect(self.deviceDiscoveryFinished)
        self.aServiceDA.serviceDiscovered.connect(self.checkService)
        self.aServiceDA.finished.connect(self.serviceScanningEnded)
        self.aSocket= QBluetoothSocket(QBluetoothServiceInfo.RfcommProtocol)
        self.aSocket.stateChanged.connect(self.nStateChanged)
        self.aSocket.errorOccurred.connect(self.nErrorOcurred)
        self.aSocket.readyRead.connect(self.bytesArrived)

        self.__gralTimer = QTimer(self)
        self.__gralTimer.setSingleShot(True)
        self.__gralTimer.timeout.connect(self.gralTimerTimeoutSlot)
    # ------------------------------------------------------------------------------------------------
    def initConnection(self):

        self.busyF= True
        self.tryingToConnectF= True

        self.remoteDevState= RemoteDeviceState.ABSENT
        if (self.localBTDevice.hostMode() == QBluetoothLocalDevice.HostPoweredOff):
            self.endConnectionTryAndNotify(False)
        elif (self.remoteDevState!=RemoteDeviceState.CONNECTED):
            self.connectedDevsList= self.localBTDevice.connectedDevices()
            # INFO: I dont' know how to get data from address, so it will be checked
            # when all devices are scanned
            self.aDeviceDA.start()
    # ------------------------------------------------------------------------------------------------
    def sendString(self, aString=str):
        self.busyF= True
        self.aSocket.write(QByteArray(aString+"\n"))
        self.busyF= False
    # --------------------------------------------------------------------------------------------
    def isConnected(self):
        return self.remoteDevState==RemoteDeviceState.CONNECTED
    # ------------------------------------------------------------------------------------------------
    @Slot(QBluetoothDeviceInfo)
    def checkRemoteDevice(self, info):

        # WARNING: First CIUPAC device found is accepted as the only one
        if (self.remoteDevState==RemoteDeviceState.ABSENT):
            if "CIUPAC-MS-" in info.name():
                self.stationName= info.name()
                self.aDeviceDA.stop()
                self.remoteDevState=RemoteDeviceState.PRESENTINLIST
                msPairingStatus = self.localBTDevice.pairingStatus(info.address())
                if (msPairingStatus != QBluetoothLocalDevice.Unpaired):
                    self.remoteDevState=RemoteDeviceState.PAIRED
                    self.remoteAddress= info.address()
                    # if list is not empty
                    if self.connectedDevsList:
                        for address in self.connectedDevsList:
                            if address==self.remoteAddress:
                                self.remoteDevState=RemoteDeviceState.CONNECTED
                                self.endConnectionTryAndNotify(True)
                                # DAD
                                if self.config.consoleOutputEnabled:
                                    print("Connected!")
                                break
                    if self.remoteDevState!=RemoteDeviceState.CONNECTED:
                        self.aServiceDA.setRemoteAddress(self.remoteAddress)
                        # WARNING: If MS is on but not paired, the following instruction
                        # throws this error: qt.bluetooth.bluez: No uuids found for "78:21:84:79:E8:36"
                        self.aServiceDA.start()
                else:
                    self.endConnectionTryAndNotify(False)
    # ------------------------------------------------------------------------------------------------
    @Slot()
    def deviceDiscoveryFinished(self):
        # MAD
        if self.config.consoleOutputEnabled:
            print("Scan finished, MS state: "+self.remoteDevState.name)
        if (self.remoteDevState==RemoteDeviceState.ABSENT):
            self.endConnectionTryAndNotify(False)
    # ------------------------------------------------------------------------------------------------
    @Slot(QBluetoothServiceInfo)
    def checkService(self, info):
        line = info.serviceName()
        # DAD
        if not line:
            print("WARNING:MS no service found")
            return
        if info.serviceUuid():
            line += "\n\t" + info.serviceUuid().toString()
        else:
            line += "\n\t" + "No service UUID"
        if self.config.consoleOutputEnabled:
            print(line)

        sppPresent=  "Serial Port Profile" in line or \
                     "SPP" in line
        if sppPresent:
            self.remoteDevState= RemoteDeviceState.SPPPRESENT

            # INFO: This one is not supported
            # self.aSocket.connectToService(self.remoteAddress,1)
            # INFO: This one worked out
            self.aSocket.connectToService(self.remoteAddress, 
                                          QBluetoothUuid.ServiceClassUuid.SerialPort,
                                          QIODeviceBase.OpenModeFlag.ReadWrite)
    # ------------------------------------------------------------------------------------------------
    @Slot()
    def serviceScanningEnded(self):
        if (self.remoteDevState.value < RemoteDeviceState.SPPPRESENT.value):
            self.endConnectionTryAndNotify(False)
    # ------------------------------------------------------------------------------------------------
    def endConnectionTryAndNotify(self,success):
        self.connectionTrySig.emit(success)
        if success:
            self.tryingToConnectF=False
        self.busyF=False    
    # ------------------------------------------------------------------------------------------------
    # MAD
    @Slot(QBluetoothSocket.SocketState)
    def nStateChanged(self, aSocketState):
        # DAD
        if self.config.consoleOutputEnabled:
            print("-----")
            print("Trying to connect flag: ",end="")
            print(self.tryingToConnectF)
            print("Socket state changed: "+aSocketState.name)
        if self.tryingToConnectF:
            if (aSocketState==QBluetoothSocket.SocketState.ConnectedState):
                self.testConnectionSlot()                
            elif (aSocketState==QBluetoothSocket.SocketState.UnconnectedState):
                self.endConnectionTryAndNotify(False)
        else:
            if (aSocketState==QBluetoothSocket.SocketState.UnconnectedState):
                self.commErrorSig.emit()
    # ------------------------------------------------------------------------------------------------
    @Slot(QBluetoothSocket.SocketError)
    def nErrorOcurred(self, aSocketError):
        # DAD
        if self.config.consoleOutputEnabled:
            print("-----")
            print("Trying to connect flag: ",end="")
            print(self.tryingToConnectF)
            print("Socket error: "+aSocketError.name)
        if self.tryingToConnectF:
            self.endConnectionTryAndNotify(False)
        else:
            self.commErrorSig.emit()
    # ------------------------------------------------------------------------------------------------
    @Slot()
    def bytesArrived(self):
        aQBArray= self.aSocket.read(CHARS_TO_READ_QTY)
        # DAD
        if (aQBArray.toStdString()=="KA"):
            self.remoteDevState= RemoteDeviceState.CONNECTED
            if self.tryingToConnectF:
                self.endConnectionTryAndNotify(True)
            else:
                # This string has no data meaning, but it is emitted
                # to clear the connection watchdog
                self.stringReceivedSig.emit("KA")
        else:
            self.stringReceivedSig.emit(aQBArray.toStdString())
    # ------------------------------------------------------------------------------------------------            
    @Slot()
    def testConnectionSlot(self):
        self.remoteDevState= RemoteDeviceState.WAITING_ACK
        self.aSocket.write(QByteArray("PING"))
        self.__gralTimer.start(2000)
    # ------------------------------------------------------------------------------------------------
    @Slot()
    def gralTimerTimeoutSlot(self):
        if self.remoteDevState==RemoteDeviceState.WAITING_ACK:
            # If we're already waiting for acknowledgment, that means
            #  BT device didn't answer.
            self.remoteDevState= RemoteDeviceState.SPPPRESENT
            self.commErrorSig.emit()
    # ------------------------------------------------------------------------------------------------

