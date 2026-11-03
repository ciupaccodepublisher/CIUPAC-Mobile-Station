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

import PySide6.QtWidgets as QtWidgets
from PySide6.QtWidgets import QGraphicsView, QWidget
import PySide6.QtCore as QtCore
from PySide6.QtCore import (QRectF)
from PySide6.QtGui import (QPen,
                           QBrush)
import pynmea2
import math
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Representation of NMEA point into 2D plane.
# Origin: fixed to first sampled point
# __oX is meters from Greenwich meridian.
# __oY is meters from equator
# x,y are meters from origin, assuming no curvature.
# INFO: Y axis is inverted
class PlotPoint:
    __EARTH_RADIUS_M= 6378137
    def __init__(self):
        self.x= 0
        self.y= 0
        # Origin of coordinates
        self.__oX=0
        self.__oY=0
        # Aux
        self.__latRads=0
    # ------------------------------------------------------------------------------------------------
    # Returns a (x,y) tuple of absolute position
    def __convert(latitudeM:float,longitudeM:float):
        __latRads= math.radians(latitudeM)
        __latitudeCircleRadius= PlotPoint.__EARTH_RADIUS_M*math.sin(math.pi/2-math.fabs(__latRads))
        __x= __latitudeCircleRadius*math.radians(longitudeM)
        __y= -PlotPoint.__EARTH_RADIUS_M*__latRads
        return __x,__y
    # ------------------------------------------------------------------------------------------------
    def setOrigin(self, nmeaObj:pynmea2.NMEASentence):
        self.__oX, self.__oY= PlotPoint.__convert (nmeaObj.latitude,nmeaObj.longitude)
    # ------------------------------------------------------------------------------------------------
    def copyFromNMEAObject(self,nmeaObj:pynmea2.NMEASentence):
        self.x, self.y= PlotPoint.__convert (nmeaObj.latitude,nmeaObj.longitude)
        self.x= self.x-self.__oX
        self.y= self.y-self.__oY
    # ------------------------------------------------------------------------------------------------
    # INFO: methods are created before class, so type annotation PlotPoint would throw a 'name not
    # defined' error. To avoid this, literals 'PlotPoint' has to be used.'
    # So much for this shitty language
    def copyFrom(self,pointM:'PlotPoint'):
        self.x= pointM.x
        self.y= pointM.y
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Keeps track of visual area limits and contains objects to manipulate points
class PointsGeometryManager():
    def __init__(self):
        self.reset()
    # ------------------------------------------------------------------------------------------------
    def reset(self):
        self.__minX=0
        self.__maxX=0
        self.__minY=0
        self.__maxY=0
        self.__M= 40
        self.__firstPoint= True
        self.__defaultRadius=0.01
        self.previousRadius=0
        self.ellipseRect= QRectF()
        self.previousEllipse= QtWidgets.QGraphicsEllipseItem()
    # ------------------------------------------------------------------------------------------------
    # Radius of new points is determined to be of constant size within visualized area.
    def recommendedRadius(self, p:PlotPoint)->float:
        if self.__firstPoint:
            self.__minX= p.x-self.__defaultRadius
            self.__maxX = p.x+self.__defaultRadius
            self.__minY= p.y-self.__defaultRadius
            self.__maxY = p.y+self.__defaultRadius
            self.__firstPoint= False
            return self.__defaultRadius
        else:
            # The thing is: area should be expanded if position plus new radius
            # is bigger than previous boundary
            # But also new radius is a function of new area, so we start by calculating
            # AS if limits were exceeded and then check if they really are.
            # These are the equations for a point that just fits new area (right x limit):
            # x+r= xm; r= (xm-xnp)/M, where:
            # x: position x of new point
            # r: new radius, if exists
            # xm: new right x limit/boundary
            # xnp= actual left x limit
            # These eqs. left:
            # r= (x-xn)/(M-1)

            # Radius if left limit exceeded:
            r= (self.__maxX-p.x)/(self.__M-1)

            # Checking xmin:
            if self.__minX > p.x-r:
                self.__minX= p.x-r
            else:
                # If xmin was not exceeded, we have to check xmax
                r= (p.x-self.__minX)/(self.__M-1)
                if self.__maxX < p.x+r:
                    self.__maxX = p.x+r

            # And same shit for Y axis:
            r= (self.__maxY-p.y)/(self.__M-1)
            if self.__minY > p.y-r:
                self.__minY= p.y-r
            else:
                r= (p.y-self.__minY)/(self.__M-1)
                if self.__maxY < p.y+r:
                    self.__maxY = p.y+r

            spanX= self.__maxX-self.__minX
            spanY= self.__maxY-self.__minY

            if spanX > spanY:
                span= spanX
            else:
                span= spanY

            return span/self.__M
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class MainGraphicsView(QGraphicsView):
    def __init__(self,mainWdt: QWidget):
        super().__init__(mainWdt)
        self.mainScene= QtWidgets.QGraphicsScene(self)
        self.setScene(self.mainScene)
        # MAD
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        self.pointsPen= QPen()
        # No borders on points
        self.pointsPen.setStyle(QtCore.Qt.PenStyle.NoPen)

        # Past time points are black
        self.blackPointsBrush= QBrush(QtCore.Qt.BrushStyle.SolidPattern)
        # Current point should be red
        self.redPointsBrush= QBrush(QtCore.Qt.GlobalColor.red, QtCore.Qt.BrushStyle.SolidPattern)
        self.pointsDimTracker= PointsGeometryManager()
        self.currentPlotPoint= PlotPoint()
        self.__previousPlotPoint= PlotPoint()
        self.__empty= True

        # MAD: Not used tools:
        # self.mainScene.sceneRectChanged.connect(self.sceneRectChangedSlot)
        # left, top, width, height)
        # sceneRect= QtCore.QRectF(-180,90,360,180)
        # print(f"{sceneRect=}")
        # self.setSceneRect(sceneRect)
        # self.maxX= self.scene().width()/2
# ------------------------------------------------------------------------------------------------
    # After plotting the point, method returns if the view must be resized
    # True: View must be resized
    def plotNMEAObj(self,nmeaObj:pynmea2.NMEASentence)->bool:
        
        if self.__empty:
            self.currentPlotPoint.setOrigin(nmeaObj)
            self.__empty= False
            self.currentPlotPoint.copyFromNMEAObject(nmeaObj)
        self.__previousPlotPoint.copyFrom(self.currentPlotPoint)
        self.currentPlotPoint.copyFromNMEAObject(nmeaObj)

        pointRadius= self.pointsDimTracker.recommendedRadius(self.currentPlotPoint)
        # Radius change if there is a visual area change.
        # That will happen only if new point is ouside current area.
        # If not, there's no need to redraw all points.
        viewMustBeResized= False
        if pointRadius != self.pointsDimTracker.previousRadius:
            viewMustBeResized= True
            self.pointsDimTracker.ellipseRect= QRectF(-pointRadius,-pointRadius,pointRadius*2.0,pointRadius*2.0)

            # Each point must be resized to mantain proportion.
            for item in self.mainScene.items():
                if type(item).__name__== "QGraphicsEllipseItem":
                    item.setRect(self.pointsDimTracker.ellipseRect)
            self.pointsDimTracker.previousRadius= pointRadius
        # Last point draw before current one should turn from red to black
        self.pointsDimTracker.previousEllipse.setBrush(self.blackPointsBrush)

        aEllipse= QtWidgets.QGraphicsEllipseItem(self.pointsDimTracker.ellipseRect)
        aEllipse.setPen(self.pointsPen)
        aEllipse.setBrush(self.redPointsBrush)
        aEllipse.setPos(self.currentPlotPoint.x,self.currentPlotPoint.y)
        
        self.mainScene.addItem(aEllipse)
        self.pointsDimTracker.previousEllipse= aEllipse
        return viewMustBeResized

        # MAD: Not used tools:
        # aEllipse.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIgnoresTransformations)
        # self.mainScene.addItem(self.aEllipse,self.pointsPen, self.blackPointsBrush)
    # ------------------------------------------------------------------------------------------------
    def getDistanceBWLastTwoPoints(self)->float:
        __deltaX= self.currentPlotPoint.x-self.__previousPlotPoint.x
        __deltaY= self.currentPlotPoint.y-self.__previousPlotPoint.y
        return math.sqrt(__deltaX ** 2 + __deltaY ** 2)
    # ------------------------------------------------------------------------------------------------
    def resetGraph(self):
        self.mainScene.clear()
        self.pointsDimTracker.reset()
        self.__empty= True
# ------------------------------------------------------------------------------------------------
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
